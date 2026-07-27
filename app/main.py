from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.core.config.settings import settings
from app.core.logging.logger import logger
from app.database.init_db import init_db
from app.database.session import check_database_connection
from app.middleware import RequestLoggingMiddleware, SecurityHeadersMiddleware
from app.exceptions.handlers import register_exception_handlers
from app.api.v1.router import api_router
from app.schemas.response import HealthResponse, PingResponse, SuccessResponse
from app.services.health_service import HealthService

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan lifecycle context handling initialization & graceful shutdown.
    """
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment Mode: Debug={settings.DEBUG}")

    # Database initialization & connection probe
    init_db()

    # Pre-warm SentenceTransformer embedding model & local vector retriever
    try:
        from app.retrieval.query_embedder.query_embedder import QueryEmbedder
        logger.info("Pre-warming QueryEmbedder sentence-transformer model during startup...")
        embedder = QueryEmbedder()
        embedder.embed_query("warmup")
        logger.info("QueryEmbedder pre-warmed successfully.")
    except Exception as exc:
        logger.warning(f"QueryEmbedder warmup warning: {exc}")

    yield

    logger.info(f"Shutting down {settings.APP_NAME}...")

app = FastAPI(
    title=settings.APP_NAME,
    description="Production-ready FastAPI backend architecture for Lee Kuan Yew AI Chatbot.",
    version=settings.APP_VERSION,
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    contact={
        "name": "AI Engineering Team",
        "url": "https://github.com",
    },
    license_info={
        "name": "MIT License",
    },
)

# Exception Handlers Registration
register_exception_handlers(app)

# Custom Middlewares
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API v1 Router Integration
app.include_router(api_router, prefix="/api/v1")

# Top-level Health Probes for Container Orchesration & Backward Compatibility
@app.get("/health", response_model=HealthResponse, tags=["Health"], summary="Root Health Probe")
async def root_health() -> HealthResponse:
    return HealthService.get_health()

@app.get("/ready", response_model=SuccessResponse[dict], tags=["Health"], summary="Root Readiness Probe")
async def root_ready() -> SuccessResponse[dict]:
    return SuccessResponse(
        message="System ready",
        data={"ready": check_database_connection()}
    )

@app.get("/version", response_model=SuccessResponse[dict], tags=["Health"], summary="Root Version Probe")
async def root_version() -> SuccessResponse[dict]:
    return SuccessResponse(
        message="API version metadata",
        data={"version": settings.APP_VERSION}
    )

@app.get("/ping", response_model=PingResponse, tags=["Health"], summary="Root Ping Probe")
async def root_ping() -> PingResponse:
    return PingResponse(message="pong")
