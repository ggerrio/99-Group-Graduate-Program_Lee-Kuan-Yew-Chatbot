import json
import math
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from app.core.config.settings import settings
from app.core.logging.logger import logger
from app.retrieval.query_embedder.query_embedder import QueryEmbedder

@dataclass
class RetrievedChunk:
    chunk_id: str
    score: float
    clean_text: str
    metadata: Dict[str, Any]

class QdrantRetriever:
    """
    Vector search retriever querying Qdrant vector database or local /processed/embeddings vector documents.
    
    TODO: Implement hybrid search (dense + sparse/BM25) when Qdrant sparse vector payload indices are configured.
    TODO: Add Cohere / Cross-Encoder re-ranking stage if search precision tuning is requested in future phases.
    """
    def __init__(self, processed_dir: Path = Path(settings.PROCESSED_DIR)):
        self.processed_dir = processed_dir
        self.embeddings_dir = processed_dir / "embeddings"
        self.embedder = QueryEmbedder()
        self.local_cache: List[Dict[str, Any]] = []
        self._load_local_index()

    def _load_local_index(self):
        """
        Loads all exported vector payload JSON files from Phase 3 (/processed/embeddings/).
        """
        if not self.embeddings_dir.exists():
            logger.warning(f"Embeddings directory does not exist: {self.embeddings_dir}")
            return

        self.local_cache.clear()
        for json_file in self.embeddings_dir.glob("*_embeddings.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    docs = json.load(f)
                    if isinstance(docs, list):
                        self.local_cache.extend(docs)
            except Exception as exc:
                logger.error(f"Error loading vector artifact '{json_file.name}': {exc}")

        logger.info(f"Loaded {len(self.local_cache)} vector documents into local retriever index.")

    @staticmethod
    def _cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0
        dot = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    def retrieve(
        self,
        query: str,
        top_k: int = settings.RETRIEVAL_TOP_K,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[RetrievedChunk]:
        """
        Retrieves top_k relevant document chunks for the user query with optional metadata filtering.
        """
        if not query or not query.strip():
            return []

        logger.info(f"Retrieving top {top_k} chunks for query: '{query[:60]}...'")
        query_vector = self.embedder.embed_query(query)

        scored_chunks: List[RetrievedChunk] = []

        for doc in self.local_cache:
            meta = doc.get("metadata", {})

            # Metadata filtering logic
            if filters:
                match = True
                for k, v in filters.items():
                    if k in meta and str(meta[k]).lower() != str(v).lower():
                        match = False
                        break
                if not match:
                    continue

            emb = doc.get("embedding", [])
            score = self._cosine_similarity(query_vector, emb)

            chunk = RetrievedChunk(
                chunk_id=doc.get("id", ""),
                score=round(score, 4),
                clean_text=doc.get("clean_text", ""),
                metadata=meta,
            )
            scored_chunks.append(chunk)

        # Sort by similarity score descending
        scored_chunks.sort(key=lambda c: c.score, reverse=True)
        top_chunks = scored_chunks[:top_k]

        top_score = top_chunks[0].score if top_chunks else 0.0
        logger.info(f"Retrieval complete. Found {len(top_chunks)} chunks (top score: {top_score}).")
        return top_chunks
