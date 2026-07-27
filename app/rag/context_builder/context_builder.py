from typing import List, Tuple
from app.core.config.settings import settings
from app.core.logging.logger import logger
from app.retrieval.vector_search.qdrant_retriever import RetrievedChunk

class ContextBuilder:
    """
    Assembles structured, tagged context blocks from retrieved chunks while enforcing token budgets.
    """
    def __init__(self, max_token_budget: int = settings.CONTEXT_TOKEN_BUDGET):
        self.max_token_budget = max_token_budget
        # Approximate 1 token = 4 characters rule of thumb
        self.max_char_budget = max_token_budget * 4

    def build_context(self, chunks: List[RetrievedChunk]) -> Tuple[str, List[RetrievedChunk]]:
        """
        Formats retrieved chunks into tagged context blocks and returns the combined string along with used chunks.
        """
        if not chunks:
            return "No relevant context retrieved.", []

        # Ensure chunks are sorted by relevance score descending
        sorted_chunks = sorted(chunks, key=lambda c: c.score, reverse=True)

        used_chunks: List[RetrievedChunk] = []
        formatted_blocks: List[str] = []
        current_chars = 0

        for chunk in sorted_chunks:
            meta = chunk.metadata
            title = meta.get("document_title", "Unknown Title")
            doc_type = meta.get("document_type", "General")
            year = meta.get("year", "N/A")
            page = meta.get("page_number", "N/A")

            header = f"[Source: {title} | Type: {doc_type} | Year: {year} | Page: {page} | Score: {chunk.score}]"
            block = f"{header}\n{chunk.clean_text}\n"

            block_len = len(block)
            if current_chars + block_len <= self.max_char_budget:
                formatted_blocks.append(block)
                used_chunks.append(chunk)
                current_chars += block_len
            else:
                logger.info(f"Context budget reached ({current_chars}/{self.max_char_budget} chars). Dropping lower-score chunks.")
                break

        assembled_context = "\n---\n".join(formatted_blocks)
        logger.info(f"Assembled context using {len(used_chunks)} chunks ({current_chars} characters).")
        return assembled_context, used_chunks
