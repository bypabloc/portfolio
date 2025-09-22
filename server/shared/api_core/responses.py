"""
Standardized API response utilities.

Provides consistent response formats for all FastAPI Lambda services
with proper error handling and metadata.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/21
"""

from typing import Any, Optional, Dict, Union
from datetime import datetime, timezone
from fastapi import Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from ..utils.logger import get_request_id


class APIResponse(BaseModel):
    """Standard API response model."""

    success: bool = Field(description="Operation success indicator")
    data: Optional[Any] = Field(default=None, description="Response data")
    error: Optional[str] = Field(default=None, description="Error message")
    error_code: Optional[str] = Field(default=None, description="Error code")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    request_id: Optional[str] = Field(default_factory=get_request_id, description="Request correlation ID")

    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        response_dict = {
            "success": self.success,
            "timestamp": self.timestamp.isoformat(),
        }

        if self.request_id:
            response_dict["request_id"] = self.request_id

        if self.success:
            response_dict["data"] = self.data
            if self.metadata:
                response_dict["metadata"] = self.metadata
        else:
            response_dict["error"] = self.error
            if self.error_code:
                response_dict["error_code"] = self.error_code

        return response_dict

    def to_json_response(self, status_code: int = 200) -> JSONResponse:
        """Convert to FastAPI JSONResponse."""
        return JSONResponse(
            content=self.to_dict(),
            status_code=status_code,
            headers={
                "X-Request-ID": self.request_id or "unknown",
                "Content-Type": "application/json"
            }
        )


class SuccessResponse(APIResponse):
    """Success response model."""

    success: bool = Field(default=True, const=True)

    def __init__(self, data: Any = None, metadata: Optional[Dict[str, Any]] = None, **kwargs):
        super().__init__(success=True, data=data, metadata=metadata, **kwargs)


class ErrorResponse(APIResponse):
    """Error response model."""

    success: bool = Field(default=False, const=True)

    def __init__(
        self,
        error: str,
        error_code: Optional[str] = None,
        status_code: int = 400,
        **kwargs
    ):
        super().__init__(
            success=False,
            error=error,
            error_code=error_code,
            **kwargs
        )
        self.status_code = status_code

    def to_json_response(self, status_code: Optional[int] = None) -> JSONResponse:
        """Convert to FastAPI JSONResponse with error status code."""
        return super().to_json_response(
            status_code=status_code or getattr(self, 'status_code', 400)
        )


def create_success_response(
    data: Any = None,
    metadata: Optional[Dict[str, Any]] = None,
    status_code: int = 200
) -> JSONResponse:
    """
    Create successful response.

    Args:
        data: Response data
        metadata: Additional metadata
        status_code: HTTP status code

    Returns:
        JSONResponse with success format
    """
    response = SuccessResponse(data=data, metadata=metadata)
    return response.to_json_response(status_code=status_code)


def create_error_response(
    error: str,
    error_code: Optional[str] = None,
    status_code: int = 400,
    details: Optional[Dict[str, Any]] = None
) -> JSONResponse:
    """
    Create error response.

    Args:
        error: Error message
        error_code: Error code for client handling
        status_code: HTTP status code
        details: Additional error details

    Returns:
        JSONResponse with error format
    """
    metadata = {"details": details} if details else None
    response = ErrorResponse(
        error=error,
        error_code=error_code,
        status_code=status_code
    )
    if metadata:
        response.metadata = metadata

    return response.to_json_response(status_code=status_code)


def create_validation_error_response(
    errors: list,
    message: str = "Validation failed"
) -> JSONResponse:
    """
    Create validation error response.

    Args:
        errors: List of validation errors
        message: Main error message

    Returns:
        JSONResponse with validation error format
    """
    return create_error_response(
        error=message,
        error_code="VALIDATION_ERROR",
        status_code=422,
        details={"validation_errors": errors}
    )


def create_not_found_response(
    resource: str = "Resource",
    resource_id: Optional[str] = None
) -> JSONResponse:
    """
    Create not found error response.

    Args:
        resource: Resource name
        resource_id: Resource identifier

    Returns:
        JSONResponse with not found error
    """
    message = f"{resource} not found"
    if resource_id:
        message += f" with ID: {resource_id}"

    return create_error_response(
        error=message,
        error_code="NOT_FOUND",
        status_code=404
    )


def create_conflict_response(
    resource: str = "Resource",
    reason: str = "already exists"
) -> JSONResponse:
    """
    Create conflict error response.

    Args:
        resource: Resource name
        reason: Conflict reason

    Returns:
        JSONResponse with conflict error
    """
    return create_error_response(
        error=f"{resource} {reason}",
        error_code="CONFLICT",
        status_code=409
    )


def create_unauthorized_response(
    message: str = "Authentication required"
) -> JSONResponse:
    """
    Create unauthorized error response.

    Args:
        message: Error message

    Returns:
        JSONResponse with unauthorized error
    """
    return create_error_response(
        error=message,
        error_code="UNAUTHORIZED",
        status_code=401
    )


def create_forbidden_response(
    message: str = "Access forbidden"
) -> JSONResponse:
    """
    Create forbidden error response.

    Args:
        message: Error message

    Returns:
        JSONResponse with forbidden error
    """
    return create_error_response(
        error=message,
        error_code="FORBIDDEN",
        status_code=403
    )


def create_internal_error_response(
    message: str = "Internal server error",
    error_id: Optional[str] = None
) -> JSONResponse:
    """
    Create internal server error response.

    Args:
        message: Error message
        error_id: Error tracking ID

    Returns:
        JSONResponse with internal error
    """
    details = {"error_id": error_id} if error_id else None

    return create_error_response(
        error=message,
        error_code="INTERNAL_ERROR",
        status_code=500,
        details=details
    )


# Common response models for OpenAPI documentation
class HealthResponse(BaseModel):
    """Health check response model."""

    status: str = Field(description="Service health status")
    service: str = Field(description="Service name")
    version: str = Field(description="Service version")
    timestamp: datetime = Field(description="Response timestamp")
    uptime_seconds: Optional[float] = Field(default=None, description="Service uptime in seconds")


class PaginatedResponse(BaseModel):
    """Paginated response metadata."""

    page: int = Field(description="Current page number")
    page_size: int = Field(description="Items per page")
    total_items: int = Field(description="Total number of items")
    total_pages: int = Field(description="Total number of pages")
    has_next: bool = Field(description="Has next page")
    has_previous: bool = Field(description="Has previous page")


def create_paginated_response(
    data: list,
    page: int,
    page_size: int,
    total_items: int,
    status_code: int = 200
) -> JSONResponse:
    """
    Create paginated response.

    Args:
        data: Page data
        page: Current page number
        page_size: Items per page
        total_items: Total number of items
        status_code: HTTP status code

    Returns:
        JSONResponse with paginated format
    """
    total_pages = (total_items + page_size - 1) // page_size

    pagination = PaginatedResponse(
        page=page,
        page_size=page_size,
        total_items=total_items,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_previous=page > 1
    )

    return create_success_response(
        data=data,
        metadata={"pagination": pagination.dict()},
        status_code=status_code
    )