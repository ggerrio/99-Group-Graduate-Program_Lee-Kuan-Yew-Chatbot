import os
from typing import List

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
except ImportError:
    try:
        from pydantic.v1 import BaseSettings
        SettingsConfigDict = None
    except ImportError:
        from pydantic import BaseSettings
        SettingsConfigDict = None

class Settings(BaseSettings):
    PROJECT_NAME: str = "Lee Kuan Yew AI Chatbot"
    API_V1_STR: str = "/api/v1"
    VERSION: str = "0.1.0"
    
    # Logging & DB Settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./lky_chatbot.db")
    
    # Future Phase AI / Vector DB Settings
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    if SettingsConfigDict is not None:
        model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
            case_sensitive=True,
            extra="ignore"
        )
    else:
        class Config:
            env_file = ".env"
            case_sensitive = True
            extra = "ignore"

settings = Settings()

