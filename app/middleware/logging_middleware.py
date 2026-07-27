import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging.logger import logger

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware logging every HTTP request method, URL, status code, latency, and Request ID.
    """
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        start_time = time.time()

        logger.info(f"--> [{request_id}] {request.method} {request.url.path}")

        try:
            response = await call_next(request)
            duration_ms = round((time.time() - start_time) * 1000, 2)
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time-Ms"] = str(duration_ms)

            logger.info(
                f"<-- [{request_id}] {request.method} {request.url.path} - Status {response.status_code} ({duration_ms}ms)"
            )
            return response
        except Exception as exc:
            duration_ms = round((time.time() - start_time) * 1000, 2)
            logger.error(
                f"x-- [{request_id}] {request.method} {request.url.path} Exception: {exc} ({duration_ms}ms)"
            )
            raise
