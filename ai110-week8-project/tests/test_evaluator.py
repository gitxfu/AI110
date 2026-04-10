"""Tests for src/evaluator.py — all metrics, mocked LLM/embeddings."""
import json
import pytest
from unittest.mock import patch


def llm_response(mock_cls, score, explanation="ok"):
    """Helper to configure a mock LLM to return a JSON score response."""
    mock_cls.return_value.invoke.return_value.content = json.dumps(
        {"score": score, "explanation": explanation}
    )


# ---------------------------------------------------------------------------
# LLM-as-judge metrics (context_relevance, faithfulness, answer_relevance)
# ---------------------------------------------------------------------------

@patch("src.evaluator.ChatGoogleGenerativeAI")
def test_context_relevance_returns_score(mock_cls):
    llm_response(mock_cls, 0.85)
    from src.evaluator import context_relevance
    result = context_relevance("What is AI?", ["AI is a field of computer science."])
    assert 0.0 <= result["score"] <= 1.0
    assert "explanation" in result


@patch("src.evaluator.ChatGoogleGenerativeAI")
def test_faithfulness_returns_score(mock_cls):
    llm_response(mock_cls, 0.9)
    from src.evaluator import faithfulness
    result = faithfulness("AI is great.", ["AI is a great technology."])
    assert 0.0 <= result["score"] <= 1.0
    assert "explanation" in result


@patch("src.evaluator.ChatGoogleGenerativeAI")
def test_answer_relevance_returns_score(mock_cls):
    llm_response(mock_cls, 0.88)
    from src.evaluator import answer_relevance
    result = answer_relevance("What is AI?", "AI is artificial intelligence.")
    assert 0.0 <= result["score"] <= 1.0
    assert "explanation" in result


@patch("src.evaluator.ChatGoogleGenerativeAI")
def test_malformed_json_returns_fallback(mock_cls):
    # LLM returns garbage — should not crash, score should be None
    mock_cls.return_value.invoke.return_value.content = "NOT VALID JSON {{"
    from src.evaluator import context_relevance
    result = context_relevance("q", ["c"])
    assert result["score"] is None
    assert isinstance(result["explanation"], str)


# ---------------------------------------------------------------------------
# Embedding cosine similarity
# ---------------------------------------------------------------------------

@patch("src.evaluator.GoogleGenerativeAIEmbeddings")
def test_embedding_similarity_identical_texts(mock_cls):
    # Same vector for both → cosine similarity should be 1.0
    vec = [0.5, 0.5, 0.5]
    mock_cls.return_value.embed_query.return_value = vec
    mock_cls.return_value.embed_documents.return_value = [vec]
    from src.evaluator import embedding_similarity
    score = embedding_similarity("same text", ["same text"])
    assert score >= 0.99


@patch("src.evaluator.GoogleGenerativeAIEmbeddings")
def test_embedding_similarity_orthogonal_texts(mock_cls):
    # Orthogonal vectors → cosine similarity should be 0.0
    mock_cls.return_value.embed_query.return_value = [1.0, 0.0, 0.0]
    mock_cls.return_value.embed_documents.return_value = [[0.0, 1.0, 0.0]]
    from src.evaluator import embedding_similarity
    score = embedding_similarity("apples", ["quantum physics"])
    assert score <= 0.1


# ---------------------------------------------------------------------------
# Keyword overlap (pure heuristic — no mocks needed)
# ---------------------------------------------------------------------------

def test_keyword_overlap_full_match():
    from src.evaluator import keyword_overlap
    # All content keywords present in chunks
    score = keyword_overlap("neural network training", ["neural network training data"])
    assert score == pytest.approx(1.0)


def test_keyword_overlap_no_match():
    from src.evaluator import keyword_overlap
    score = keyword_overlap("quantum physics", ["cooking recipes for pasta"])
    assert score == pytest.approx(0.0)


def test_keyword_overlap_stopwords_excluded():
    from src.evaluator import keyword_overlap
    # "the", "is", "a" are stopwords — only "cat" is a real token
    score = keyword_overlap("the cat is a", ["the cat sits on a mat"])
    assert score > 0.0  # "cat" matched
