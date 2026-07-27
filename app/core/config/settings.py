import os
from typing import List, Union
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Centralized Pydantic v2 application settings loader.
    """
    APP_NAME: str = Field(default="Lee Kuan Yew AI Chatbot", description="Application Title")
    APP_VERSION: str = Field(default="0.4.0", description="API Version")
    DEBUG: bool = Field(default=False, description="Debug mode status")
    HOST: str = Field(default="0.0.0.0", description="Server host binding")
    PORT: int = Field(default=8000, description="Server port binding")

    # Infrastructure & Persistence
    DATABASE_URL: str = Field(default="sqlite:///./lky_chatbot.db", description="Database URI")
    LOG_LEVEL: str = Field(default="INFO", description="Loguru threshold level")

    # Security & CORS
    ALLOWED_ORIGINS: Union[List[str], str] = Field(
        default=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173"],
        description="CORS allowed origins"
    )

    # Ingestion Pipeline Settings (Phase 3)
    CHUNK_SIZE: int = Field(default=750, description="Target chunk size in tokens/characters")
    CHUNK_OVERLAP: int = Field(default=150, description="Chunk overlap size in tokens/characters")
    EMBEDDING_MODEL: str = Field(default="BAAI/bge-small-en-v1.5", description="HuggingFace embedding model name")
    HF_TOKEN: str = Field(default="", description="Optional HuggingFace Hub API Token for authenticated model downloads")
    KNOWLEDGE_DIR: str = Field(default="./knowledge", description="Source raw PDF knowledge directory")
    PROCESSED_DIR: str = Field(default="./processed", description="Processed ingestion artifacts output directory")
    SUPPORTED_EXTENSIONS: List[str] = Field(default=[".pdf"], description="Supported file extensions")
    MAX_FILE_SIZE: int = Field(default=52428800, description="Maximum supported PDF size in bytes (50MB)")
    PROCESSING_BATCH_SIZE: int = Field(default=32, description="Batch size for embedding generation")

    # AI, RAG & Chat Settings (Phase 4)
    GEMINI_API_KEY: str = Field(default="", description="Google Gemini API Key")
    GEMINI_MODEL_NAME: str = Field(default="gemini-2.0-flash", description="Google Gemini Model Name")
    QDRANT_URL: str = Field(default="http://localhost:6333", description="Qdrant vector DB URL")
    QDRANT_API_KEY: str = Field(default="", description="Qdrant API Key")
    QDRANT_COLLECTION_NAME: str = Field(default="lky_knowledge", description="Qdrant collection name")

    RETRIEVAL_TOP_K: int = Field(default=5, description="Number of vector chunks to retrieve per query")
    CONTEXT_TOKEN_BUDGET: int = Field(default=3000, description="Maximum context token budget for generation")
    CHAT_HISTORY_MAX_TURNS: int = Field(default=6, description="Max in-memory conversation turns retained per session")
    SIMILARITY_SCORE_THRESHOLD: float = Field(default=0.35, description="Minimum similarity score threshold for grounding")

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
