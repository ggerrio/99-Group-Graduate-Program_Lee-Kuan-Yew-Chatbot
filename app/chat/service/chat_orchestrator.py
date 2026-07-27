import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from app.core.config.settings import settings
from app.core.logging.logger import logger
from app.retrieval.vector_search.qdrant_retriever import QdrantRetriever, RetrievedChunk
from app.rag.context_builder.context_builder import ContextBuilder
from app.rag.temporal.post_2015_detector import Post2015Detector
from app.chat.service.gemini_service import GeminiService
from app.chat.history.in_memory_history import InMemoryChatHistoryManager

class ChatOrchestrator:
    """
    Coordinates end-to-end RAG workflow: Retrieval -> Context Assembly -> Persona Prompting -> Gemini Generation -> Citations.
    """
    def __init__(self):
        self.retriever = QdrantRetriever()
        self.context_builder = ContextBuilder(max_token_budget=settings.CONTEXT_TOKEN_BUDGET)
        self.gemini_service = GeminiService()
        self.history_manager = InMemoryChatHistoryManager()
        self.prompt_template = self._load_prompt_template()

    def _load_prompt_template(self) -> str:
        template_path = Path("app/rag/prompt_templates/persona_prompt.txt")
        if template_path.exists():
            try:
                return template_path.read_text(encoding="utf-8")
            except Exception as exc:
                logger.error(f"Error loading persona prompt template: {exc}")

        return (
            "You are Lee Kuan Yew.\n"
            "Answer strictly using this retrieved context:\n{context_block}\n\n"
            "Question: {user_query}"
        )

    def process_chat(
        self,
        message: str,
        session_id: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Tuple[str, List[Dict[str, Any]], str, bool, bool]:
        """
        Processes a chat query and returns: (answer, citations, session_id, is_refusal, is_post_2015_inference).
        """
        active_session_id = session_id or str(uuid.uuid4())
        logger.info(f"Processing chat query for session '{active_session_id}': '{message[:60]}...'")

        # Step 1: Retrieve relevant chunks
        chunks = self.retriever.retrieve(
            query=message,
            top_k=settings.RETRIEVAL_TOP_K,
            filters=filters,
        )

        # Step 2: Temporal Post-March 2015 check
        is_post_2015 = Post2015Detector.is_post_2015_event(message, chunks)

        # Step 3: Relevance / Refusal check
        top_score = chunks[0].score if chunks else 0.0
        if not chunks or (top_score < settings.SIMILARITY_SCORE_THRESHOLD and not is_post_2015):
            logger.info(f"Low retrieval confidence (score {top_score} < threshold {settings.SIMILARITY_SCORE_THRESHOLD}). Triggering refusal.")
            refusal_msg = "I have not publicly expressed a clear position on this matter based on the available records."
            self.history_manager.add_turn(active_session_id, "user", message)
            self.history_manager.add_turn(active_session_id, "assistant", refusal_msg)
            return refusal_msg, [], active_session_id, True, False

        # Step 4: Context Assembly within token budget
        context_block, used_chunks = self.context_builder.build_context(chunks)

        # Step 5: Format Persona System Prompt
        full_prompt = self.prompt_template.format(
            context_block=context_block,
            user_query=message,
        )

        # Step 6: Generate persona response via Gemini API
        raw_response = self.gemini_service.generate_response(
            prompt=full_prompt,
            history=self.history_manager.get_history(active_session_id),
        )

        final_answer = raw_response
        if is_post_2015 and "after my lifetime" not in raw_response.lower():
            final_answer = (
                "This event occurred after my lifetime (March 2015).\n\n"
                "AN INFERENCE BASED ON HISTORICAL PRINCIPLES:\n"
                f"{raw_response}"
            )

        # Step 7: Build Citation Payloads
        citations: List[Dict[str, Any]] = []
        for chunk in used_chunks:
            meta = chunk.metadata
            citation = {
                "document_title": meta.get("document_title", "Unknown Title"),
                "document_type": meta.get("document_type", "general"),
                "year": meta.get("year"),
                "page_number": meta.get("page_number", 1),
                "score": chunk.score,
            }
            citations.append(citation)

        # Step 8: Save to in-memory history
        self.history_manager.add_turn(active_session_id, "user", message)
        self.history_manager.add_turn(active_session_id, "assistant", final_answer)

        logger.info(f"Chat processing complete for session '{active_session_id}'. Citations: {len(citations)}.")
        return final_answer, citations, active_session_id, False, is_post_2015
