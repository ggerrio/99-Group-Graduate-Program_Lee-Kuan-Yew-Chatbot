from datetime import datetime, timezone

def get_utc_now_iso() -> str:
    """
    Returns current UTC timestamp formatted in ISO 8601 string.
    """
    return datetime.now(timezone.utc).isoformat()
