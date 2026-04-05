"""Shared fixtures and setup for RAG pipeline tests."""
from dotenv import load_dotenv

# Load .env so GOOGLE_API_KEY is available for real API tests
load_dotenv()
