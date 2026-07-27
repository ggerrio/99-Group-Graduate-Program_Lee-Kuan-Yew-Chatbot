import re
from pathlib import Path
from typing import Dict, Any, Optional

class MetadataExtractor:
    """
    Extracts structured metadata from file paths, text content, and document attributes.
    """
    YEAR_PATTERN = re.compile(r"\b(19\d{2}|20\d{2})\b")

    @classmethod
    def determine_document_type(cls, file_path: Path) -> str:
        parts = [p.lower() for p in file_path.parts]
        for category in ["memoirs", "speeches", "interviews", "articles"]:
            if category in parts:
                return category
        return "general"

    @classmethod
    def extract_year(cls, text: str, filename: str) -> Optional[int]:
        filename_match = cls.YEAR_PATTERN.search(filename)
        if filename_match:
            return int(filename_match.group(1))

        text_match = cls.YEAR_PATTERN.search(text[:500])
        if text_match:
            return int(text_match.group(1))

        return None

    @classmethod
    def create_metadata(
        cls,
        file_path: Path,
        text_sample: str,
        page_number: int,
        chunk_index: int,
        total_chunks: int,
        section_title: Optional[str] = None,
    ) -> Dict[str, Any]:
        document_type = cls.determine_document_type(file_path)
        year = cls.extract_year(text_sample, file_path.name)
        title = file_path.stem.replace("_", " ").replace("-", " ").title()

        return {
            "document_title": title,
            "document_type": document_type,
            "author": "Lee Kuan Yew",
            "year": year,
            "category": document_type.capitalize(),
            "source_filename": file_path.name,
            "page_number": page_number,
            "chunk_index": chunk_index,
            "total_chunks": total_chunks,
            "language": "en",
            "section_title": section_title or title,
        }
