import os
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, Depends, HTTPException
# import openai
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from pydantic import BaseModel
from typing import List
from uuid import UUID

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
class Item(BaseModel):
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
@app.get("/doctor/", response_model=List[Item])
async def read_items(db: AsyncSession = Depends(get_db)):
    query = text("SELECT doctor_id, full_name FROM doctor")
    result = await db.execute(query)
    items = result.mappings().all()
    return items