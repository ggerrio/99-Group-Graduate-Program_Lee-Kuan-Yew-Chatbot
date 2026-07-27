from typing import List, Dict, Any, Optional

def evaluate_retrieval_precision_recall(
    retrieved_chunks: List[Any],
    expected_source: Optional[str],
    top_k: int = 5,
) -> Dict[str, float]:
    """
    Computes precision@k and recall@k for a single query.
    Checks whether retrieved chunks match expected_source document title.
    """
    if not expected_source:
        return {"precision_at_k": 0.0, "recall_at_k": 0.0, "hit": 0.0}

    if not retrieved_chunks:
        return {"precision_at_k": 0.0, "recall_at_k": 0.0, "hit": 0.0}

    relevant_hits = 0
    expected_lower = expected_source.lower()

    for chunk in retrieved_chunks[:top_k]:
        doc_title = chunk.metadata.get("document_title", "").lower()
        if expected_lower in doc_title or doc_title in expected_lower:
            relevant_hits += 1

    precision = relevant_hits / float(min(len(retrieved_chunks), top_k))
    hit = 1.0 if relevant_hits > 0 else 0.0

    return {
        "precision_at_k": round(precision, 4),
        "recall_at_k": round(hit, 4),  # Hit@k acts as binary recall metric for single source
        "hit": hit,
    }
