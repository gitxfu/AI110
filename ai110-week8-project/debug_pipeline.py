from src.evaluator import context_relevance, faithfulness, answer_relevance, keyword_overlap
from src.generator import generate_answer
from src.retriever import retrieve
from src.ingestion import ingest_pdf
from dotenv import load_dotenv
load_dotenv()

# 1. Ingest
count = ingest_pdf("data/pdfs/week8_guide.pdf")
print(f"[ingestion] chunks: {count}")

# 2. Retrieve
chunks = retrieve("What are the main deliverables?", k=4)
print(f"[retriever] got {len(chunks)} chunks")
for i, c in enumerate(chunks):
    print(f"  chunk {i}: {c.page_content[:80]}...")

# 3. Generate
context = "\n\n".join(c.page_content for c in chunks)
answer = generate_answer("What are the main deliverables?", context)
print(f"[generator] answer: {answer[:200]}")

# 4. Evaluate
# chunk_texts = [c.page_content for c in chunks]
# print("[evaluator] context_relevance:", context_relevance(
#     "What are the main deliverables?", chunk_texts))
# print("[evaluator] faithfulness:", faithfulness(answer, chunk_texts))
# print("[evaluator] answer_relevance:", answer_relevance(
#     "What are the main deliverables?", answer))
# print("[evaluator] keyword_overlap:", keyword_overlap(
#     "What are the main deliverables?", chunk_texts))
