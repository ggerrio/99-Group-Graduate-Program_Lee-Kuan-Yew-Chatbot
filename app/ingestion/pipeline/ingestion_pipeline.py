import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from app.core.config.settings import settings
from app.core.logging.logger import logger
from app.ingestion.loaders.pdf_loader import PDFLoader
from app.ingestion.cleaners.text_cleaner import TextCleaner
from app.ingestion.splitters.semantic_splitter import SemanticSplitter
from app.ingestion.metadata.metadata_extractor import MetadataExtractor
from app.ingestion.validators.chunk_validator import ChunkValidator
from app.ingestion.embeddings.embedder import EmbeddingGenerator
from app.ingestion.exporters.processed_exporter import ProcessedExporter
from app.ingestion.utils.hash_utils import compute_file_sha256

class IngestionPipeline:
    """
    Modular ingestion pipeline transforming raw PDFs into clean, validated, embedded vector-ready documents.
    """
    def __init__(self, force_reprocess: bool = False, dry_run: bool = False):
        self.force_reprocess = force_reprocess
        self.dry_run = dry_run
        self.loader = PDFLoader(max_file_size=settings.MAX_FILE_SIZE)
        self.cleaner = TextCleaner()
        self.splitter = SemanticSplitter(
            target_chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
        )
        self.validator = ChunkValidator()
        self.embedder = EmbeddingGenerator(model_name=settings.EMBEDDING_MODEL)
        self.exporter = ProcessedExporter(processed_dir=Path(settings.PROCESSED_DIR))

    def process_file(self, file_path: Path) -> Optional[List[Dict[str, Any]]]:
        """
        Executes end-to-end ingestion pipeline on a single PDF document.
        """
        if not file_path.exists() or file_path.suffix.lower() not in settings.SUPPORTED_EXTENSIONS:
            return None

        file_hash = compute_file_sha256(file_path)
        state = self.exporter.load_state()

        # Incremental ingestion check
        if not self.force_reprocess and file_path.name in state:
            if state[file_path.name].get("sha256") == file_hash:
                logger.info(f"Skipping unchanged file '{file_path.name}' (SHA256 match).")
                return []

        start_time = time.time()
        logger.info(f"--> Ingestion started for '{file_path.name}'")

        # Stage 1: Load PDF
        doc = self.loader.load_pdf(file_path)
        if not doc or not doc.pages:
            logger.warning(f"Aborting ingestion for '{file_path.name}': PDF loading yielded no content.")
            return None

        # Stage 2 & 3: Clean & Split per page
        all_chunks: List[str] = []
        all_page_numbers: List[int] = []

        for page in doc.pages:
            cleaned_page_text = self.cleaner.clean_text(page.text)
            if not cleaned_page_text:
                continue

            page_chunks = self.splitter.split_text(cleaned_page_text)
            for c in page_chunks:
                all_chunks.append(c.text)
                all_page_numbers.append(page.page_number)

        if not all_chunks:
            logger.warning(f"No valid text chunks generated from '{file_path.name}'.")
            return None

        # Stage 4: Validate Chunks
        valid_chunks, valid_indices = self.validator.validate_chunks(all_chunks)
        if not valid_chunks:
            logger.warning(f"All chunks failed validation for '{file_path.name}'.")
            return None

        total_valid = len(valid_chunks)

        # Stage 5: Extract Metadata per valid chunk
        metadatas: List[Dict[str, Any]] = []
        for new_idx, orig_idx in enumerate(valid_indices, start=1):
            page_num = all_page_numbers[orig_idx]
            chunk_text = valid_chunks[new_idx - 1]
            meta = MetadataExtractor.create_metadata(
                file_path=file_path,
                text_sample=chunk_text,
                page_number=page_num,
                chunk_index=new_idx,
                total_chunks=total_valid,
            )
            metadatas.append(meta)

        # Dry-run early exit
        if self.dry_run:
            duration = round(time.time() - start_time, 2)
            logger.info(f"[DRY-RUN] Processed '{file_path.name}': {total_valid} valid chunks ({duration}s).")
            return []

        # Stage 6: Generate Embeddings
        logger.info(f"Generating embeddings for {total_valid} chunks of '{file_path.name}'...")
        embeddings = self.embedder.embed_texts(valid_chunks)

        # Stage 7 & 8: Export Vector Documents & Save
        vector_docs = self.exporter.export_vector_documents(
            source_filename=file_path.name,
            file_hash=file_hash,
            chunks=valid_chunks,
            metadatas=metadatas,
            embeddings=embeddings,
        )

        duration = round(time.time() - start_time, 2)
        logger.info(f"<-- Ingestion finished for '{file_path.name}': {len(vector_docs)} chunks ({duration}s).")
        return vector_docs

    def process_directory(self, target_dir: Path) -> List[Dict[str, Any]]:
        """
        Recursively processes all PDF files in target directory.
        """
        all_vector_docs: List[Dict[str, Any]] = []
        pdf_files = list(target_dir.rglob("*.pdf"))

        logger.info(f"Discovered {len(pdf_files)} PDF files in '{target_dir}'.")
        for pdf_file in pdf_files:
            try:
                docs = self.process_file(pdf_file)
                if docs:
                    all_vector_docs.extend(docs)
            except Exception as exc:
                logger.error(f"Unexpected error processing '{pdf_file.name}': {exc}")
                continue

        return all_vector_docs
