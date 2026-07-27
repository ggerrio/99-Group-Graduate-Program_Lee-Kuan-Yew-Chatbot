import json
import uuid
from pathlib import Path
from typing import List, Dict, Any
from app.core.config.settings import settings
from app.core.logging.logger import logger

class ProcessedExporter:
    """
    Exports clean vector-ready document artifacts to the /processed directory.
    Manages incremental ingestion state to skip unchanged files.
    """
    def __init__(self, processed_dir: Path = Path(settings.PROCESSED_DIR)):
        self.processed_dir = processed_dir
        self.chunks_dir = processed_dir / "chunks"
        self.metadata_dir = processed_dir / "metadata"
        self.embeddings_dir = processed_dir / "embeddings"
        self.state_file = processed_dir / "state.json"
        self._ensure_dirs()

    def _ensure_dirs(self):
        self.chunks_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_dir.mkdir(parents=True, exist_ok=True)
        self.embeddings_dir.mkdir(parents=True, exist_ok=True)

    def load_state(self) -> Dict[str, Any]:
        if self.state_file.exists():
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as exc:
                logger.warning(f"Could not load state file {self.state_file}: {exc}")
        return {}

    def save_state(self, state: Dict[str, Any]):
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)

    def export_vector_documents(
        self,
        source_filename: str,
        file_hash: str,
        chunks: List[str],
        metadatas: List[Dict[str, Any]],
        embeddings: List[List[float]],
    ) -> List[Dict[str, Any]]:
        vector_docs: List[Dict[str, Any]] = []
        safe_stem = Path(source_filename).stem.replace(" ", "_")

        for idx, (chunk_text, meta, emb) in enumerate(zip(chunks, metadatas, embeddings)):
            doc_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{source_filename}_{idx}"))
            vector_doc = {
                "id": doc_id,
                "embedding": emb,
                "metadata": meta,
                "clean_text": chunk_text,
            }
            vector_docs.append(vector_doc)

        # Save chunks JSON
        chunks_file = self.chunks_dir / f"{safe_stem}_chunks.json"
        with open(chunks_file, "w", encoding="utf-8") as f:
            json.dump([d["clean_text"] for d in vector_docs], f, indent=2)

        # Save metadata JSON
        metadata_file = self.metadata_dir / f"{safe_stem}_metadata.json"
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump([d["metadata"] for d in vector_docs], f, indent=2)

        # Save vector payload JSON
        embeddings_file = self.embeddings_dir / f"{safe_stem}_embeddings.json"
        with open(embeddings_file, "w", encoding="utf-8") as f:
            json.dump(vector_docs, f, indent=2)

        # Update state JSON
        state = self.load_state()
        state[source_filename] = {
            "sha256": file_hash,
            "chunks_count": len(vector_docs),
            "output_file": str(embeddings_file),
        }
        self.save_state(state)

        logger.info(f"Exported {len(vector_docs)} vector documents for '{source_filename}'.")
        return vector_docs
