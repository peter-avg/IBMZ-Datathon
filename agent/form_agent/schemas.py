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
    name: str | None
    email: EmailStr | None
    date_of_birth: date | None
    error: ErrorMixin | None


class MedicationSchema(BaseModel):
    name: str | None
    strength: int | None = Field(..., description="Strength in mg.", gt=0)
    frequency: int | None = Field(..., gt=0)
    duration: int | None = Field(..., gt=0)


class SymptomSchema(BaseModel):
    name: str | None = Field(..., description="amoxicillin")
    duration: int | None = Field(..., description="Duration in days", gt=0)
    intensity: Literal[1, 2, 3, 4, 5] | None = Field(..., description="Symptom intensity")
    recurrence: bool | None


class ListMedicationSchema(BaseModel):
    meds: List[MedicationSchema]
    error: ErrorMixin | None


class ListSymptomSchema(BaseModel):
    symps: List[SymptomSchema]
    error: ErrorMixin | None


class PatientSchema(BaseModel):
    pii: PatientPIISchema | None = None
    medication: ListMedicationSchema | None = None
    symptoms: ListSymptomSchema | None = None
    error: ErrorMixin | None = None


class RecommendationSchema(BaseModel):
    recommendation: str | None = None
    error: ErrorMixin | None = None


######################################################################
#                      Info Intent Schemas                           #
######################################################################


class infoIntent(Enum):
    PII = 0
    MEDS = 1
    SYMPS = 2
    ALL = 3
    ERR = 4
    CONT = 5
    REC = 6


INTENT_LITERALS = ["Personally identifiable information", "Medication", "Symptoms"]


class InfoIntentSchema(BaseModel):
    intents: List[Literal["Personally identifiable information", "Medication", "Symptoms"]] | None = Field(
        default=None,
        description="If you recognise that one \\\
                      or more of the literals exist in the text, please \\\
                      include them in the base model.",
    )
    error: ErrorMixin | None

    def to_ii(self, intent: str) -> infoIntent:
        if intent == INTENT_LITERALS[0]:
            return infoIntent.PII

        if intent == INTENT_LITERALS[1]:
            return infoIntent.MEDS

        if intent == INTENT_LITERALS[2]:
            return infoIntent.SYMS

        return infoIntent.ERR


SCHEMAS = {
    infoIntent.PII: PatientPIISchema,
    infoIntent.MEDS: ListMedicationSchema,
    infoIntent.SYMPS: ListSymptomSchema,
    infoIntent.ALL: PatientSchema,
    infoIntent.ERR: ErrorMixin,
    infoIntent.CONT: InfoIntentSchema,
    infoIntent.REC: RecommendationSchema
}
