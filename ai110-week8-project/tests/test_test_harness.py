"""Tests for src/test_harness.py — mocked pipeline."""
import json
import pytest
from unittest.mock import patch


@pytest.fixture
def test_cases_file(tmp_path):
    cases = [
        {"question": "What is AI?"},
        {"question": "What is Python?"},
    ]
    path = tmp_path / "test_cases.json"
    path.write_text(json.dumps(cases))
    return str(path)


MOCK_RESULT = {
    "context_relevance": {"score": 0.8, "explanation": "ok"},
    "faithfulness": {"score": 0.8, "explanation": "ok"},
    "answer_relevance": {"score": 0.8, "explanation": "ok"},
    "keyword_overlap": 0.8,
}


@patch("src.test_harness.run_pipeline")
def test_runs_once_per_question(mock_run, test_cases_file):
    mock_run.return_value = MOCK_RESULT
    from src.test_harness import run_test_harness
    run_test_harness(test_cases_path=test_cases_file)
    assert mock_run.call_count == 2  # one call per test case


@patch("src.test_harness.run_pipeline")
def test_returns_results_and_averages(mock_run, test_cases_file):
    mock_run.return_value = MOCK_RESULT
    from src.test_harness import run_test_harness
    out = run_test_harness(test_cases_path=test_cases_file)
    assert "results" in out
    assert "averages" in out
    assert len(out["results"]) == 2


@patch("src.test_harness.run_pipeline")
def test_passes_when_scores_above_threshold(mock_run, test_cases_file):
    mock_run.return_value = MOCK_RESULT  # all scores 0.8
    from src.test_harness import run_test_harness
    out = run_test_harness(test_cases_path=test_cases_file, threshold=0.6)
    assert out["passed"] is True


@patch("src.test_harness.run_pipeline")
def test_fails_when_scores_below_threshold(mock_run, test_cases_file):
    low = {k: ({"score": 0.3, "explanation": "low"} if isinstance(v, dict) else 0.3)
           for k, v in MOCK_RESULT.items()}
    mock_run.return_value = low
    from src.test_harness import run_test_harness
    out = run_test_harness(test_cases_path=test_cases_file, threshold=0.6)
    assert out["passed"] is False
