"""Tests for src/generator.py — mocked google.genai Client API."""
import pytest
from unittest.mock import patch, MagicMock


def mock_client(mock_genai, text="Some answer."):
    """Configure mock genai.Client to return a fixed answer."""
    client = MagicMock()
    client.models.generate_content.return_value = MagicMock(text=text)
    mock_genai.Client.return_value = client
    return client


@patch("src.generator.genai")
def test_returns_non_empty_string(mock_genai):
    mock_client(mock_genai)
    from src.generator import generate_answer
    answer = generate_answer("What is AI?", "AI stands for artificial intelligence.")
    assert isinstance(answer, str) and len(answer.strip()) > 0


@patch("src.generator.genai")
def test_prompt_includes_question_and_context(mock_genai):
    client = mock_client(mock_genai, "answer")
    from src.generator import generate_answer
    generate_answer("my question", "my context")
    call_args = client.models.generate_content.call_args
    prompt = str(call_args)
    assert "my question" in prompt
    assert "my context" in prompt


@patch("src.generator.genai")
def test_api_error_propagates(mock_genai):
    client = MagicMock()
    client.models.generate_content.side_effect = Exception("API error")
    mock_genai.Client.return_value = client
    from src.generator import generate_answer
    with pytest.raises(Exception):
        generate_answer("question", "context")
