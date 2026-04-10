"""Streamlit UI for the Multi-Document RAG Evaluator."""
import os
import tempfile
import shutil

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from src.ingestion import ingest_pdf
from src.retriever import retrieve
from src.generator import generate_answer
from src.evaluator import (
    context_relevance,
    faithfulness,
    answer_relevance,
    embedding_similarity,
    keyword_overlap,
)
from src.test_harness import run_test_harness

st.set_page_config(page_title="RAG Evaluator", layout="wide")
st.title("Multi-Document RAG Evaluator")

# ── Session state defaults ──────────────────────────────────────────
if "uploaded_docs" not in st.session_state:
    st.session_state.uploaded_docs = []

# ── Sidebar ─────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Indexed Documents")
    if st.session_state.uploaded_docs:
        for doc in st.session_state.uploaded_docs:
            st.write(f"- {doc['name']} ({doc['chunks']} chunks)")
    else:
        st.write("No documents indexed yet.")

    if st.button("Clear All"):
        db_path = "data/faiss_db"
        if os.path.exists(db_path):
            shutil.rmtree(db_path)
        st.session_state.uploaded_docs = []
        st.rerun()

# ── 1. Upload Section ──────────────────────────────────────────────
st.header("1. Upload PDFs")
uploaded_files = st.file_uploader(
    "Upload one or more PDF files",
    type=["pdf"],
    accept_multiple_files=True,
)

if uploaded_files:
    for uf in uploaded_files:
        already = any(d["name"] == uf.name for d in st.session_state.uploaded_docs)
        if already:
            continue
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uf.read())
            tmp_path = tmp.name
        try:
            with st.spinner(f"Ingesting {uf.name}..."):
                chunk_count = ingest_pdf(tmp_path)
            st.session_state.uploaded_docs.append(
                {"name": uf.name, "chunks": chunk_count}
            )
            st.success(f"{uf.name} — {chunk_count} chunks indexed")
        except Exception as e:
            st.error(f"Failed to ingest {uf.name}: {e}")
        finally:
            os.unlink(tmp_path)

# ── 2. Ask Section ──────────────────────────────────────────────────
st.header("2. Ask a Question")
question = st.text_input("Enter your question")

if question:
    # Phase 1: generate answer
    try:
        with st.spinner("Retrieving and generating answer..."):
            docs = retrieve(question)
            chunk_texts = [doc.page_content for doc in docs]
            context_str = "\n\n".join(chunk_texts)
            answer = generate_answer(question, context_str)
        st.subheader("Answer")
        st.write(answer)
    except Exception as e:
        st.error(f"Generation failed: {e}")
        answer = None

    # Phase 2: evaluation metrics
    if answer:
        METRIC_INFO = {
            "context_relevance": "How relevant the retrieved chunks are to the question.",
            "faithfulness": "Whether the answer is supported by the retrieved context.",
            "answer_relevance": "How directly the answer addresses the question.",
            "embedding_similarity": "Cosine similarity between answer and context embeddings.",
            "keyword_overlap": "Fraction of question keywords found in retrieved context.",
        }

        with st.status("Evaluating...", expanded=True) as status:
            try:
                scores = {
                    "context_relevance": context_relevance(question, chunk_texts),
                    "faithfulness": faithfulness(answer, chunk_texts),
                    "answer_relevance": answer_relevance(question, answer),
                    "embedding_similarity": embedding_similarity(answer, chunk_texts),
                    "keyword_overlap": keyword_overlap(question, chunk_texts),
                }
                status.update(label="Evaluation complete", state="complete")
            except Exception as e:
                status.update(label="Evaluation failed", state="error")
                st.error(f"Evaluation error: {e}")
                scores = None

        if scores:
            st.subheader("Evaluation Scores")
            for metric, value in scores.items():
                if isinstance(value, dict):
                    score = value.get("score")
                else:
                    score = value

                if score is None:
                    color = "red"
                    label = "N/A"
                elif score < 0.4:
                    color = "red"
                    label = f"{score:.2f}"
                elif score < 0.7:
                    color = "orange"
                    label = f"{score:.2f}"
                else:
                    color = "green"
                    label = f"{score:.2f}"

                with st.expander(f":{color}[{label}] — {metric}"):
                    st.write(METRIC_INFO[metric])
                    if isinstance(value, dict) and "explanation" in value:
                        st.write(f"**LLM explanation:** {value['explanation']}")

# ── 3. Test Harness Section ─────────────────────────────────────────
st.header("3. Batch Evaluation")
if st.button("Run Test Harness"):
    try:
        with st.spinner("Running test harness..."):
            harness_result = run_test_harness()

        averages = harness_result["averages"]
        passed = harness_result["passed"]

        if passed:
            st.success("PASSED — all average scores meet threshold")
        else:
            st.error("FAILED — some average scores below threshold")

        st.subheader("Average Scores")
        avg_data = {k: (f"{v:.3f}" if v is not None else "N/A") for k, v in averages.items()}
        st.table(avg_data)

        st.subheader("Per-Question Results")
        dict_metrics = {"context_relevance", "faithfulness", "answer_relevance"}
        table_rows = []
        for r in harness_result["results"]:
            row = {"question": r["question"]}
            for m in averages:
                val = r[m]
                if m in dict_metrics:
                    s = val.get("score") if isinstance(val, dict) else val
                else:
                    s = val
                row[m] = f"{s:.3f}" if s is not None else "N/A"
            table_rows.append(row)
        st.table(table_rows)

    except Exception as e:
        st.error(f"Test harness failed: {e}")
