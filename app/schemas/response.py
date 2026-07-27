from typing import Generic, TypeVar, Optional, Dict, Any, List
from pydantic import BaseModel, Field
from app.utils.datetime import get_utc_now_iso

T = TypeVar("T")

class ResponseBase(BaseModel):
    success: bool = Field(default=True, description="Indicates request success status")
    message: str = Field(default="Operation completed successfully", description="Status message")
    timestamp: str = Field(default_factory=get_utc_now_iso, description="ISO UTC Timestamp")

class SuccessResponse(ResponseBase, Generic[T]):
    data: Optional[T] = Field(default=None, description="Payload data")

class ErrorResponse(ResponseBase):
    success: bool = Field(default=False, description="Always false for errors")
    details: Dict[str, Any] = Field(default_factory=dict, description="Detailed error information or validation errors")

class PaginatedResponse(SuccessResponse[List[T]], Generic[T]):
    total: int = Field(default=0, description="Total record count")
    page: int = Field(default=1, description="Current page number")
    size: int = Field(default=20, description="Page size limit")

class HealthResponse(BaseModel):
    status: str = Field(default="ok", json_schema_extra={"example": "ok"})
    version: str = Field(default="0.2.0")
    database: str = Field(default="connected")
    uptime_seconds: float = Field(default=0.0)
    timestamp: str = Field(default_factory=get_utc_now_iso)

class SystemInfoResponse(BaseModel):
    app_name: str
    app_version: str
    debug_mode: bool
    python_version: str
    database_status: str

class PingResponse(BaseModel):
    message: str = Field(default="pong")
    timestamp: str = Field(default_factory=get_utc_now_iso)
