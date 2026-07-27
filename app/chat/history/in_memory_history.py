from typing import Dict, List
from dataclasses import dataclass, field
from app.core.config.settings import settings
from app.core.logging.logger import logger

@dataclass
class ChatTurn:
    role: str # "user" or "assistant"
    content: str

class InMemoryChatHistoryManager:
    """
    In-memory single-session conversation history store managing max turns.
    """
    def __init__(self, max_turns: int = settings.CHAT_HISTORY_MAX_TURNS):
        self.max_turns = max_turns
        self._sessions: Dict[str, List[ChatTurn]] = {}

    def get_history(self, session_id: str) -> List[ChatTurn]:
        return self._sessions.get(session_id, [])

    def add_turn(self, session_id: str, role: str, content: str):
        if session_id not in self._sessions:
            self._sessions[session_id] = []
        
        self._sessions[session_id].append(ChatTurn(role=role, content=content))
        
        # Enforce max turns limit per session
        if len(self._sessions[session_id]) > self.max_turns * 2:
            self._sessions[session_id] = self._sessions[session_id][-(self.max_turns * 2):]
            logger.info(f"Trimmed chat history for session '{session_id}' to max {self.max_turns} turns.")

    def clear_session(self, session_id: str):
        if session_id in self._sessions:
            del self._sessions[session_id]
