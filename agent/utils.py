from pydantic import BaseModel, ValidationError, cast
from instructor import Instructor
from typing import Type

import agent.errors as errors
import config as conf


def query_llm(prompt: str, schema: BaseModel) -> BaseModel:
    resp = LLM_CALL_FALLABLE(schema, prompt)

    typed_resp = cast(schema, resp)

    if typed_resp.error.error:
        raise errors.LLMError(typed_resp.error.error_message)

    return typed_resp


async def LLM_CALL(
    response_model: Type[BaseModel],
    model: str | None,
    client: Instructor,
    content: str,
) -> BaseModel:
    if model == conf.GEMINI:
        return client.chat.completions.create(
            messages=[{"role": "user", "content": content}],
            response_model=response_model,
        )

    return client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": content}],
        response_model=response_model,
    )


async def LLM_CALL_FALLABLE(
    response_model: Type[BaseModel],
    content: str,
) -> BaseModel:
    for client in conf.CLIENTS:
        try:
            return await LLM_CALL(response_model, client.model, client.client, content)
        except ValidationError as e:
            print(str(e))
    raise RuntimeError("No model managed to get a validated response")
