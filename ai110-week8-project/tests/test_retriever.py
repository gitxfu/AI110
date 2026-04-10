"""Integration test for the retriever module — calls real Gemini embedding API."""
import os
import shutil
import pytest

FAISS_DIR = "data/faiss_db"
REAL_PDF = "data/pdfs/week8_guide.pdf"


@pytest.fixture(scope="module")
def indexed_pdf():
    """Ingest the real PDF once for all retriever tests, then clean up."""
    if not os.path.exists(REAL_PDF):
        pytest.skip("week8_guide.pdf not found")
    if os.path.exists(FAISS_DIR):
        shutil.rmtree(FAISS_DIR)
    from src.ingestion import ingest_pdf
    ingest_pdf(REAL_PDF)
    yield
    if os.path.exists(FAISS_DIR):
        shutil.rmtree(FAISS_DIR)


def test_retrieve_returns_relevant_chunks(indexed_pdf):
    """Query the real FAISS index and expect non-empty results with content."""
    from src.retriever import retrieve

    results = retrieve("What are the main deliverables?", k=4)

    assert len(results) > 0                        # got results
    assert all(hasattr(r, "page_content") for r in results)  # each has text
    assert all(len(r.page_content) > 0 for r in results)     # text is non-empty
