import hashlib
from typing import List, Tuple, Set
from app.core.logging.logger import logger

class ChunkValidator:
    """
    Validates chunk quality, filters duplicate/corrupted text, and logs quality metrics.
    """
    def __init__(self, min_chunk_len: int = 30):
        self.min_chunk_len = min_chunk_len

    def validate_chunks(self, chunks: List[str]) -> Tuple[List[str], List[int]]:
        valid_chunks: List[str] = []
        valid_indices: List[int] = []
        seen_hashes: Set[str] = set()

        for idx, chunk in enumerate(chunks):
            if not chunk or not chunk.strip():
                logger.warning(f"Validation skipped empty chunk at index {idx}")
                continue

            stripped = chunk.strip()
            if len(stripped) < self.min_chunk_len:
                logger.warning(
                    f"Validation skipped short chunk (len {len(stripped)} < {self.min_chunk_len}) at index {idx}"
                )
                continue

            # Check for non-printable encoding corruption
            printable_ratio = sum(1 for c in stripped if c.isprintable()) / len(stripped)
            if printable_ratio < 0.8:
                logger.warning(f"Validation skipped unprintable/corrupted chunk at index {idx}")
                continue

            # Deduplication check
            chunk_hash = hashlib.sha256(stripped.encode("utf-8")).hexdigest()
            if chunk_hash in seen_hashes:
                logger.warning(f"Validation skipped duplicate chunk content at index {idx}")
                continue

            seen_hashes.add(chunk_hash)
            valid_chunks.append(stripped)
            valid_indices.append(idx)

        return valid_chunks, valid_indices
