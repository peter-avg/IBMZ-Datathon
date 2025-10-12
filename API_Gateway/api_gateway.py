import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import date, datetime

# --- 1. Configuration and Setup ---

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment variables and add a safety check
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set. Please create a .env file.")

# Create the FastAPI app instance
app = FastAPI()

# Database engine setup
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set to True for debugging to see SQL queries
    connect_args={"ssl": "require"}
)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Dependency to get a database session
async def get_db():
    async with async_session() as session:
        yield session

# --- 2. Pydantic Models (Data Schemas) ---

# --- Doctor Schemas ---
class DoctorBase(BaseModel):
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None

class DoctorCreate(DoctorBase):
    pass

class DoctorUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class Doctor(DoctorBase):
    doctor_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# --- Patient Schemas ---
class PatientBase(BaseModel):
    full_name: str
    dob: Optional[date] = None
    sex_at_birth: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    full_name: Optional[str] = None
    dob: Optional[date] = None
    sex_at_birth: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class Patient(PatientBase):
    patient_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# --- Form Schemas (Simplified for this example) ---
# In a real app, you would have detailed models for symptoms and medications
class SymptomCreate(BaseModel):
    name: str
    duration: Optional[int] = None
    intensity: Optional[int] = None

class MedicationCreate(BaseModel):
    name: str
    strength: Optional[int] = None
    
class FormCreate(BaseModel):
    patient_id: UUID
    doctor_id: UUID = None
    symptoms: List[SymptomCreate]
    medications: Optional[List[MedicationCreate]] = None

# --- 3. API Endpoints ---

# === DOCTOR ENDPOINTS ===

@app.post("/doctors/", response_model=Doctor, status_code=status.HTTP_201_CREATED)
async def create_doctor(doctor: DoctorCreate, db: AsyncSession = Depends(get_db)):
    query = text("""
        INSERT INTO doctor (doctor_id, full_name, email, phone)
        VALUES (:doctor_id, :full_name, :email, :phone)
        RETURNING *
    """)
    new_doctor_id = uuid4()
    result = await db.execute(query, {**doctor.model_dump(), "doctor_id": new_doctor_id})
    await db.commit()
    return result.mappings().first()

@app.get("/doctors/", response_model=List[Doctor])
async def read_doctors(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM doctor"))
    return result.mappings().all()

@app.get("/doctors/{doctor_id}", response_model=Doctor)
async def read_doctor(doctor_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM doctor WHERE doctor_id = :id"), {"id": doctor_id})
    db_doctor = result.mappings().first()
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return db_doctor

@app.patch("/doctors/{doctor_id}", response_model=Doctor)
async def update_doctor(doctor_id: UUID, doctor_data: DoctorUpdate, db: AsyncSession = Depends(get_db)):
    update_data = doctor_data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")
    set_clause = ", ".join(f"{key} = :{key}" for key in update_data.keys())
    query = text(f"UPDATE doctor SET {set_clause} WHERE doctor_id = :id RETURNING *")
    result = await db.execute(query, {"id": doctor_id, **update_data})
    await db.commit()
    updated_doctor = result.mappings().first()
    if updated_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return updated_doctor

@app.delete("/doctors/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(doctor_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("DELETE FROM doctor WHERE doctor_id = :id"), {"id": doctor_id})
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Doctor not found")
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# === PATIENT ENDPOINTS ===

@app.post("/patients/", response_model=Patient, status_code=status.HTTP_201_CREATED)
async def create_patient(patient: PatientCreate, db: AsyncSession = Depends(get_db)):
    query = text("""
        INSERT INTO patient (patient_id, full_name, dob, sex_at_birth, phone, email)
        VALUES (:patient_id, :full_name, :dob, :sex_at_birth, :phone, :email)
        RETURNING *
    """)
    new_patient_id = uuid4()
    result = await db.execute(query, {**patient.model_dump(), "patient_id": new_patient_id})
    await db.commit()
    return result.mappings().first()

@app.get("/patients/", response_model=List[Patient])
async def read_patients(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM patient"))
    return result.mappings().all()

@app.get("/patients/{patient_id}", response_model=Patient)
async def read_patient(patient_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM patient WHERE patient_id = :id"), {"id": patient_id})
    db_patient = result.mappings().first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

@app.patch("/patients/{patient_id}", response_model=Patient)
async def update_patient(patient_id: UUID, patient_data: PatientUpdate, db: AsyncSession = Depends(get_db)):
    update_data = patient_data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")
    set_clause = ", ".join(f"{key} = :{key}" for key in update_data.keys())
    query = text(f"UPDATE patient SET {set_clause} WHERE patient_id = :id RETURNING *")
    result = await db.execute(query, {"id": patient_id, **update_data})
    await db.commit()
    updated_patient = result.mappings().first()
    if updated_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return updated_patient

@app.delete("/patients/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(patient_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("DELETE FROM patient WHERE patient_id = :id"), {"id": patient_id})
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Patient not found")
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
# === FORM SUBMISSION ENDPOINT ===

@app.post("/forms/", status_code=status.HTTP_201_CREATED)
async def create_form_submission(form_data: FormCreate, db: AsyncSession = Depends(get_db)):
    # This is a complex transaction, so we handle it carefully.
    # In a real-world scenario, you might use SQLAlchemy's ORM for this to make it cleaner.
    new_form_id = uuid4()
    
    try:
        # --- Logic to Check and create doctor_patient relationship ---
        check_query = text("""
            SELECT 1 FROM doctor_patient 
            WHERE doctor_id = :doctor_id AND patient_id = :patient_id
        """)
        existing_relation = await db.execute(check_query, {
            "doctor_id": form_data.doctor_id,
            "patient_id": form_data.patient_id
        })

        # If the query returns no rows, the relationship does not exist
        if existing_relation.scalar_one_or_none() is None:
            relationship_query = text("""
                INSERT INTO doctor_patient (doctor_patient_id, doctor_id, patient_id)
                VALUES (:id, :doctor_id, :patient_id)
            """)
            await db.execute(relationship_query, {
                "id": uuid4(),
                "doctor_id": form_data.doctor_id,
                "patient_id": form_data.patient_id
            })
        # --- End of relationship creation logic ---

        # 1. Create the main form entry
        form_query = text("""
            INSERT INTO form (form_id, patient_id, doctor_id)
            VALUES (:form_id, :patient_id, :doctor_id)
        """)
        await db.execute(form_query, {
            "form_id": new_form_id,
            "patient_id": form_data.patient_id,
            "doctor_id": form_data.doctor_id
        })

        # 2. Insert all symptoms and link them
        for symptom in form_data.symptoms:
            new_symptom_id = uuid4()
            symptom_query = text("""
                INSERT INTO symptom (symptom_id, name, duration, intensity)
                VALUES (:symptom_id, :name, :duration, :intensity)
            """)
            await db.execute(symptom_query, {**symptom.model_dump(), "symptom_id": new_symptom_id})
            
            link_symptom_query = text("""
                INSERT INTO form_symptom (form_symptom_id, form_id, symptom_id)
                VALUES (:form_symptom_id, :form_id, :symptom_id)
            """)
            await db.execute(link_symptom_query, {
                "form_symptom_id": uuid4(),
                "form_id": new_form_id,
                "symptom_id": new_symptom_id
            })

        # 3. Insert all medications and link them
        if form_data.medications:
            for medication in form_data.medications:
                new_medication_id = uuid4()
                medication_query = text("""
                    INSERT INTO medication (medication_id, name, strength)
                    VALUES (:medication_id, :name, :strength)
                """)
                await db.execute(medication_query, {**medication.model_dump(), "medication_id": new_medication_id})
                
                link_medication_query = text("""
                    INSERT INTO form_medication (form_medication_id, form_id, medication_id)
                    VALUES (:form_medication_id, :form_id, :medication_id)
                """)
                await db.execute(link_medication_query, {
                    "form_medication_id": uuid4(),
                    "form_id": new_form_id,
                    "medication_id": new_medication_id
                })

        # If all went well, commit the transaction
        await db.commit()
        return {"form_id": new_form_id, "status": "Submission successful"}
        
    except Exception as e:
        # If any step fails, roll back all changes
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Transaction failed: {e}")