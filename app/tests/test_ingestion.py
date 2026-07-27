from pathlib import Path
from app.ingestion.cleaners.text_cleaner import TextCleaner
from app.ingestion.splitters.semantic_splitter import SemanticSplitter
from app.ingestion.metadata.metadata_extractor import MetadataExtractor
from app.ingestion.validators.chunk_validator import ChunkValidator
from app.ingestion.embeddings.embedder import EmbeddingGenerator
from app.ingestion.loaders.pdf_loader import PDFLoader
from app.ingestion.exporters.processed_exporter import ProcessedExporter

def test_text_cleaner():
    raw = "Lee Kuan Yew Speeches\nPage 1 of 5\n\nSingapore became independent in 1965.\n\n\n\nIt prospered rapidly."
    cleaned = TextCleaner.clean_text(raw)
    assert "Page 1 of 5" not in cleaned
    assert "Lee Kuan Yew Speeches" not in cleaned
    assert "Singapore became independent in 1965." in cleaned

def test_semantic_splitter():
    text = (
        "Singapore's economic transformation was guided by strict meritocracy and long-term vision. "
        "The nation invested heavily in human capital, modern infrastructure, and foreign direct investment. "
        "This approach allowed Singapore to transition from a regional trading port to a global financial hub."
    )
    splitter = SemanticSplitter(target_chunk_size=100, chunk_overlap=20)
    chunks = splitter.split_text(text)
    assert len(chunks) > 0
    assert all(isinstance(c.text, str) for c in chunks)

def test_metadata_extractor():
    sample_path = Path("knowledge/speeches/1965_independence_address.pdf")
    meta = MetadataExtractor.create_metadata(
        file_path=sample_path,
        text_sample="In 1965 Singapore gained sovereignty.",
        page_number=1,
        chunk_index=1,
        total_chunks=5,
    )
    assert meta["document_type"] == "speeches"
    assert meta["author"] == "Lee Kuan Yew"
    assert meta["year"] == 1965
    assert meta["chunk_index"] == 1
    assert meta["total_chunks"] == 5

def test_chunk_validator():
    validator = ChunkValidator(min_chunk_len=15)
    test_chunks = [
        "Valid text chunk containing sufficient content.",
        "",
        "Short",
        "Valid text chunk containing sufficient content.", # Duplicate
    ]
    valid_chunks, valid_indices = validator.validate_chunks(test_chunks)
    assert len(valid_chunks) == 1
    assert valid_chunks[0] == "Valid text chunk containing sufficient content."

def test_embedding_generator_dimensions():
    embedder = EmbeddingGenerator()
    texts = ["Governance and meritocracy in Singapore.", "Economic development strategy."]
    vectors = embedder.embed_texts(texts)
    assert len(vectors) == 2
    assert len(vectors[0]) == 384

def test_pdf_loader_corrupt_file(tmp_path):
    corrupt_pdf = tmp_path / "corrupt.pdf"
    corrupt_pdf.write_text("This is not a valid PDF file")
    loader = PDFLoader()
    doc = loader.load_pdf(corrupt_pdf)
    assert doc is None

def test_processed_exporter(tmp_path):
    exporter = ProcessedExporter(processed_dir=tmp_path)
    source_fn = "test_doc.pdf"
    chunks = ["Sample chunk content text."]
    metadatas = [{"document_title": "Test Doc", "chunk_index": 1}]
    embeddings = [[0.1] * 384]

    docs = exporter.export_vector_documents(
        source_filename=source_fn,
        file_hash="test_sha256_hash",
        chunks=chunks,
        metadatas=metadatas,
        embeddings=embeddings,
    )
    assert len(docs) == 1
    assert docs[0]["clean_text"] == "Sample chunk content text."
    assert (tmp_path / "chunks" / "test_doc_chunks.json").exists()
    assert (tmp_path / "embeddings" / "test_doc_embeddings.json").exists()
