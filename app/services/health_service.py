import time
from app.core.config.settings import settings
from app.database.session import check_database_connection
from app.schemas.response import HealthResponse

START_TIME = time.time()

class HealthService:
    """
    Business service computing health, readiness, and system uptime.
    """
    @staticmethod
    def get_health() -> HealthResponse:
        db_status = "connected" if check_database_connection() else "disconnected"
        uptime = round(time.time() - START_TIME, 2)
        return HealthResponse(
            status="ok" if db_status == "connected" else "degraded",
            version=settings.APP_VERSION,
            database=db_status,
            uptime_seconds=uptime,
        )

    @staticmethod
    def is_ready() -> bool:
        return check_database_connection()
