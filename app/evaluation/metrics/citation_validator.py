from typing import List, Dict, Any

# Canonical document keywords & maximum valid page counts derived from Phase 3 ingestion
KNOWN_DOCUMENTS = {
    "third world": {"canonical_title": "From Third World To First World", "max_pages": 800},
    "singapore story": {"canonical_title": "The Singapore Story", "max_pages": 800},
    "one man": {"canonical_title": "One Man's View Of The World", "max_pages": 400},
    "bilingual": {"canonical_title": "Singapore's Bilingual Journey", "max_pages": 400},
    "speeches": {"canonical_title": "Speeches", "max_pages": 300},
    "interviews": {"canonical_title": "Interviews", "max_pages": 300},
    "articles": {"canonical_title": "Articles", "max_pages": 300},
}

def normalize_title(title: str) -> str:
    if not title:
        return ""
    # Normalize unicode smart quotes and special characters
    return title.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').strip().lower()

def validate_citations(citations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validates that cited document titles exist in knowledge base and page numbers are within valid ranges.
    """
    if not citations:
        return {"valid_count": 0, "invalid_count": 0, "failures": []}

    valid_count = 0
    invalid_count = 0
    failures = []

    for idx, cite in enumerate(citations):
        raw_title = cite.get("document_title", "").strip()
        page = cite.get("page_number", 0)

        norm_title = normalize_title(raw_title)
        doc_found = False
        max_pages = 800

        for key, info in KNOWN_DOCUMENTS.items():
            if key in norm_title or norm_title in key:
                doc_found = True
                max_pages = info["max_pages"]
                break

        if not doc_found:
            invalid_count += 1
            failures.append({
                "citation_index": idx,
                "document_title": raw_title,
                "page_number": page,
                "reason": f"Unknown document title '{raw_title}' not in knowledge base",
            })
        elif page <= 0 or page > max_pages:
            invalid_count += 1
            failures.append({
                "citation_index": idx,
                "document_title": raw_title,
                "page_number": page,
                "reason": f"Page number {page} out of bounds (1-{max_pages}) for '{raw_title}'",
            })
        else:
            valid_count += 1

    return {
        "valid_count": valid_count,
        "invalid_count": invalid_count,
        "failures": failures,
    }
