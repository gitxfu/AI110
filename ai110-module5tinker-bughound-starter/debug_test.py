from bughound_agent import BugHoundAgent
from llm_client import GroqClient

CODE = """
# TODO: Replace this with real input validation
def compute_ratio(x, y):
    print("computing ratio...")
    try:
        return x / y
    except:
        return 0
"""

def print_result(label, result):
    print(f"\n=== {label} ===")
    for issue in result["issues"]:
        print(f"  [{issue['severity']}] {issue['type']}: {issue['msg']}")
    for log in result["logs"]:
        print(f"  {log['step']}: {log['message']}")

# Offline (heuristic)
agent = BugHoundAgent(client=None)
print_result("Offline / Heuristic", agent.run(CODE))

# Groq
try:
    agent = BugHoundAgent(client=GroqClient())
    print_result("Groq", agent.run(CODE))
except Exception as e:
    print(f"\n=== Groq ===\n  ERROR: {e}")

# == = Offline / Heuristic == =
# [Low] Code Quality: Found print statements. Consider using logging for non-toy code.
# [High] Reliability: Found a bare `except: `. Catch a specific exception or use `except Exception as e: `.
# [Medium] Maintainability: Found TODO comments. Unfinished logic can hide bugs or missing cases.
# PLAN: Planning a quick scan + fix proposal workflow.
# ANALYZE: Using heuristic analyzer(offline mode).
# ANALYZE: Found 3 issue(s).
# ACT: Using heuristic fixer(offline mode).
# TEST: Risk assessed as high(score=30).
# REFLECT: Fix is not safe enough to auto-apply. Human review recommended.

# == = Groq == =
# [high] missing-validation: Function lacks input validation for numeric types(x and y could be non-numeric).
# [medium] broad-exception: Except block catches all exceptions(including non-division errors like TypeError).
# [medium] silent-failure: Returns 0 on failure without clear error indication, potentially masking critical issues.
# PLAN: Planning a quick scan + fix proposal workflow.
# ANALYZE: Using LLM analyzer.
# ANALYZE: Found 3 issue(s).
# ACT: Using LLM fixer.
# TEST: Risk assessed as high(score=15).
# REFLECT: Fix is not safe enough to auto-apply. Human review recommended.

# My findings:
# heuristics produce "High"/"Low"/"Medium" (capitalized), Groq produced "high"/"medium" (lowercase). 
# The agent accepts both because _normalize_issues just calls str(), but if anything downstream expected a specific casing, it would break.

# Heuristics catch surface-level patterns with regex. The LLM understands meaning ,it caught that returning 0 silently is a problem, which no regex could find. But it also missed the print and TODO because those weren't semantically "bugs" to the model.
