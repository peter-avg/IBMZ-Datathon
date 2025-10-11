from agent.form_agent.schemas import PatientSchema, RecommendationSchema
from agent.form_agent.utils import PatientFormBuilder
from fastapi import FastAPI

app = FastAPI()

builder = PatientFormBuilder()


@app.get("/get_form/", response_model=PatientSchema)
async def get_form(text: str):
    form = await builder.get_patient_form(text)

    return form


@app.get("/get_recommendation/", response_model=RecommendationSchema) 
async def get_recommendation(text: str):
    recommendation = await builder.get_patient_recommendation(text)

    return recommendation
