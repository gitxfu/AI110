"""Integration tests for the ingestion module — calls real Gemini embedding API."""
import os
import shutil
import pytest

# FAISS vector store written by ingest_pdf()
FAISS_DIR = "data/faiss_db"
# Real PDF used for integration tests
REAL_PDF = "data/pdfs/week8_guide.pdf"


@pytest.fixture(autouse=True)
def clean_faiss():
    """Wipe the FAISS index before and after each test for isolation."""
    if os.path.exists(FAISS_DIR):
        shutil.rmtree(FAISS_DIR)
    yield
    if os.path.exists(FAISS_DIR):
        shutil.rmtree(FAISS_DIR)


@pytest.mark.skipif(not os.path.exists(REAL_PDF), reason="week8_guide.pdf not found")
def test_ingest_real_pdf():
    """Ingest a real PDF: expect chunk count > 0 and FAISS index on disk."""
    from src.ingestion import ingest_pdf

    count = ingest_pdf(REAL_PDF)

    assert count > 0                    # chunks were created
    assert os.path.exists(FAISS_DIR)   # FAISS index was written to disk
