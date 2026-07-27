from typing import List, Optional
from app.core.config.settings import settings
from app.core.logging.logger import logger
from app.ingestion.embeddings.embedder import EmbeddingGenerator

class QueryEmbedder:
    """
    Singleton query embedding service caching the BAAI/bge-small-en-v1.5 model instance.
    Guarantees the model is loaded once and shared across requests.
    """
    _instance: Optional["QueryEmbedder"] = None
    _embedder: Optional[EmbeddingGenerator] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QueryEmbedder, cls).__new__(cls)
            cls._embedder = EmbeddingGenerator(model_name=settings.EMBEDDING_MODEL)
            logger.info(f"QueryEmbedder singleton initialized with '{settings.EMBEDDING_MODEL}'.")
        return cls._instance

    def embed_query(self, query_text: str) -> List[float]:
        """
        Embeds an incoming user query text into a 384-dimensional dense vector.
        """
        if not query_text or not query_text.strip():
            return [0.0] * 384

        if self._embedder is not None:
            vectors = self._embedder.embed_texts([query_text])
            if vectors:
                return vectors[0]

        logger.warning("QueryEmbedder fallback vector generated.")
        return [0.1] * 384
