"""
Core DocuBot class responsible for:
- Loading documents from the docs/ folder
- Building a simple retrieval index (Phase 1)
- Retrieving relevant snippets (Phase 1)
- Supporting retrieval only answers
- Supporting RAG answers when paired with Gemini (Phase 2)
"""

import os
import glob
import re
import math

STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "shall",
    "should", "may", "might", "must", "can", "could", "am", "in", "on",
    "at", "to", "for", "of", "with", "by", "from", "as", "into", "about",
    "it", "its", "i", "me", "my", "we", "our", "you", "your", "he", "she",
    "they", "them", "this", "that", "these", "those", "there", "here",
    "how", "what", "which", "who", "when", "where", "why", "if", "or",
    "and", "but", "not", "no", "any", "all", "each", "some",
    "docs", "document", "documents", "mention", "using",
}


class DocuBot:
    def __init__(self, docs_folder="docs", llm_client=None):
        """
        docs_folder: directory containing project documentation files
        llm_client: optional Gemini client for LLM based answers
        """
        self.docs_folder = docs_folder
        self.llm_client = llm_client

        # Load documents and chunk them by heading
        self.documents = self.load_documents()  # List of (filename, text)
        self.chunks = self._chunk_documents(self.documents)  # List of (label, text)

        # Build index over chunks, plus IDF weights
        self.index = self.build_index(self.chunks)
        self.num_chunks = len(self.chunks)
        self.idf = self._compute_idf()

    # -----------------------------------------------------------
    # Document Loading
    # -----------------------------------------------------------

    def load_documents(self):
        """
        Loads all .md and .txt files inside docs_folder.
        Returns a list of tuples: (filename, text)
        """
        docs = []
        pattern = os.path.join(self.docs_folder, "*.*")
        for path in glob.glob(pattern):
            if path.endswith(".md") or path.endswith(".txt"):
                with open(path, "r", encoding="utf8") as f:
                    text = f.read()
                filename = os.path.basename(path)
                docs.append((filename, text))
        return docs

    # -----------------------------------------------------------
    # Chunking (Phase 2)
    # -----------------------------------------------------------

    def _chunk_documents(self, documents):
        """
        Split each document into sections by markdown headings.
        Prepends the doc title (first heading) to each chunk for context.
        Returns a list of (filename, text) tuples.
        """
        chunks = []
        for filename, text in documents:
            sections = re.split(r"(?=^#{1,3}\s)", text, flags=re.MULTILINE)
            # Extract the document title from the first heading
            title = ""
            for s in sections:
                s = s.strip()
                if s.startswith("#"):
                    title = s.split("\n")[0]
                    break

            for section in sections:
                section = section.strip()
                if not section:
                    continue
                # Prepend title to non-title chunks so the doc topic is searchable
                if not section.startswith("# ") and title:
                    section = title + "\n\n" + section
                chunks.append((filename, section))
        return chunks

    # -----------------------------------------------------------
    # Index Construction (Phase 1 + 2)
    # -----------------------------------------------------------

    def _tokenize(self, text):
        """Lowercase, extract words, remove stopwords."""
        words = re.findall(r"[a-z0-9_]+", text.lower())
        return [w for w in words if w not in STOPWORDS]

    def build_index(self, chunks):
        """
        Build an inverted index mapping tokens to chunk indices.
        """
        index = {}
        for i, (label, text) in enumerate(chunks):
            for token in set(self._tokenize(text)):
                if token not in index:
                    index[token] = []
                index[token].append(i)
        return index

    def _compute_idf(self):
        """Compute IDF for each token: log(num_chunks / docs_containing_token)."""
        idf = {}
        for token, chunk_ids in self.index.items():
            idf[token] = math.log(self.num_chunks / len(chunk_ids))
        return idf

    # -----------------------------------------------------------
    # Scoring and Retrieval (Phase 1 + 2)
    # -----------------------------------------------------------

    def score_document(self, query, text):
        """
        TF-IDF scoring: term frequency in the chunk * IDF weight.
        """
        query_words = self._tokenize(query)
        text_tokens = self._tokenize(text)
        score = 0.0
        for word in query_words:
            tf = text_tokens.count(word)
            if tf > 0:
                score += tf * self.idf.get(word, 0.0)
        return score

    def retrieve(self, query, top_k=3):
        """
        Use the index to find candidate chunks, score with TF-IDF,
        return top_k as (filename, text) sorted by score descending.
        """
        query_words = self._tokenize(query)
        candidate_indices = set()
        for word in query_words:
            if word in self.index:
                candidate_indices.update(self.index[word])

        scored = []
        for i in candidate_indices:
            filename, text = self.chunks[i]
            score = self.score_document(query, text)
            scored.append((score, filename, text))

        scored.sort(key=lambda x: x[0], reverse=True)
        results = [(filename, text) for score, filename, text in scored]
        return results[:top_k]

    # -----------------------------------------------------------
    # Answering Modes
    # -----------------------------------------------------------

    def answer_retrieval_only(self, query, top_k=3):
        """
        Phase 1 retrieval only mode.
        Returns raw snippets and filenames with no LLM involved.
        """
        snippets = self.retrieve(query, top_k=top_k)

        if not snippets:
            return "I do not know based on these docs."

        formatted = []
        for filename, text in snippets:
            formatted.append(f"[{filename}]\n{text}\n")

        return "\n---\n".join(formatted)

    def answer_rag(self, query, top_k=3):
        """
        Phase 2 RAG mode.
        Uses student retrieval to select snippets, then asks Gemini
        to generate an answer using only those snippets.
        """
        if self.llm_client is None:
            raise RuntimeError(
                "RAG mode requires an LLM client. Provide a GeminiClient instance."
            )

        snippets = self.retrieve(query, top_k=top_k)

        if not snippets:
            return "I do not know based on these docs."

        return self.llm_client.answer_from_snippets(query, snippets)

    # -----------------------------------------------------------
    # Bonus Helper: concatenated docs for naive generation mode
    # -----------------------------------------------------------

    def full_corpus_text(self):
        """
        Returns all documents concatenated into a single string.
        This is used in Phase 0 for naive 'generation only' baselines.
        """
        return "\n\n".join(text for _, text in self.documents)
