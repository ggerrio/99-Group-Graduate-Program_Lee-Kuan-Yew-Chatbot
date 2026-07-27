import uuid
from fastapi import Request
from app.core.logging.logger import logger

def get_request_id(request: Request) -> str:
    """
    Extracts or generates X-Request-ID header.
    """
    return request.headers.get("X-Request-ID", str(uuid.uuid4()))

def get_logger():
    """
    Returns application logger.
    """
    return logger
