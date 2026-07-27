from fastapi import APIRouter, Depends, status
from app.schemas.response import SuccessResponse
from app.chat.api.schemas import ChatRequest, ChatResponse, CitationItem
from app.chat.service.chat_orchestrator import ChatOrchestrator

router = APIRouter(prefix="/chat", tags=["Chat"])

# Instantiate single orchestrator dependency
_orchestrator = ChatOrchestrator()

def get_chat_orchestrator() -> ChatOrchestrator:
    return _orchestrator

@router.post(
    "",
    response_model=SuccessResponse[ChatResponse],
    status_code=status.HTTP_200_OK,
    summary="Converse with Lee Kuan Yew AI Chatbot",
    description="Processes user questions, retrieves grounded document context, applies persona rules, and returns answers with source citations.",
)

def chat_endpoint(
    request: ChatRequest,
    orchestrator: ChatOrchestrator = Depends(get_chat_orchestrator),
) -> SuccessResponse[ChatResponse]:
    answer, raw_citations, session_id, is_refusal, is_post_2015 = orchestrator.process_chat(
        message=request.message,
        session_id=request.session_id,
        filters=request.filters,
    )

    citations = [CitationItem(**c) for c in raw_citations]

    payload = ChatResponse(
        answer=answer,
        citations=citations,
        session_id=session_id,
        is_refusal=is_refusal,
        is_post_2015_inference=is_post_2015,
    )

    return SuccessResponse(
        data=payload,
        message="Chat response generated successfully.",
    )
