from fastapi import APIRouter, status
from app.services.health_service import HealthService
from app.services.system_service import SystemService
from app.schemas.response import HealthResponse, SystemInfoResponse, PingResponse, SuccessResponse
from app.exceptions.exceptions import DatabaseException

router = APIRouter()

@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Application Health Status",
    description="Returns detailed health metrics including database status and uptime.",
)
async def get_health() -> HealthResponse:
    return HealthService.get_health()

@router.get(
    "/ready",
    response_model=SuccessResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="Readiness Probe",
    description="Verifies whether database and system dependencies are ready to serve traffic.",
)
async def get_readiness() -> SuccessResponse[dict]:
    ready = HealthService.is_ready()
    if not ready:
        raise DatabaseException(message="Database engine ping failed")
    return SuccessResponse(
        message="System is ready",
        data={"ready": True, "database": "connected"}
    )

@router.get(
    "/version",
    response_model=SuccessResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="API Version Metrics",
    description="Returns current API semver version.",
)
async def get_version() -> SuccessResponse[dict]:
    health_data = HealthService.get_health()
    return SuccessResponse(
        message="API version metadata",
        data={"version": health_data.version}
    )

@router.get(
    "/ping",
    response_model=PingResponse,
    status_code=status.HTTP_200_OK,
    summary="Ping Probe",
    description="Lightweight ping endpoint returning pong.",
)
async def get_ping() -> PingResponse:
    return PingResponse(message="pong")

@router.get(
    "/system",
    response_model=SystemInfoResponse,
    status_code=status.HTTP_200_OK,
    summary="System Telemetry Information",
    description="Returns environment telemetry, Python runtime, and app configuration mode.",
)
async def get_system_info() -> SystemInfoResponse:
    return SystemService.get_system_info()
