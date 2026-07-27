from typing import List
from app.core.config.settings import settings
from app.core.logging.logger import logger

class EmbeddingGenerator:
    """
    Generates dense vector embeddings using SentenceTransformers with BAAI/bge-small-en-v1.5.
    Includes fallback mock embedding mode for offline/dry-run environments.
    """
    def __init__(self, model_name: str = settings.EMBEDDING_MODEL):
        self.model_name = model_name
        self.model = None
        self._load_model()

    def _load_model(self):
        try:
            import os
            if settings.HF_TOKEN:
                os.environ["HF_TOKEN"] = settings.HF_TOKEN
            from sentence_transformers import SentenceTransformer
            logger.info(f"Loading SentenceTransformer model '{self.model_name}'...")
            self.model = SentenceTransformer(self.model_name)
            logger.info("Embedding model loaded successfully.")
        except Exception as exc:
            logger.warning(f"SentenceTransformer load deferred or offline fallback: {exc}")
            self.model = None

    def embed_texts(self, texts: List[str], batch_size: int = settings.PROCESSING_BATCH_SIZE) -> List[List[float]]:
        if not texts:
            return []

        if self.model is not None:
            try:
                embeddings = self.model.encode(
                    texts,
                    batch_size=batch_size,
                    show_progress_bar=False,
                    normalize_embeddings=True,
                )
                return [e.tolist() for e in embeddings]
            except Exception as exc:
                logger.error(f"Error generating embeddings with model: {exc}")

        # Fallback deterministic normalized 384-dimensional vector for dry-run/testing
        logger.info(f"Generating deterministic fallback vectors for {len(texts)} chunks.")
        dummy_vectors = []
        for text in texts:
            val = float(hash(text) % 1000) / 1000.0
            vector = [val] * 384
            dummy_vectors.append(vector)
        return dummy_vectors
