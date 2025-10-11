from pydantic import BaseModel, Field, EmailStr
from typing import List, Literal
from datetime import date
from enum import Enum

######################################################################
#                             Error Schemas                          #
######################################################################


class ErrorMixin(BaseModel):
    error: bool = Field(
        default=False,
        description="True if there was an error \\\
            with parsing the user intent",
    )
    error_message: str | None = Field(
        default=None,
        description="A user friendly error message \\\
            to drive better user prompting",
    )


######################################################################
#                             Form Schemas                           #
######################################################################


class PatientPIISchema(BaseModel):
    name: str
    email: EmailStr
    date_of_birth: date
    error: ErrorMixin


class MedicationSchema(BaseModel):
    name: str
    strength: int = Field(..., description="Strength in mg.", gt=0)
    frequency: int = Field(..., gt=0)
    duration: int = Field(..., gt=0)
    error: ErrorMixin


class SymptomSchema(BaseModel):
    name: str = Field(..., description="amoxicillin")
    duration: int = Field(..., description="Duration in days", gt=0)
    intensity: Literal[1, 2, 3, 4, 5] = Field(..., description="Symptom intensity")
    recurrence: bool
    error: ErrorMixin


class PatientSchema(BaseModel):
    pii: PatientPIISchema | None
    medication: List[MedicationSchema] | None
    symptoms: List[SymptomSchema] | None
    error: ErrorMixin


######################################################################
#                      Info Intent Schemas                           #
######################################################################


class infoIntent(Enum):
    PII = 0
    MEDS = 1
    SYMPS = 2
    ALL = 3
    ERR = 4


class infoIntentSchema(BaseModel):
    intent: (
        List[Literal["Personally identifiable information", "Medication", "Symptoms"]]
        | None
    ) = Field(
        default=None,
        description="If you recognise that one \\\
                      or more of the literals exist in the text, please \\\
                      include them in the base model.",
    )
    error: ErrorMixin


SCHEMAS = {
    infoIntent.PII: PatientPIISchema,
    infoIntent.MEDS: MedicationSchema,
    infoIntent.SYMPS: SymptomSchema,
    infoIntent.ALL: PatientSchema,
}
