"""PDF ingestion module for RAG pipeline."""
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

FAISS_DIR = "data/faiss_db"


def ingest_pdf(file_path: str) -> int:
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    if not pages:
        return 0
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(pages)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    if os.path.exists(FAISS_DIR):
        db = FAISS.load_local(FAISS_DIR, embeddings, allow_dangerous_deserialization=True)
        db.add_documents(chunks)
    else:
        db = FAISS.from_documents(documents=chunks, embedding=embeddings)
    db.save_local(FAISS_DIR)
    return len(chunks)
