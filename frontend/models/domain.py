"""Domain models for AI-assisted Clinical Forms application."""

from datetime import datetime, date
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class FormStatus(str, Enum):
    """Form status enumeration."""
    DRAFT = "draft"
    FINALIZED = "finalized"


class Doctor(BaseModel):
    """Doctor entity model."""
    id: str = Field(..., description="Primary key")
    name: str = Field(..., description="Doctor's full name")


class Patient(BaseModel):
    """Patient entity model."""
    id: str = Field(..., description="Primary key")
    name: str = Field(..., description="Patient's full name")
    email: Optional[str] = Field(
        None, description="Patient's email address"
    )
    date_of_birth: Optional[date] = Field(
        None, description="Patient's date of birth"
    )


class Form(BaseModel):
    """Clinical form entity model."""
    id: str = Field(..., description="Primary key")
    patient_id: str = Field(..., description="Foreign key to Patient")
    doctor_id: str = Field(..., description="Foreign key to Doctor")
    created_at: Optional[datetime] = Field(
        None, description="Form creation timestamp"
    )
    status: FormStatus = Field(FormStatus.DRAFT, description="Form status")
    free_text_notes: Optional[str] = Field(
        None, description="Free text notes"
    )


class Symptom(BaseModel):
    """Symptom entity model."""
    id: str = Field(..., description="Primary key")
    form_id: str = Field(..., description="Foreign key to Form")
    name: str = Field(..., description="Symptom name")
    duration: Optional[str] = Field(None, description="Symptom duration")
    intensity: Optional[str] = Field(
        None, description="Symptom intensity (1-10 or mild/moderate/severe)"
    )
    recurrence: Optional[str] = Field(
        None, description="Symptom recurrence pattern"
    )


class Medication(BaseModel):
    """Medication entity model."""
    id: str = Field(..., description="Primary key")
    form_id: str = Field(..., description="Foreign key to Form")
    name: str = Field(..., description="Medication name")
    strength: Optional[str] = Field(
        None, description="Medication strength (e.g., '500 mg')"
    )
    frequency: Optional[str] = Field(
        None, description="Medication frequency (e.g., '2x/day')"
    )
    duration: Optional[str] = Field(
        None, description="Medication duration (e.g., '7 days')"
    )


# Request/Response models for API
class CreatePatientRequest(BaseModel):
    """Request model for creating a patient."""
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    sex_at_birth: Optional[str] = None


class CreateFormRequest(BaseModel):
    """Request model for creating a form."""
    patient_id: str
    doctor_id: str


class UpdateFormRequest(BaseModel):
    """Request model for updating a form."""
    status: Optional[FormStatus] = None
    free_text_notes: Optional[str] = None


class CreateSymptomRequest(BaseModel):
    """Request model for creating a symptom."""
    form_id: str
    name: str
    duration: Optional[str] = None
    intensity: Optional[str] = None
    recurrence: Optional[str] = None


class UpdateSymptomRequest(BaseModel):
    """Request model for updating a symptom."""
    name: Optional[str] = None
    duration: Optional[str] = None
    intensity: Optional[str] = None
    recurrence: Optional[str] = None


class CreateMedicationRequest(BaseModel):
    """Request model for creating a medication."""
    form_id: str
    name: str
    strength: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None


class UpdateMedicationRequest(BaseModel):
    """Request model for updating a medication."""
    name: Optional[str] = None
    strength: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None


# AI extraction models
class ExtractedEntity(BaseModel):
    """Base model for AI-extracted entities."""
    name: str
    confidence: Optional[float] = None


class ExtractedSymptom(ExtractedEntity):
    """AI-extracted symptom entity."""
    duration: Optional[str] = None
    intensity: Optional[str] = None
    recurrence: Optional[str] = None


class ExtractedMedication(ExtractedEntity):
    """AI-extracted medication entity."""
    strength: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None


class ExtractionResult(BaseModel):
    """Result of AI entity extraction from transcript."""
    symptoms: List[ExtractedSymptom] = Field(default_factory=list)
    medications: List[ExtractedMedication] = Field(default_factory=list)
    raw_text: str = Field(..., description="Original transcript text")


# =============================================================================
# Backend API Models (matching FastAPI schema)
# =============================================================================

class BackendDoctor(BaseModel):
    """Backend Doctor model matching API schema."""
    full_name: str = Field(..., description="Doctor's full name")
    email: Optional[str] = Field(None, description="Doctor's email address")
    phone: Optional[str] = Field(None, description="Doctor's phone number")
    doctor_id: str = Field(..., description="Doctor UUID")
    created_at: datetime = Field(..., description="Creation timestamp")


class BackendDoctorCreate(BaseModel):
    """Backend Doctor creation request."""
    full_name: str = Field(..., description="Doctor's full name")
    email: Optional[str] = Field(None, description="Doctor's email address")
    phone: Optional[str] = Field(None, description="Doctor's phone number")


class BackendDoctorUpdate(BaseModel):
    """Backend Doctor update request."""
    full_name: Optional[str] = Field(None, description="Doctor's full name")
    email: Optional[str] = Field(None, description="Doctor's email address")
    phone: Optional[str] = Field(None, description="Doctor's phone number")


class BackendPatient(BaseModel):
    """Backend Patient model matching API schema."""
    full_name: str = Field(..., description="Patient's full name")
    dob: Optional[date] = Field(None, description="Date of birth")
    sex_at_birth: Optional[str] = Field(None, description="Sex at birth")
    phone: Optional[str] = Field(None, description="Patient's phone number")
    email: Optional[str] = Field(None, description="Patient's email address")
    patient_id: str = Field(..., description="Patient UUID")
    created_at: datetime = Field(..., description="Creation timestamp")


class BackendPatientCreate(BaseModel):
    """Backend Patient creation request."""
    full_name: str = Field(..., description="Patient's full name")
    dob: Optional[date] = Field(None, description="Date of birth")
    sex_at_birth: Optional[str] = Field(None, description="Sex at birth")
    phone: Optional[str] = Field(None, description="Patient's phone number")
    email: Optional[str] = Field(None, description="Patient's email address")


class BackendPatientUpdate(BaseModel):
    """Backend Patient update request."""
    full_name: Optional[str] = Field(None, description="Patient's full name")
    dob: Optional[date] = Field(None, description="Date of birth")
    sex_at_birth: Optional[str] = Field(None, description="Sex at birth")
    phone: Optional[str] = Field(None, description="Patient's phone number")
    email: Optional[str] = Field(None, description="Patient's email address")


class BackendSymptomCreate(BaseModel):
    """Backend Symptom creation request."""
    name: str = Field(..., description="Symptom name")
    duration: Optional[int] = Field(None, description="Duration as integer")
    intensity: Optional[int] = Field(None, description="Intensity as integer")


class BackendMedicationCreate(BaseModel):
    """Backend Medication creation request."""
    name: str = Field(..., description="Medication name")
    strength: Optional[int] = Field(None, description="Strength as integer")


class BackendFormCreate(BaseModel):
    """Backend Form creation request."""
    patient_id: str = Field(..., description="Patient UUID")
    doctor_id: Optional[str] = Field(None, description="Doctor UUID")
    symptoms: List[BackendSymptomCreate] = Field(..., description="List of symptoms")
    medications: Optional[List[BackendMedicationCreate]] = Field(
        None, description="List of medications"
    )


# =============================================================================
# Adapter Methods
# =============================================================================

def convert_string_to_int(value: Optional[str]) -> Optional[int]:
    """Convert string to integer, handling common formats."""
    if not value:
        return None

    # Handle numeric strings
    if value.isdigit():
        return int(value)

    # Handle "X/10" format
    if "/" in value and value.split("/")[0].isdigit():
        return int(value.split("/")[0])

    # Handle text intensity mappings
    intensity_map = {
        "mild": 3,
        "moderate": 5,
        "severe": 8,
        "slight": 2,
        "minor": 2,
        "somewhat": 4,
        "bad": 7,
        "terrible": 9,
        "awful": 9
    }

    if value.lower() in intensity_map:
        return intensity_map[value.lower()]

    # Try to extract number from string
    import re
    numbers = re.findall(r'\d+', value)
    if numbers:
        return int(numbers[0])

    return None


def convert_int_to_string(value: Optional[int]) -> Optional[str]:
    """Convert integer back to string representation."""
    if value is None:
        return None
    return str(value)


# Frontend to Backend Adapters
def doctor_to_backend(doctor: Doctor) -> BackendDoctorCreate:
    """Convert frontend Doctor to backend DoctorCreate."""
    return BackendDoctorCreate(
        full_name=doctor.name,
        email=None,  # Frontend doesn't have email
        phone=None   # Frontend doesn't have phone
    )


def patient_to_backend(patient: Patient) -> BackendPatientCreate:
    """Convert frontend Patient to backend PatientCreate."""
    return BackendPatientCreate(
        full_name=patient.name,
        dob=patient.date_of_birth,
        sex_at_birth=None,  # Frontend doesn't have this field
        phone=None,         # Frontend doesn't have phone
        email=patient.email
    )


def symptom_to_backend(symptom: Symptom) -> BackendSymptomCreate:
    """Convert frontend Symptom to backend SymptomCreate."""
    return BackendSymptomCreate(
        name=symptom.name,
        duration=convert_string_to_int(symptom.duration),
        intensity=convert_string_to_int(symptom.intensity)
    )


def medication_to_backend(medication: Medication) -> BackendMedicationCreate:
    """Convert frontend Medication to backend MedicationCreate."""
    return BackendMedicationCreate(
        name=medication.name,
        strength=convert_string_to_int(medication.strength)
    )


# Backend to Frontend Adapters
def backend_doctor_to_frontend(backend_doctor: BackendDoctor) -> Doctor:
    """Convert backend Doctor to frontend Doctor."""
    return Doctor(
        id=backend_doctor.doctor_id,
        name=backend_doctor.full_name
    )


def backend_patient_to_frontend(backend_patient: BackendPatient) -> Patient:
    """Convert backend Patient to frontend Patient."""
    return Patient(
        id=backend_patient.patient_id,
        name=backend_patient.full_name,
        email=backend_patient.email,
        date_of_birth=backend_patient.dob
    )


def backend_symptom_to_frontend(
    backend_symptom: BackendSymptomCreate, form_id: str
) -> Symptom:
    """Convert backend SymptomCreate to frontend Symptom."""
    return Symptom(
        id="",  # Will be generated by frontend
        form_id=form_id,
        name=backend_symptom.name,
        duration=convert_int_to_string(backend_symptom.duration),
        intensity=convert_int_to_string(backend_symptom.intensity),
        recurrence=None  # Backend doesn't support this
    )


def backend_medication_to_frontend(
    backend_medication: BackendMedicationCreate, form_id: str
) -> Medication:
    """Convert backend MedicationCreate to frontend Medication."""
    return Medication(
        id="",  # Will be generated by frontend
        form_id=form_id,
        name=backend_medication.name,
        strength=convert_int_to_string(backend_medication.strength),
        frequency=None,  # Backend doesn't support this
        duration=None    # Backend doesn't support this
    )
