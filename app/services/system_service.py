import sys
from app.core.config.settings import settings
from app.database.session import check_database_connection
from app.schemas.response import SystemInfoResponse

class SystemService:
    """
    Business service returning system telemetry and runtime environment info.
    """
    @staticmethod
    def get_system_info() -> SystemInfoResponse:
        return SystemInfoResponse(
            app_name=settings.APP_NAME,
            app_version=settings.APP_VERSION,
            debug_mode=settings.DEBUG,
            python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            database_status="healthy" if check_database_connection() else "unhealthy",
        )
