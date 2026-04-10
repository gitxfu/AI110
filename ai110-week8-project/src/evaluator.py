"""RAG evaluation metrics — LLM-as-judge and heuristic."""
import json
import math

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "shall",
    "should", "may", "might", "must", "can", "could", "am", "in", "on",
    "at", "to", "for", "of", "with", "by", "from", "as", "into", "about",
    "between", "through", "during", "before", "after", "above", "below",
    "and", "but", "or", "nor", "not", "so", "yet", "both", "either",
    "neither", "each", "every", "all", "any", "few", "more", "most",
    "other", "some", "such", "no", "only", "own", "same", "than", "too",
    "very", "just", "because", "if", "when", "where", "how", "what",
    "which", "who", "whom", "this", "that", "these", "those", "i", "me",
    "my", "myself", "we", "our", "ours", "you", "your", "he", "him",
    "his", "she", "her", "it", "its", "they", "them", "their",
}


def _llm_judge(prompt: str) -> dict:
    """Call Gemini and parse JSON response. Return fallback on error."""
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview")
        response = llm.invoke(prompt)
        # gemini-3.1 returns content as a list of dicts: [{"type": "text", "text": "..."}]
        # older models return a plain string
        raw = response.content
        if isinstance(raw, list):
            content = next((b["text"] for b in raw if b.get("type") == "text"), "")
        else:
            content = raw
        # Strip markdown code fences if present (e.g. ```json ... ```)
        content = content.strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        result = json.loads(content.strip())
        return result
    except Exception:
        return {"score": None, "explanation": "Evaluation failed"}


def context_relevance(question: str, chunks: list[str]) -> dict:
    prompt = (
        "Rate from 0 to 1 how relevant the following context chunks are to the question. "
        "Return ONLY valid JSON: {\"score\": <float>, \"explanation\": <string>}\n\n"
        f"Question: {question}\n\nContext chunks:\n" + "\n".join(chunks)
    )
    return _llm_judge(prompt)


def faithfulness(answer: str, chunks: list[str]) -> dict:
    prompt = (
        "Rate from 0 to 1 whether the following answer is fully supported by the context chunks. "
        "Return ONLY valid JSON: {\"score\": <float>, \"explanation\": <string>}\n\n"
        f"Answer: {answer}\n\nContext chunks:\n" + "\n".join(chunks)
    )
    return _llm_judge(prompt)


def answer_relevance(question: str, answer: str) -> dict:
    prompt = (
        "Rate from 0 to 1 how directly the answer addresses the question. "
        "Return ONLY valid JSON: {\"score\": <float>, \"explanation\": <string>}\n\n"
        f"Question: {question}\n\nAnswer: {answer}"
    )
    return _llm_judge(prompt)


def embedding_similarity(text: str, texts: list[str]) -> float:
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    answer_vec = embeddings.embed_query(text)
    context_vec = embeddings.embed_documents(texts)[0]

    dot = sum(a * b for a, b in zip(answer_vec, context_vec))
    mag_a = math.sqrt(sum(a * a for a in answer_vec))
    mag_b = math.sqrt(sum(b * b for b in context_vec))

    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def keyword_overlap(question: str, chunks: list[str]) -> float:
    tokens = [w.lower() for w in question.split() if w.lower() not in STOPWORDS]
    if not tokens:
        return 0.0
    context_text = " ".join(chunks).lower()
    matched = sum(1 for t in tokens if t in context_text)
    return matched / len(tokens)
