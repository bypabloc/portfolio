"""
FastAPI dependency injection utilities.

Common dependencies for logging, request tracking, and validation
across all Lambda services.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/21
"""

from typing import Optional, Annotated
from fastapi import Depends, Request, Header, HTTPException
from ..utils.logger import get_logger, get_request_id
import logging


def get_request_logger(request: Request) -> logging.Logger:
    """
    Get logger for the current request.

    Args:
        request: FastAPI request object

    Returns:
        Logger instance with request context
    """
    # Extract service name from request path or use default
    path_parts = request.url.path.strip("/").split("/")
    service_name = path_parts[0] if path_parts and path_parts[0] else "api"

    return get_logger(service_name)


def get_current_request_id() -> Optional[str]:
    """
    Get current request ID from context.

    Returns:
        Request ID string or None
    """
    return get_request_id()


def validate_content_type(
    content_type: Annotated[Optional[str], Header()] = None
) -> Optional[str]:
    """
    Validate request content type.

    Args:
        content_type: Content-Type header value

    Returns:
        Validated content type

    Raises:
        HTTPException: If content type is invalid for POST/PUT requests
    """
    return content_type


def get_user_agent(
    user_agent: Annotated[Optional[str], Header(alias="User-Agent")] = None
) -> Optional[str]:
    """
    Get user agent from request headers.

    Args:
        user_agent: User-Agent header value

    Returns:
        User agent string
    """
    return user_agent


def get_client_ip(request: Request) -> str:
    """
    Get client IP address from request.

    Args:
        request: FastAPI request object

    Returns:
        Client IP address
    """
    # Check for forwarded IP headers (common in Lambda/API Gateway)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # Take the first IP in the chain
        return forwarded_for.split(",")[0].strip()

    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip.strip()

    # Fallback to direct client IP
    return request.client.host if request.client else "unknown"


def require_json_content_type(
    content_type: Annotated[Optional[str], Header()] = None
) -> str:
    """
    Require JSON content type for requests.

    Args:
        content_type: Content-Type header value

    Returns:
        Validated content type

    Raises:
        HTTPException: If content type is not JSON
    """
    if not content_type or not content_type.startswith("application/json"):
        raise HTTPException(
            status_code=415,
            detail="Content-Type must be application/json"
        )
    return content_type


def get_api_version(
    request: Request,
    api_version: Annotated[Optional[str], Header(alias="API-Version")] = None
) -> str:
    """
    Get API version from header or path.

    Args:
        request: FastAPI request object
        api_version: API-Version header value

    Returns:
        API version string
    """
    if api_version:
        return api_version

    # Extract version from path (e.g., /v1/resource)
    path_parts = request.url.path.strip("/").split("/")
    for part in path_parts:
        if part.startswith("v") and part[1:].isdigit():
            return part

    return "v1"  # Default version


def validate_request_size(
    request: Request,
    max_size_mb: int = 10
) -> Request:
    """
    Validate request body size.

    Args:
        request: FastAPI request object
        max_size_mb: Maximum request size in MB

    Returns:
        Validated request

    Raises:
        HTTPException: If request is too large
    """
    content_length = request.headers.get("Content-Length")
    if content_length:
        try:
            size_bytes = int(content_length)
            max_size_bytes = max_size_mb * 1024 * 1024

            if size_bytes > max_size_bytes:
                raise HTTPException(
                    status_code=413,
                    detail=f"Request body too large. Maximum size: {max_size_mb}MB"
                )
        except ValueError:
            # Invalid Content-Length header
            pass

    return request


def get_correlation_id(
    correlation_id: Annotated[Optional[str], Header(alias="X-Correlation-ID")] = None
) -> Optional[str]:
    """
    Get correlation ID for request tracking.

    Args:
        correlation_id: X-Correlation-ID header value

    Returns:
        Correlation ID or current request ID
    """
    return correlation_id or get_request_id()


# Common dependency combinations
RequestLogger = Annotated[logging.Logger, Depends(get_request_logger)]
ClientIP = Annotated[str, Depends(get_client_ip)]
UserAgent = Annotated[Optional[str], Depends(get_user_agent)]
ContentType = Annotated[Optional[str], Depends(validate_content_type)]
JSONContentType = Annotated[str, Depends(require_json_content_type)]
APIVersion = Annotated[str, Depends(get_api_version)]
CorrelationID = Annotated[Optional[str], Depends(get_correlation_id)]
ValidatedRequest = Annotated[Request, Depends(validate_request_size)]


def create_pagination_dependency(
    max_page_size: int = 100,
    default_page_size: int = 20
):
    """
    Create pagination dependency with configurable limits.

    Args:
        max_page_size: Maximum items per page
        default_page_size: Default items per page

    Returns:
        Pagination dependency function
    """

    def get_pagination(
        page: int = 1,
        page_size: int = default_page_size,
        offset: Optional[int] = None
    ) -> dict:
        """
        Get pagination parameters.

        Args:
            page: Page number (1-based)
            page_size: Items per page
            offset: Optional offset override

        Returns:
            Pagination parameters

        Raises:
            HTTPException: If parameters are invalid
        """
        if page < 1:
            raise HTTPException(
                status_code=400,
                detail="Page number must be greater than 0"
            )

        if page_size < 1 or page_size > max_page_size:
            raise HTTPException(
                status_code=400,
                detail=f"Page size must be between 1 and {max_page_size}"
            )

        # Calculate offset if not provided
        if offset is None:
            offset = (page - 1) * page_size

        return {
            "page": page,
            "page_size": page_size,
            "offset": offset,
            "limit": page_size
        }

    return get_pagination


# Default pagination dependency
Pagination = Annotated[dict, Depends(create_pagination_dependency())]