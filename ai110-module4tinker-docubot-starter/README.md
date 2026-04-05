# DocuBot

DocuBot is a small documentation assistant that helps answer developer questions about a codebase.  
It can operate in three different modes:

1. **Naive LLM mode**  
   Sends the entire documentation corpus to a Gemini model and asks it to answer the question.

2. **Retrieval only mode**  
   Uses a simple indexing and scoring system to retrieve relevant snippets without calling an LLM.

3. **RAG mode (Retrieval Augmented Generation)**  
   Retrieves relevant snippets, then asks Gemini to answer using only those snippets.

The docs folder contains realistic developer documents (API reference, authentication notes, database notes), but these files are **just text**. They support retrieval experiments and do not require students to set up any backend systems.

---

## Setup

### 1. Install Python dependencies

    pip install -r requirements.txt

### 2. Configure environment variables

Copy the example file:

    cp .env.example .env

Then edit `.env` to include your Gemini API key:

    GEMINI_API_KEY=your_api_key_here

If you do not set a Gemini key, you can still run retrieval only mode.

---

## Running DocuBot

Start the program:

    python main.py

Choose a mode:

- **1**: Naive LLM (Gemini reads the full docs)  
- **2**: Retrieval only (no LLM)  
- **3**: RAG (retrieval + Gemini)

You can use built in sample queries or type your own.

---

## Running Retrieval Evaluation (optional)

    python evaluation.py

This prints simple retrieval hit rates for sample queries.

---

## Modifying the Project

You will primarily work in:

- `docubot.py`  
  Implement or improve the retrieval index, scoring, and snippet selection.

- `llm_client.py`  
  Adjust the prompts and behavior of LLM responses.

- `dataset.py`  
  Add or change sample queries for testing.

---

## Requirements

- Python 3.9+
- A Gemini API key for LLM features (only needed for modes 1 and 3)
- No database, no server setup, no external services besides LLM calls




```text
┌─────────────────────────────────────────────────────────────────┐
│ STARTUP                                                         │
├─────────────────────────────────────────────────────────────────┤
│ main() [main.py] — entry point, runs mode loop                  │
│   │                                                             │
│   ├─► try_create_llm_client() [main.py] — init GeminiClient     │
│   │     └─► GeminiClient.__init__() [llm_client.py] — load key  │
│   │                                                             │
│   └─► DocuBot.__init__() [docubot.py] — init bot               │
│         ├─► load_documents() [docubot.py] — read docs/ folder   │
│         │     (dataset.py) load_fallback_documents() — backup   │
│         └─► build_index() [docubot.py] — build inverted index * │
└─────────────────────────────────────┬───────────────────────────┘
                                      │
                  choose_mode() [main.py] — prompt user for 1/2/3
                                      │
              ┌───────────────────────┼───────────────────────┐
              │                       │                       │
              ▼                       ▼                       ▼
┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│  MODE 1: NAIVE LLM  │ │  MODE 2: RETRIEVAL  │ │    MODE 3: RAG      │
│    (Phase 0)        │ │    ONLY (Phase 1)   │ │    (Phase 2)        │
├─────────────────────┤ ├─────────────────────┤ ├─────────────────────┤
│ run_naive_llm_mode()│ │run_retrieval_only_  │ │  run_rag_mode()     │
│ [main.py]           │ │mode() [main.py]     │ │  [main.py]          │
└────────┬────────────┘ └─────────┬───────────┘ └──────────┬──────────┘
         │                        │                         │
         ▼                        ▼                         ▼
┌────────────────────┐ ┌──────────────────────────────────────────────┐
│    (no retrieval)  │ │          RETRIEVAL STAGE                     │
│                    │ ├──────────────────────────────────────────────┤
│                    │ │ retrieve() [docubot.py] — get top_k docs *   │
│                    │ │   └─► score_document() [docubot.py]          │
│                    │ │         score query vs doc text *            │
└────────┬───────────┘ └──────────┬───────────────────┬──────────────┘
         │                        │                   │
         │              ┌─────────┘                   └──────────────┐
         │              │                                            │
         ▼              ▼                                            ▼
┌─────────────────────────────────┐              ┌──────────────────────────────┐
│ GENERATION STAGE                │              │ GENERATION STAGE             │
├─────────────────────────────────┤              ├──────────────────────────────┤
│ full_corpus_text() [docubot.py] │              │ answer_rag() [docubot.py]    │
│   — concat all docs             │              │   — combine snippets+query   │
│         │                       │              │         │                    │
│         ▼                       │              │         ▼                    │
│ naive_answer_over_full_docs()   │              │ answer_from_snippets()       │
│ [llm_client.py]                 │              │ [llm_client.py]              │
│   — prompt: answer freely       │              │   — prompt: snippets only    │
└──────────┬──────────────────────┘              └──────────────┬───────────────┘
           │                                                    │
           ▼                                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ OUTPUT                                                                       │
├──────────────────────────────────────────────────────────────────────────────┤
│ Mode 1: LLM answer (no grounding)                                            │
│ Mode 2: answer_retrieval_only() [docubot.py] — raw filenames + snippets      │
│ Mode 3: LLM answer grounded in retrieved snippets                            │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│ EVALUATION (standalone — evaluation.py)                                      │
├──────────────────────────────────────────────────────────────────────────────┤
│ evaluate_retrieval() — run SAMPLE_QUERIES, score retrieval hit rate          │
│   ├─► expected_files_for_query() — substring match vs EXPECTED_SOURCES       │
│   └─► bot.retrieve() — same retrieval path as Mode 2/3 above                │
│ print_eval_results() — format and print hit rate + per-query detail          │
└──────────────────────────────────────────────────────────────────────────────┘

* = TODO (not yet implemented)
────────────────────────────────────────────────────────────────────────────────
get_query_or_use_samples() [main.py] — shared by all 3 modes; prompts for
  custom query or returns SAMPLE_QUERIES from dataset.py
```


=========== Some key concepts ============

## build_index(documents) — why an inverted index?
Instead of scanning every document for every query (slow), you pre-compute a lookup table once at startup:
token → [list of filenames containing it]
Rationale: At query time you only need to score documents that share at least one word with the query — skipping irrelevant docs entirely. For a small corpus it doesn't matter much, but it's the right mental model for how real search engines work.
 
## score_document(query, text) — why word overlap count?
score = number of query words found in the document
Rationale: It's the simplest possible signal that actually works. If your query is "auth token" and a doc contains both words, it scores 2. A doc with neither scores 0. This is essentially unigram term matching — the floor of information retrieval, not the ceiling. It's intentionally naive so you can feel the difference when you improve it (e.g. weighting rare words more, TF-IDF).

## retrieve(query, top_k=3) — why use the index to filter first?
1. query words → index lookup → candidate filenames (union)
2. score each candidate with score_document()
3. sort descending, return top_k (filename, text) tuples
Rationale: The index acts as a pre-filter. You only call score_document() on docs that are plausibly relevant (share ≥1 word). Then scoring ranks them. This two-step pattern — filter then rank — is the backbone of every production retrieval system (Elasticsearch, Lucene, etc.), just with fancier filters and rankers.


============== Phase 1 observation ===============
1. Retrieval returns entire documents, not snippets.

docubot.py:98 — retrieve() returns (filename, text) where text is the full file content. So even if only one sentence is relevant, you get the whole doc dumped back.

2. Scoring is too coarse — common words dominate.

docubot.py:85 — score_document() counts raw word overlap. Words like "the", "a", "is" appear in every doc, so every doc scores similarly. The actual relevant keywords get drowned out.

Hit rate: 0.88 — but misleading. Returns 3 full documents per query (out of 4 total). Correct file rarely ranked first. Payment query wrongly returns 3 docs.

===============Phase 2 observation ===============

**Hit rate: 0.88** — same number, but quality is dramatically different:

| Metric | Phase 1 | Phase 2 |
|--------|---------|---------|
| What is returned | Full documents | Focused heading-level chunks |
| Scoring method | Flat word count | TF-IDF (rare words weighted higher) |
| Stopword filtering | None | Common words removed |
| Correct file ranked #1 | ~3/8 queries | 7/8 queries |
| Payment query (unanswerable) | Returns 3 irrelevant docs | Returns empty (correct refusal) |
| Text sent to LLM in RAG mode | Entire file contents | Small relevant sections only |


1. **Stopwords** — filtered out words like "the", "is", "how" that match every document
2. **Chunking** — split docs by markdown headings so retrieval returns sections, not whole files
3. **TF-IDF** — score = term frequency x inverse document frequency, so rare words like "token" outweigh common words like "run"