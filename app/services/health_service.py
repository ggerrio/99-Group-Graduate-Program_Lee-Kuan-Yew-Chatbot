import time
from app.core.config.settings import settings
from app.database.session import check_database_connection
from app.schemas.response import HealthResponse

START_TIME = time.time()

class HealthService:
    """
    Business service computing health, readiness, and system uptime.
    Gracefully handles standalone RAG-only mode where database is optional.
    """
    @staticmethod
    def get_health() -> HealthResponse:
        db_status = "not_configured"
        status_val = "ok"

        if getattr(settings, "DATABASE_URL", None):
            try:
                db_ok = check_database_connection()
                db_status = "connected" if db_ok else "disconnected"
                if not db_ok:
                    status_val = "degraded"
            except Exception as exc:
                logger.warning(f"DB health check skipped or failed: {exc}")
                db_status = "skipped"
        
        uptime = round(time.time() - START_TIME, 2)
        return HealthResponse(
            status=status_val,
            version=settings.APP_VERSION,
            database=db_status,
            uptime_seconds=uptime,
        )

    @staticmethod
    def is_ready() -> bool:
        if getattr(settings, "DATABASE_URL", None):
            try:
                return check_database_connection()
            except Exception:
                return True
        return True
