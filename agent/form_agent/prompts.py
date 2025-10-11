from agent.form_agent.schemas import infoIntent as intent


def get_patient_PII_prompt(text: str) -> str:
    return f"""
        Extract any personally identifiable information from \\\
            the following text:\n{text}
    """


def get_patient_medication_prompt(text: str) -> str:
    return f"""
        Extract medications mentioned in the following text:\n{text}
    """


def get_patient_symptoms_prompt(text: str) -> str:
    return f"""
        Extract symptoms mentioned in the following text:\n{text}
    """


PROMPTS = {
    intent.PII: get_patient_PII_prompt,
    intent.MEDS: get_patient_medication_prompt,
    intent.SYMPS: get_patient_symptoms_prompt,
}
