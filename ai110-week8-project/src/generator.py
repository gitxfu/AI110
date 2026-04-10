"""Generator module for RAG pipeline."""
import os
from google import genai


def generate_answer(question: str, context: str) -> str:
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    prompt = (
        "Answer the question based only on the provided context. "
        "If the context does not contain enough information, say you don't have enough information.\n\n"
        f"Context: {context}\n\n"
        f"Question: {question}"
    )
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        contents=prompt,
    )
    return response.text or ""
