from dataclasses import dataclass
from pydantic import BaseModel
from typing import cast, Type

from agent.form_agent.schemas import infoIntent as ii
from agent.form_agent.schemas import INTENT_LITERALS
import agent.form_agent.schemas as schemas
import agent.form_agent.prompts as prompts

from agent.utils import query_llm
from agent.errors import error


def from_str(intent: str) -> Type[ii]:
    if intent == INTENT_LITERALS[0]:
        return ii.PII

    if intent == INTENT_LITERALS[1]:
        return ii.MEDS

    if intent == INTENT_LITERALS[2]:
        return ii.SYMPS

    return ii.ERR


@dataclass
class PatientFormBuilder:
    async def _contains(self, text: str) -> dict[ii, bool]:
        prompt = prompts.PROMPTS[ii.CONT](text)
        schema = schemas.SCHEMAS[ii.CONT]
        resp = await query_llm(prompt, schema)

        detected = []
        for intent in resp.intents:
            if intent is not None:
                detected.append(intent)

        return {from_str(intent): (intent in detected) for intent in INTENT_LITERALS}

    async def get_info(self, intent: ii, text: str) -> BaseModel:
        prompt = prompts.PROMPTS[intent](text)
        schema = schemas.SCHEMAS[intent]
        resp = await query_llm(prompt, schema)

        typed_resp = cast(schema, resp)

        if typed_resp.error is not None:
            if typed_resp.error.error:
                raise error.LLMError(typed_resp.error.error_message)

        return typed_resp

    async def get_patient_form(self, text: str) -> schemas.PatientSchema:
        info = {ii.PII: None, ii.MEDS: None, ii.SYMPS: None}

        contains_results = await self._contains(text)
        for intent, cond in contains_results.items():
            if cond:
                if intent is not None:
                    info[intent] = await self.get_info(intent, text)

        pii = info[ii.PII]
        meds = info[ii.MEDS]
        symps = info[ii.SYMPS]

        breakpoint()

        res = schemas.PatientSchema(
            pii=pii,
            medication=meds,
            symptoms=symps
        )

        return res

    async def get_patient_recommendation(
            self,
            form: str
    ) -> schemas.RecommendationSchema:
        prompt = prompts.PROMPTS[ii.REC](form)
        schema = schemas.SCHEMAS[ii.REC]

        resp = await query_llm(prompt, schema)

        return resp
