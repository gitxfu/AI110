"""Run the test harness from the project root and print a formatted report.

Usage:
    python run_harness.py
"""
from dotenv import load_dotenv
load_dotenv()

from src.test_harness import run_test_harness, _print_report, THRESHOLD

output = run_test_harness()
_print_report(output, THRESHOLD)
