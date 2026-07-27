import logging
import sys
from app.core.config import settings

def setup_logging() -> logging.Logger:
    """
    Configures structured logging for the application.
    """
    log_level_str = settings.LOG_LEVEL.upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    logger = logging.getLogger("lky_chatbot")
    logger.setLevel(log_level)

    # Avoid duplicated log handlers if initialized multiple times
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

logger = setup_logging()
