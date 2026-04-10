"""RAG evaluation test harness — runs pipeline over test cases and aggregates scores.

Usage:
    python -m src.test_harness
"""
import json

from src.evaluator import (
    context_relevance,
    faithfulness,
    answer_relevance,
    keyword_overlap,
)

METRICS = ["context_relevance", "faithfulness", "answer_relevance", "keyword_overlap"]
DICT_METRICS = {"context_relevance", "faithfulness", "answer_relevance"}
THRESHOLD = 0.6


def run_pipeline(question: str) -> dict:
    """Run the full RAG pipeline and evaluate all metrics for a single question."""
    from src.retriever import retrieve
    from src.generator import generate_answer

    chunks = retrieve(question)
    chunk_texts = [c.page_content for c in chunks]
    context = "\n\n".join(chunk_texts)
    answer = generate_answer(question, context)

    return {
        "answer": answer,
        "context_relevance": context_relevance(question, chunk_texts),
        "faithfulness": faithfulness(answer, chunk_texts),
        "answer_relevance": answer_relevance(question, answer),
        "keyword_overlap": keyword_overlap(question, chunk_texts),
    }


def run_test_harness(test_cases_path: str = None, threshold: float = THRESHOLD) -> dict:
    """Load test cases, run pipeline for each, compute averages, and determine pass/fail."""
    if test_cases_path is None:
        test_cases_path = "data/test_cases.json"

    with open(test_cases_path, "r") as f:
        test_cases = json.load(f)

    results = []
    for case in test_cases:
        question = case["question"]
        pipeline_result = run_pipeline(question)
        entry = {"question": question}
        entry.update(pipeline_result)
        results.append(entry)

    # Compute averages
    averages = {}
    for m in METRICS:
        scores = []
        for r in results:
            val = r[m]
            s = val.get("score") if m in DICT_METRICS else val
            if s is not None:
                scores.append(s)
        averages[m] = sum(scores) / len(scores) if scores else None

    passed = all(
        averages[m] is not None and averages[m] >= threshold for m in METRICS
    )

    return {"results": results, "averages": averages, "passed": passed}


def _score_symbol(score, threshold):
    if score is None:
        return "❓"
    return "✅" if score >= threshold else "❌"


def _print_report(output: dict, threshold: float):
    results = output["results"]
    averages = output["averages"]

    print(f"\n{'='*60}")
    print(f"  RAG Evaluation — {len(results)} test cases  (threshold: {threshold})")
    print(f"{'='*60}\n")

    for i, r in enumerate(results, 1):
        print(f"[{i}/{len(results)}] {r['question']}")
        print(f"  Answer: {r['answer'][:120].strip()}...")
        for m in METRICS:
            val = r[m]
            s = val.get("score") if m in DICT_METRICS else val
            sym = _score_symbol(s, threshold)
            print(f"  {m:<24} {sym}  {f'{s:.2f}' if s is not None else 'N/A'}")
        print()

    print(f"{'='*60}")
    print("  SUMMARY")
    print(f"{'='*60}")
    for m in METRICS:
        avg = averages[m]
        sym = _score_symbol(avg, threshold)
        print(f"  {m:<24} avg: {f'{avg:.2f}' if avg is not None else 'N/A'}  {sym}")
    print(f"\n  Overall: {'PASS ✅' if output['passed'] else 'FAIL ❌'}")
    print(f"{'='*60}\n")


