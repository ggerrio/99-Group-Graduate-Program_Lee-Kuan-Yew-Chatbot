from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(..., description="User question or prompt message", min_length=1)
    session_id: Optional[str] = Field(default=None, description="Optional conversation session ID")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Optional metadata query filters")

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "What were the core principles behind Singapore's economic success?",
                "session_id": "sess-12345",
                "filters": {"document_type": "speeches"}
            }
        }
    }

class CitationItem(BaseModel):
    document_title: str = Field(..., description="Title of the source document")
    document_type: str = Field(..., description="Category (memoirs, speeches, interviews, articles)")
    year: Optional[int] = Field(default=None, description="Year of publication or speech")
    page_number: int = Field(..., description="Source page number")
    score: float = Field(..., description="Vector search similarity relevance score")

class ChatResponse(BaseModel):
    answer: str = Field(..., description="Generated persona answer")
    citations: List[CitationItem] = Field(default_factory=list, description="Grounding source citations")
    session_id: str = Field(..., description="Active session ID")
    is_refusal: bool = Field(..., description="Indicates if query was refused due to lack of grounding context")
    is_post_2015_inference: bool = Field(..., description="Indicates if answer is a post-March 2015 historical inference")

    model_config = {
        "json_schema_extra": {
            "example": {
                "answer": "Singapore's economic strategy required relentless emphasis on meritocracy, human resource development, and long-term planning.",
                "citations": [
                    {
                        "document_title": "From Third World To First World",
                        "document_type": "memoirs",
                        "year": 2000,
                        "page_number": 42,
                        "score": 0.88
                    }
                ],
                "session_id": "sess-12345",
                "is_refusal": False,
                "is_post_2015_inference": False
            }
        }
    }
