from app.database.session import engine, check_database_connection
from app.models.base import Base
from app.core.logging.logger import logger

def init_db() -> None:
    """
    Creates database schema tables on startup.
    """
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    if check_database_connection():
        logger.info("Database initialized successfully.")
    else:
        logger.warning("Database ping returned false during startup.")
