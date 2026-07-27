import sys
from pathlib import Path
from loguru import logger
from app.core.config.settings import settings

def setup_logging():
    """
    Configures Loguru logging format and handlers.
    """
    # Ensure logs directory exists
    Path("logs").mkdir(exist_ok=True)

    # Remove default standard logger handlers
    logger.remove()

    # Console stdout handler
    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL.upper(),
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
        backtrace=settings.DEBUG,
        diagnose=settings.DEBUG,
    )

    # File logger handler
    logger.add(
        "logs/app.log",
        rotation="10 MB",
        retention="7 days",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
        compression="zip",
        enqueue=True,
    )

    return logger

# Initialize default loguru logger
setup_logging()
