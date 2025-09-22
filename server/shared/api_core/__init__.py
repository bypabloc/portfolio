"""
API Core utilities for FastAPI Lambda services.

Provides common FastAPI patterns, middleware, and utilities optimized
for AWS Lambda environment.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/21
"""

from .app_factory import create_fastapi_app
from .middleware import setup_cors_middleware, setup_logging_middleware
from .responses import APIResponse, ErrorResponse, create_success_response, create_error_response
from .dependencies import get_request_logger, get_request_id
from .fastapi_deps import (
    FastAPI,
    HTTPException,
    Depends,
    Query,
    Path,
    Body,
    Header,
    Request,
    Response,
    JSONResponse,
    StatusCodes,
    CommonQuery,
    CommonPath,
    CommonHeaders
)

__all__ = [
    # App factory and middleware
    "create_fastapi_app",
    "setup_cors_middleware",
    "setup_logging_middleware",

    # Response utilities
    "APIResponse",
    "ErrorResponse",
    "create_success_response",
    "create_error_response",

    # Dependencies
    "get_request_logger",
    "get_request_id",

    # FastAPI core imports
    "FastAPI",
    "HTTPException",
    "Depends",
    "Query",
    "Path",
    "Body",
    "Header",
    "Request",
    "Response",
    "JSONResponse",

    # Utilities
    "StatusCodes",
    "CommonQuery",
    "CommonPath",
    "CommonHeaders"
]