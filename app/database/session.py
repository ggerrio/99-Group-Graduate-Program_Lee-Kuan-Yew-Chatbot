from pathlib import Path
from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import sessionmaker, Session
from app.core.config.settings import settings
from app.core.logging.logger import logger

db_url = (settings.DATABASE_URL or "").strip()

if not db_url:
    err_msg = (
        "DATABASE_URL environment variable is missing or empty. "
        "Please set a valid DATABASE_URL (e.g. 'sqlite:///./lky_chatbot.db') in your deployment platform's environment variables."
    )
    logger.error(err_msg)
    raise ValueError(err_msg)

# Ensure parent directory exists for SQLite database files
is_sqlite = db_url.startswith("sqlite")
if is_sqlite:
    sqlite_path_str = db_url.replace("sqlite:///", "").split("?")[0]
    if sqlite_path_str and sqlite_path_str != ":memory:":
        db_file_path = Path(sqlite_path_str)
        if db_file_path.parent and not db_file_path.parent.exists():
            try:
                db_file_path.parent.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created SQLite database directory: '{db_file_path.parent.absolute()}'")
            except Exception as exc:
                logger.warning(f"Could not create SQLite directory '{db_file_path.parent}': {exc}")

connect_args = {"check_same_thread": False} if is_sqlite else {}

try:
    engine = create_engine(
        db_url,
        connect_args=connect_args,
        pool_pre_ping=True,
        echo=settings.DEBUG,
    )
except ArgumentError as exc:
    err_msg = (
        f"Could not parse DATABASE_URL from string '{db_url}'. "
        f"Please verify your DATABASE_URL environment variable syntax in your deployment platform. Error: {exc}"
    )
    logger.error(err_msg)
    raise ValueError(err_msg) from exc

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)

def get_db() -> Generator[Session, None, None]:
    """
    Dependency injection generator yielding transactional database sessions.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as exc:
        db.rollback()
        logger.error(f"Database session error: {exc}")
        raise
    finally:
        db.close()

def check_database_connection() -> bool:
    """
    Executes a ping query to verify database engine connectivity.
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception as exc:
        logger.error(f"Database connectivity check failed: {exc}")
        return False
