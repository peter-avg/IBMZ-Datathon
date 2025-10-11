from pydantic import BaseModel, cast
from dataclasses import dataclass

from agent.form_agent.schemas import InfoIntentSchema as ii_schema
from agent.form_agent.schemas import infoIntent as ii
from agent.form_agent.schemas import INTENT_LITERALS
import agent.form_agent.schemas as schemas
import agent.form_agent.prompts as prompts

from agent.utils import query_llm
from agent.errors import errors


@dataclass
class PatientFormBuilder:
    def _contains(self, text: str) -> dict[ii, bool]:
        prompt = prompts.PROMPTS[ii.CONT](text)
        schema = schemas.SCHEMAS[ii.CONT]
        resp = query_llm(prompt, schema)

        detected = set(resp.intents or [])
        return {ii_schema().to_ii(intent): (intent in detected) for intent in INTENT_LITERALS}

    def get_info(intent: ii, text: str) -> BaseModel:
        prompt = prompts.PROMPTS[intent](text)
        schema = schemas.SCHEMAS[intent]
        resp = query_llm(prompt, schema)

        typed_resp = cast(schema, resp)

        if typed_resp.error.error:
            raise errors.LLMError(typed_resp.error.error_message)

        return typed_resp

    def get_patient_form(self, text: str) -> schemas.PatientSchema:
        info = {ii.PII: None, ii.MEDS: None, ii.SYMPS: None}

        for intent, cond in self._contains(text):
            if cond:
                info[intent] = self.get_info(intent)

        return schemas.PatientSchema(pii=info[ii.PII], medication=info[ii.MEDS], symptoms=info[ii.SYMPS])
