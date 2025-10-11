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
    email: Optional[str] = Field(None, description="Patient's email address")
    date_of_birth: Optional[date] = Field(None, description="Patient's date of birth")


class Form(BaseModel):
    """Clinical form entity model."""
    id: str = Field(..., description="Primary key")
    patient_id: str = Field(..., description="Foreign key to Patient")
    doctor_id: str = Field(..., description="Foreign key to Doctor")
    created_at: Optional[datetime] = Field(None, description="Form creation timestamp")
    status: FormStatus = Field(FormStatus.DRAFT, description="Form status")
    free_text_notes: Optional[str] = Field(None, description="Free text notes")


class Symptom(BaseModel):
    """Symptom entity model."""
    id: str = Field(..., description="Primary key")
    form_id: str = Field(..., description="Foreign key to Form")
    name: str = Field(..., description="Symptom name")
    duration: Optional[str] = Field(None, description="Symptom duration")
    intensity: Optional[str] = Field(
        None, description="Symptom intensity (1-10 or mild/moderate/severe)"
    )
    recurrence: Optional[str] = Field(None, description="Symptom recurrence pattern")


class Medication(BaseModel):
    """Medication entity model."""
    id: str = Field(..., description="Primary key")
    form_id: str = Field(..., description="Foreign key to Form")
    name: str = Field(..., description="Medication name")
    strength: Optional[str] = Field(None, description="Medication strength (e.g., '500 mg')")
    frequency: Optional[str] = Field(None, description="Medication frequency (e.g., '2x/day')")
    duration: Optional[str] = Field(None, description="Medication duration (e.g., '7 days')")


# Request/Response models for API
class CreatePatientRequest(BaseModel):
    """Request model for creating a patient."""
    name: str
    email: Optional[str] = None
    date_of_birth: Optional[date] = None


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

