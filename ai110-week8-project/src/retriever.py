"""Retriever module for RAG pipeline."""
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

FAISS_DIR = "data/faiss_db"


def retrieve(query: str, k: int = 4) -> list:
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    db = FAISS.load_local(FAISS_DIR, embeddings, allow_dangerous_deserialization=True)
    return db.similarity_search(query, k=k)
