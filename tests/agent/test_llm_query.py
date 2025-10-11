import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from pydantic import BaseModel, ValidationError

import agent.utils as llm


class MockResponse(BaseModel):
    text: str


@pytest.mark.asyncio 
async def test_llm_query_function():
    mock_client = MagicMock()
    mock_response = MockResponse(text="Hello OpenAI")
    mock_client.chat.completions.create = AsyncMock(
        return_value=mock_response
    )

    result = await llm.query_llm("hello", mock_response)

    assert result.text == "Hello OpenAI"


@pytest.mark.asyncio
async def test_llm_call_with_openai_model():
    mock_client = MagicMock()
    mock_response = MockResponse(text="Hello OpenAI")
    mock_client.chat.completions.create = AsyncMock(
        return_value=mock_response
    )

    result = await llm.LLM_CALL(
        response_model=MockResponse,
        model="gpt-4o-mini",
        client=mock_client,
        content="Hi there!",
    )

    mock_client.chat.completions.create.assert_awaited_once()
    assert isinstance(result, MockResponse)
    assert result.text == "Hello OpenAI"


@pytest.mark.asyncio
async def test_llm_call_fallable_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.chat.completions.create = AsyncMock(
        return_value=MockResponse(text="Success")
    )

    mock_conf_client = MagicMock()
    mock_conf_client.model = "gpt-4o-mini"
    mock_conf_client.client = mock_client

    monkeypatch.setattr(llm.conf, "CLIENTS", [mock_conf_client])

    result = await llm.LLM_CALL_FALLABLE(MockResponse, "Hi there!")
    assert isinstance(result, MockResponse)
    assert result.text == "Success"
