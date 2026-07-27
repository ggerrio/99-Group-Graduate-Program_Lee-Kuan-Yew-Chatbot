from fastapi import APIRouter
from app.api.v1.routers.health import router as health_router
from app.api.v1.routers.chat import router as chat_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["Health & System"])
api_router.include_router(chat_router)
