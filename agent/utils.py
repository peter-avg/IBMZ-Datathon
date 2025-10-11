from pydantic import BaseModel, ValidationError
from instructor import Instructor
from typing import Type

import agent.config as conf


async def query_llm(prompt: str, schema: BaseModel) -> BaseModel:
    resp = await LLM_CALL_FALLABLE(schema, prompt)

    return resp


async def LLM_CALL(
    response_model: Type[BaseModel],
    model: str | None,
    client: Instructor,
    content: str,
) -> BaseModel:
    if model == conf.GEMINI:
        return await client.chat.completions.create(
            messages=[{"role": "user", "content": content}],
            response_model=response_model,
        )

    return await client.chat.completions.create(
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
