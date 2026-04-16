from bughound_agent import BugHoundAgent
from llm_client import MockClient


def test_workflow_runs_in_offline_mode_and_returns_shape():
    agent = BugHoundAgent(client=None)  # heuristic-only
    code = "def f():\n    print('hi')\n    return True\n"
    result = agent.run(code)

    assert isinstance(result, dict)
    assert "issues" in result
    assert "fixed_code" in result
    assert "risk" in result
    assert "logs" in result

    assert isinstance(result["issues"], list)
    assert isinstance(result["fixed_code"], str)
    assert isinstance(result["risk"], dict)
    assert isinstance(result["logs"], list)
    assert len(result["logs"]) > 0


def test_offline_mode_detects_print_issue():
    agent = BugHoundAgent(client=None)
    code = "def f():\n    print('hi')\n    return True\n"
    result = agent.run(code)

    assert any(issue.get("type") == "Code Quality" for issue in result["issues"])


def test_offline_mode_proposes_logging_fix_for_print():
    agent = BugHoundAgent(client=None)
    code = "def f():\n    print('hi')\n    return True\n"
    result = agent.run(code)

    fixed = result["fixed_code"]
    assert "logging" in fixed
    assert "logging.info(" in fixed


def test_mock_client_forces_llm_fallback_to_heuristics_for_analysis():
    # MockClient returns non-JSON for analyzer prompts, so agent should fall back.
    agent = BugHoundAgent(client=MockClient())
    code = "def f():\n    print('hi')\n    return True\n"
    result = agent.run(code)

    assert any(issue.get("type") == "Code Quality" for issue in result["issues"])
    # Ensure we logged the fallback path
    assert any("Falling back to heuristics" in entry.get("message", "") for entry in result["logs"])


# ----------------------------
# Sample file tests (Part 4)
# ----------------------------

def test_cleanish_has_no_high_severity_issues():
    with open("sample_code/cleanish.py") as f:
        code = f.read()
    agent = BugHoundAgent(client=None)
    result = agent.run(code)
    high = [i for i in result["issues"] if i["severity"] == "High"]
    assert len(high) == 0, f"Expected no High issues on clean code, got: {high}"


def test_mixed_issues_detects_multiple_issues_and_blocks_autofix():
    with open("sample_code/mixed_issues.py") as f:
        code = f.read()
    agent = BugHoundAgent(client=None)
    result = agent.run(code)
    assert len(result["issues"]) >= 2, "Expected at least 2 issues in mixed_issues.py"
    assert result["risk"]["should_autofix"] is False


def test_flaky_try_except_detects_reliability_issue():
    with open("sample_code/flaky_try_except.py") as f:
        code = f.read()
    agent = BugHoundAgent(client=None)
    result = agent.run(code)
    reliability = [i for i in result["issues"] if i["type"] == "Reliability"]
    assert len(reliability) >= 1, "Expected a Reliability issue for bare except"
