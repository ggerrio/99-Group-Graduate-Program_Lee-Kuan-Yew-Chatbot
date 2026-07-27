from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from app.exceptions.exceptions import AppException
from app.schemas.response import ErrorResponse
from app.core.logging.logger import logger

def register_exception_handlers(app: FastAPI) -> None:
    """
    Registers centralized exception handlers returning uniform JSON error responses.
    """
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        logger.warning(f"AppException on {request.url.path}: {exc.message}")
        error_res = ErrorResponse(message=exc.message, details=exc.details)
        return JSONResponse(status_code=exc.status_code, content=error_res.model_dump())

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.warning(f"HTTPException {exc.status_code} on {request.url.path}: {exc.detail}")
        error_res = ErrorResponse(message=str(exc.detail), details={})
        return JSONResponse(status_code=exc.status_code, content=error_res.model_dump())

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning(f"ValidationError on {request.url.path}: {exc.errors()}")
        error_res = ErrorResponse(
            message="Request parameter validation failed",
            details={"errors": exc.errors()},
        )
        return JSONResponse(status_code=422, content=error_res.model_dump())

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled Exception on {request.url.path}: {exc}")
        error_res = ErrorResponse(
            message="An unexpected server error occurred",
            details={"type": exc.__class__.__name__},
        )
        return JSONResponse(status_code=500, content=error_res.model_dump())
