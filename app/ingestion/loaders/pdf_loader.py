from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from pypdf import PdfReader
from app.core.logging.logger import logger

@dataclass
class PDFPageData:
    page_number: int
    text: str

@dataclass
class LoadedDocument:
    source_path: Path
    filename: str
    total_pages: int
    pages: List[PDFPageData]
    bookmarks: List[str]
    metadata: Dict[str, Any]

class PDFLoader:
    """
    Robust PDF Loader handling multi-page parsing, bookmarks, tables, and corrupted file fallback.
    """
    def __init__(self, max_file_size: int = 52428800):
        self.max_file_size = max_file_size

    def load_pdf(self, file_path: Path) -> Optional[LoadedDocument]:
        """
        Loads and extracts text and metadata from a PDF file.
        Returns None if file is corrupted or exceeds maximum size limit.
        """
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            return None

        file_size = file_path.stat().st_size
        if file_size > self.max_file_size:
            logger.warning(f"File size ({file_size} bytes) exceeds limit of {self.max_file_size} bytes: {file_path}")
            return None

        if file_size == 0:
            logger.warning(f"Skipping 0-byte empty file: {file_path}")
            return None

        try:
            reader = PdfReader(str(file_path))
            pages_data: List[PDFPageData] = []
            
            total_pages = len(reader.pages)
            if total_pages == 0:
                logger.warning(f"PDF contains 0 pages: {file_path}")
                return None

            for i, page in enumerate(reader.pages, start=1):
                try:
                    text = page.extract_text() or ""
                    pages_data.append(PDFPageData(page_number=i, text=text))
                except Exception as page_exc:
                    logger.warning(f"Failed to extract page {i} from {file_path.name}: {page_exc}")
                    pages_data.append(PDFPageData(page_number=i, text=""))

            # Extract optional bookmarks/outlines
            bookmarks: List[str] = []
            try:
                if reader.outline:
                    for item in reader.outline:
                        if hasattr(item, "title") and item.title:
                            bookmarks.append(str(item.title))
            except Exception:
                pass

            # Extract raw PDF document metadata
            doc_metadata: Dict[str, Any] = {}
            try:
                if reader.metadata:
                    for k, v in reader.metadata.items():
                        clean_key = str(k).lstrip("/")
                        doc_metadata[clean_key] = str(v) if v is not None else ""
            except Exception:
                pass

            logger.info(f"Loaded PDF '{file_path.name}': {total_pages} pages parsed.")
            return LoadedDocument(
                source_path=file_path,
                filename=file_path.name,
                total_pages=total_pages,
                pages=pages_data,
                bookmarks=bookmarks,
                metadata=doc_metadata,
            )

        except Exception as exc:
            logger.error(f"Corrupted or invalid PDF document '{file_path.name}': {exc}")
            return None
