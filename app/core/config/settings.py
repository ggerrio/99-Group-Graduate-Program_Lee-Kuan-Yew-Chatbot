"""
Application Settings Configuration
=================================
Centralized configuration for the Lee Kuan Yew AI Chatbot backend.
All environment-sensitive values are loaded from environment variables
with sensible defaults for local development.
"""

import os
from pathlib import Path
from typing import List, Optional, Union
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """Production-ready settings with environment variable overrides."""

    # ── Application Identity ──────────────────────────────────────────
    APP_NAME: str = "Lee Kuan Yew AI Chatbot"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, description="Enable debug mode")

    # ── Server Configuration ────────────────────────────────────────────
    HOST: str = "0.0.0.0"
    PORT: int = Field(default=8000, description="Server port (overridden by Railway $PORT)")

    # ── CORS Configuration ──────────────────────────────────────────────
    # CRITICAL: Must include your Vercel production & preview domains
    ALLOWED_ORIGINS: Union[List[str], str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
            "https://lky-chatbot.vercel.app",
            "https://*.vercel.app",
        ],
        description="Allowed CORS origins. Override in production via env var."
    )

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                import json
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return ["*"]

    # ── Retrieval & Ingestion Configuration ──────────────────────────────
    EMBEDDING_MODEL: str = Field(default="BAAI/bge-small-en-v1.5", description="HuggingFace embedding model name")
    HF_TOKEN: str = Field(default="", description="Optional HuggingFace Hub API Token")
    KNOWLEDGE_DIR: str = Field(default="./knowledge", description="Source raw PDF knowledge directory")
    PROCESSED_DIR: str = Field(default="processed", description="Relative path to processed data directory")
    CHUNK_SIZE: int = Field(default=750, description="Target chunk size")
    CHUNK_OVERLAP: int = Field(default=150, description="Chunk overlap size")
    MAX_FILE_SIZE: int = Field(default=52428800, description="Max file size in bytes")
    PROCESSING_BATCH_SIZE: int = Field(default=32, description="Batch size for embedding generation")
    RETRIEVAL_TOP_K: int = Field(default=5, description="Number of top chunks to retrieve per query")
    CONTEXT_TOKEN_BUDGET: int = Field(default=3000, description="Maximum context token budget for generation")
    CHAT_HISTORY_MAX_TURNS: int = Field(default=6, description="Max in-memory conversation turns retained per session")
    SIMILARITY_SCORE_THRESHOLD: float = Field(default=0.35, description="Minimum similarity score threshold for grounding")

    # ── Gemini LLM Configuration ──────────────────────────────────────
    GEMINI_API_KEY: Optional[str] = Field(default=None, description="Google Gemini API key")
    GEMINI_MODEL_NAME: str = Field(default="gemini-2.0-flash", description="Gemini model identifier")
    GEMINI_TEMPERATURE: float = Field(default=0.3, ge=0.0, le=2.0)
    GEMINI_MAX_OUTPUT_TOKENS: int = Field(default=2048, ge=1, le=8192)

    # ── Database (Optional / Legacy) ────────────────────────────────────
    DATABASE_URL: Optional[str] = Field(
        default="sqlite:///./lky_chatbot.db",
        description="Database URL. Set to empty string to disable DB in production."
    )

    # ── Logging ─────────────────────────────────────────────────────────
    LOG_LEVEL: str = Field(default="INFO", description="Logging level: DEBUG, INFO, WARNING, ERROR")

    # ── Pydantic Settings Config ────────────────────────────────────────
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore",  # Allow extra env vars without raising errors
    }

    @property
    def processed_dir_path(self) -> Path:
        """Resolve PROCESSED_DIR to an absolute Path object."""
        return Path(self.PROCESSED_DIR).resolve()


# Singleton instance — import this everywhere
settings = Settings()