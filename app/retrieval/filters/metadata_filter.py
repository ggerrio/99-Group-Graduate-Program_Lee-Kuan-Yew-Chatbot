from typing import Dict, Any, Optional

class MetadataFilterBuilder:
    """
    Constructs metadata filters for document type, year, and category queries.
    """
    @staticmethod
    def build_filter(
        document_type: Optional[str] = None,
        year: Optional[int] = None,
        category: Optional[str] = None,
    ) -> Dict[str, Any]:
        filters: Dict[str, Any] = {}
        if document_type:
            filters["document_type"] = document_type.lower()
        if year is not None:
            filters["year"] = year
        if category:
            filters["category"] = category.capitalize()
        return filters
