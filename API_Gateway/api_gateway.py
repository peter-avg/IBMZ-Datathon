import os
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, Depends, HTTPException, Response, status
# import openai
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from pydantic import BaseModel
from typing import List
from uuid import uuid4, UUID

# --- Configuration ---
load_dotenv() # <-- ADD THIS to load the .env file

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL_RAW = os.getenv("DATABASE_URL")

# --- Safety Check ---
# ADD THIS to ensure the app fails gracefully if the URL is missing
if not DATABASE_URL_RAW:
    raise ValueError("DATABASE_URL environment variable not set. Please create a .env file.")

# --- OpenAI Client Setup ---
# client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)

# --- FastAPI App ---
app = FastAPI()

# --- Pydantic Schemas ---

# Pydantic model for data coming FROM the frontend
class DoctorCreate(BaseModel):
    full_name: str

# Pydantic model for data sent back TO the frontend
class Doctor(BaseModel):
    doctor_id: UUID
    full_name: str
    class Config:
        from_attributes = True

# --- Database Setup ---
engine = create_async_engine(
    DATABASE_URL_RAW,
    echo=False, # Changed to False for cleaner production logs
    connect_args={"ssl": "require"}
)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Dependency to get a DB session
async def get_db():
    async with async_session() as session:
        yield session

# --- API Endpoints ---

# LLM REST endpoint
# @app.post("/llm/infer")
# async def llm_infer(prompt: str):
#     if not OPENAI_API_KEY:
#         raise HTTPException(status_code=500, detail="OPENAI_API_KEY environment variable not set.")
#     try:
#         response = await client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens=150
#         )
#         return {"result": response.choices[0].message.content.strip()}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
        except Exception:
            break

# REST API to interact with Postgres
@app.get("/get_doctor/", response_model=List[Doctor])
async def get_doctor(db: AsyncSession = Depends(get_db)):
    query = text("SELECT doctor_id, full_name FROM doctor")
    result = await db.execute(query)
    items = result.mappings().all()
    return items

@app.post("/create_doctor/", response_model=Doctor, status_code=201)
async def create_doctor(
    doctor_data: DoctorCreate, # FastAPI validates the incoming data against this model
    db: AsyncSession = Depends(get_db)
):
    new_doctor_id = uuid4()
    query = text("""
        INSERT INTO doctor (doctor_id, full_name)
        VALUES (:doctor_id, :full_name)
    """)
    try:
        await db.execute(
            query,
            {"doctor_id": new_doctor_id, "full_name": doctor_data.full_name}
        )
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    return {"doctor_id": new_doctor_id, "full_name": doctor_data.full_name}


@app.delete("/doctor/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(
    doctor_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    # Define the DELETE query using a named parameter
    query = text("DELETE FROM doctor WHERE doctor_id = :doctor_id")

    try:
        # Execute the query
        result = await db.execute(query, {"doctor_id": doctor_id})
        
        # Check if any row was actually deleted
        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Doctor with id {doctor_id} not found"
            )
        
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    # Return a 204 response which has no body, indicating success
    return Response(status_code=status.HTTP_204_NO_CONTENT)