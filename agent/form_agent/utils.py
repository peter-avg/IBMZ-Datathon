from dataclasses import dataclass
from pydantic import BaseModel

from agent.form_agent.schemas import infoIntent as ii
import agent.form_agent.schemas as schemas
import agent.form_agent.prompts as prompts

from agent.utils import query_llm


@dataclass
class PatientFormBuilder:
    def _contains_PII(self, text: str) -> bool:
        import re

        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        date_pattern = r"\b\d{4}-\d{2}-\d{2}\b|\b\d{2}/\d{2}/\d{4}\b"
        return bool(re.search(email_pattern, text) or re.search(date_pattern, text))

    def _contains_medications(self, text: str) -> bool:
        KNOWN_MEDS = ["paracetamol", "ibuprofen", "amoxicillin", "metformin"]
        text_lower = text.lower()
        return any(med in text_lower for med in KNOWN_MEDS)

    def _contains_symptoms(self, text: str) -> bool:
        KNOWN_SYMPTOMS = ["fever", "cough", "headache", "fatigue", "nausea"]
        text_lower = text.lower()
        return any(symptom in text_lower for symptom in KNOWN_SYMPTOMS)

    CONTAINS = {
        ii.PII: _contains_PII,
        ii.MEDS: _contains_medications,
        ii.SYMPS: _contains_symptoms,
    }

    def get_info(intent: ii, text: str) -> BaseModel:
        prompt = prompts.PROMPTS[intent](text)
        schema = schemas.SCHEMAS[intent]
        resp = query_llm(prompt, schema)

        return resp

    def get_patient_form(self, text: str) -> schemas.PatientSchema:
        info = {ii.PII: None, ii.MEDS: None, ii.SYMPS: None}

        for intent, check_func in self.CONTAINS.keys():
            if check_func(text):
                info[intent] = self.get_info(intent)

        return schemas.PatientSchema(
            pii=info[ii.PII], medication=info[ii.MEDS], symptoms=info[ii.SYMPS]
        )
