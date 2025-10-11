"""Configuration utilities for the Clinical Forms application."""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration."""
    
    # Backend API configuration
    BACKEND_API_URL: str = os.getenv("BACKEND_API_URL", "http://localhost:8000")
    
    # Default doctor for demo
    DEFAULT_DOCTOR_ID: str = os.getenv("DEFAULT_DOCTOR_ID", "D001")
    DEFAULT_DOCTOR_NAME: str = os.getenv("DEFAULT_DOCTOR_NAME", "Dr. Demo")
    
    # AI/ASR configuration
    ASR_MODEL: str = os.getenv("ASR_MODEL", "whisper-small")
    AI_AUTOFILL_ENABLED: bool = os.getenv("AI_AUTOFILL_ENABLED", "true").lower() == "true"
    
    # Audio configuration
    AUDIO_SAMPLE_RATE: int = int(os.getenv("AUDIO_SAMPLE_RATE", "16000"))
    AUDIO_CHUNK_SIZE: int = int(os.getenv("AUDIO_CHUNK_SIZE", "1024"))
    
    # UI configuration
    PATIENTS_PER_PAGE: int = int(os.getenv("PATIENTS_PER_PAGE", "12"))
    TRANSCRIPT_MAX_LINES: int = int(os.getenv("TRANSCRIPT_MAX_LINES", "50"))
    
    # Development settings
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    MOCK_API: bool = os.getenv("MOCK_API", "true").lower() == "true"


# Global config instance
config = Config()

