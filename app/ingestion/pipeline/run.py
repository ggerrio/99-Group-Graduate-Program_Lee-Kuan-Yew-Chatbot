import argparse
import sys
from pathlib import Path
from app.core.config.settings import settings
from app.core.logging.logger import logger
from app.ingestion.pipeline.ingestion_pipeline import IngestionPipeline

def main():
    parser = argparse.ArgumentParser(
        description="Lee Kuan Yew AI Chatbot - Knowledge Ingestion Pipeline CLI"
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Force full re-processing of all documents, ignoring cached hash state",
    )
    parser.add_argument(
        "--file",
        type=str,
        default=None,
        help="Path to a single PDF document to process",
    )
    parser.add_argument(
        "--folder",
        type=str,
        default=None,
        help="Specific sub-folder inside knowledge directory to process",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Execute parsing, cleaning, and validation without generating embeddings or saving output",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable detailed log outputs",
    )

    args = parser.parse_args()

    if args.verbose:
        logger.info("Verbose mode activated.")

    logger.info("Initializing Knowledge Ingestion Pipeline...")
    pipeline = IngestionPipeline(
        force_reprocess=args.full,
        dry_run=args.dry_run,
    )

    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            logger.error(f"Target file does not exist: {file_path}")
            sys.exit(1)
        results = pipeline.process_file(file_path)
        logger.info(f"Single file ingestion complete. Generated {len(results or [])} vector docs.")
    else:
        target_dir = Path(args.folder) if args.folder else Path(settings.KNOWLEDGE_DIR)
        if not target_dir.exists():
            logger.error(f"Knowledge directory does not exist: {target_dir}")
            sys.exit(1)
        results = pipeline.process_directory(target_dir)
        logger.info(f"Directory ingestion complete. Total vector docs generated: {len(results)}")

if __name__ == "__main__":
    main()
