import pytest
from pydantic import ValidationError
from datetime import date
from unittest.mock import AsyncMock

import agent.form_agent.schemas as schemas
from agent.form_agent.utils import PatientFormBuilder
from agent.form_agent.schemas import infoIntent as ii


class TestSchemas:
    def test_patient_pii_schema_valid(self):
        pii = schemas.PatientPIISchema(
            name="Alice",
            email="alice@example.com",
            date_of_birth=date(1990, 1, 1),
            error=None
        )
        assert pii.name == "Alice"
        assert pii.email == "alice@example.com"

    def test_medication_schema_invalid_strength(self):
        with pytest.raises(ValidationError):
            schemas.MedicationSchema(
                name="Amoxicillin",
                strength=-10,
                frequency=2,
                duration=7
            )

    def test_symptom_schema_valid(self):
        symptom = schemas.SymptomSchema(
            name="headache",
            duration=3,
            intensity=2,
            recurrence=False
        )
        assert symptom.name == "headache"
        assert symptom.intensity == 2


@pytest.mark.asyncio
class TestPatientFormBuilder:

    @pytest.fixture
    def builder(self):
        return PatientFormBuilder()

    @pytest.mark.asyncio
    async def test_contains_detects_intents(self, builder, monkeypatch):
        # Mock the query_llm function
        monkeypatch.setattr("agent.form_agent.utils.query_llm", AsyncMock())
        mock_response = schemas.InfoIntentSchema(intents=["Medication", "Symptoms"])
        builder._contains = AsyncMock(return_value={ii.MEDS: True, ii.SYMPS: True, ii.PII: False})

        result = await builder._contains("I take meds and have headaches")
        assert result[ii.MEDS] is True
        assert result[ii.SYMPS] is True
        assert result[ii.PII] is False

