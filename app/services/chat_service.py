from typing import Dict, Any

class ChatService:
    """
    Abstract Service Interface placeholder for future AI / RAG Chat execution.
    No AI logic is executed in Phase 2.
    """
    async def process_query(self, query: str) -> Dict[str, Any]:
        """
        Placeholder method for future RAG pipeline invocation.
        """
        raise NotImplementedError("AI Chat execution will be implemented in future phases.")
