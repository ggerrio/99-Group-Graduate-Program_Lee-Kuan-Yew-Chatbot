from fastapi.testclient import TestClient
from app.main import app
from app.retrieval.query_embedder.query_embedder import QueryEmbedder
from app.retrieval.vector_search.qdrant_retriever import QdrantRetriever, RetrievedChunk
from app.rag.context_builder.context_builder import ContextBuilder
from app.rag.temporal.post_2015_detector import Post2015Detector
from app.chat.service.chat_orchestrator import ChatOrchestrator

client = TestClient(app)

def test_query_embedder_singleton():
    e1 = QueryEmbedder()
    e2 = QueryEmbedder()
    assert e1 is e2
    vec = e1.embed_query("Meritocracy in Singapore")
    assert len(vec) == 384

def test_vector_search_with_filtering():
    retriever = QdrantRetriever()
    results = retriever.retrieve("Singapore economic growth", top_k=3, filters={"document_type": "memoirs"})
    assert isinstance(results, list)
    if results:
        assert results[0].metadata.get("document_type") == "memoirs"

def test_context_builder_token_budget():
    builder = ContextBuilder(max_token_budget=200) # 800 char budget
    chunks = [
        RetrievedChunk(
            chunk_id="1",
            score=0.9,
            clean_text="A " * 150, # ~300 chars
            metadata={"document_title": "Doc A", "page_number": 1},
        ),
        RetrievedChunk(
            chunk_id="2",
            score=0.8,
            clean_text="B " * 300, # ~600 chars
            metadata={"document_title": "Doc B", "page_number": 2},
        ),
    ]
    context, used = builder.build_context(chunks)
    assert len(used) == 1
    assert "Doc A" in context

def test_post_2015_detector():
    chunks = []
    assert Post2015Detector.is_post_2015_event("What is your view on ChatGPT in 2024?", chunks) is True
    assert Post2015Detector.is_post_2015_event("Tell me about independence in 1965", chunks) is False

def test_chat_orchestrator_refusal():
    orchestrator = ChatOrchestrator()
    answer, citations, sess_id, is_refusal, is_post_2015 = orchestrator.process_chat(
        message="How do I bake a chocolate lava cake?",
        filters={"document_type": "unrelated_category_filter"}
    )
    assert is_refusal is True
    assert "I have not publicly expressed a clear position" in answer
    assert len(citations) == 0

def test_chat_api_endpoint():
    response = client.post(
        "/api/v1/chat",
        json={"message": "What were the core principles of Singapore's development?"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "answer" in data["data"]
    assert "citations" in data["data"]
    assert "session_id" in data["data"]
