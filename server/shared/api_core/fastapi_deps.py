"""
FastAPI common imports and dependencies.

Centralized location for commonly used FastAPI imports to avoid
repetition across microservices.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/21
"""

# Core FastAPI imports
from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    Query,
    Path,
    Body,
    Header,
    Cookie,
    Form,
    File,
    UploadFile,
    Request,
    Response,
    BackgroundTasks,
    Security,
    status
)

# FastAPI response types
from fastapi.responses import (
    JSONResponse,
    HTMLResponse,
    PlainTextResponse,
    RedirectResponse,
    StreamingResponse,
    FileResponse
)

# FastAPI middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware

# FastAPI security
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    APIKeyHeader,
    APIKeyQuery,
    APIKeyCookie
)

# FastAPI exceptions
from fastapi.exceptions import (
    RequestValidationError,
    HTTPException as FastAPIHTTPException,
    ValidationException
)

# Re-export commonly used items
__all__ = [
    # Core
    "FastAPI",
    "HTTPException",
    "Depends",
    "Query",
    "Path",
    "Body",
    "Header",
    "Cookie",
    "Form",
    "File",
    "UploadFile",
    "Request",
    "Response",
    "BackgroundTasks",
    "Security",
    "status",

    # Responses
    "JSONResponse",
    "HTMLResponse",
    "PlainTextResponse",
    "RedirectResponse",
    "StreamingResponse",
    "FileResponse",

    # Middleware
    "CORSMiddleware",
    "TrustedHostMiddleware",
    "GZipMiddleware",

    # Security
    "HTTPBearer",
    "HTTPAuthorizationCredentials",
    "HTTPBasic",
    "HTTPBasicCredentials",
    "OAuth2PasswordBearer",
    "OAuth2PasswordRequestForm",
    "APIKeyHeader",
    "APIKeyQuery",
    "APIKeyCookie",

    # Exceptions
    "RequestValidationError",
    "FastAPIHTTPException",
    "ValidationException"
]


# Common status codes for convenience
class StatusCodes:
    """HTTP status codes for API responses."""

    # Success
    OK = status.HTTP_200_OK
    CREATED = status.HTTP_201_CREATED
    ACCEPTED = status.HTTP_202_ACCEPTED
    NO_CONTENT = status.HTTP_204_NO_CONTENT

    # Client Error
    BAD_REQUEST = status.HTTP_400_BAD_REQUEST
    UNAUTHORIZED = status.HTTP_401_UNAUTHORIZED
    FORBIDDEN = status.HTTP_403_FORBIDDEN
    NOT_FOUND = status.HTTP_404_NOT_FOUND
    METHOD_NOT_ALLOWED = status.HTTP_405_METHOD_NOT_ALLOWED
    CONFLICT = status.HTTP_409_CONFLICT
    UNPROCESSABLE_ENTITY = status.HTTP_422_UNPROCESSABLE_ENTITY
    TOO_MANY_REQUESTS = status.HTTP_429_TOO_MANY_REQUESTS

    # Server Error
    INTERNAL_SERVER_ERROR = status.HTTP_500_INTERNAL_SERVER_ERROR
    BAD_GATEWAY = status.HTTP_502_BAD_GATEWAY
    SERVICE_UNAVAILABLE = status.HTTP_503_SERVICE_UNAVAILABLE
    GATEWAY_TIMEOUT = status.HTTP_504_GATEWAY_TIMEOUT


# Common query parameters
class CommonQuery:
    """Common query parameter factories."""

    @staticmethod
    def page(default: int = 1, description: str = "Page number (1-based)"):
        """Page number query parameter."""
        return Query(default, ge=1, description=description)

    @staticmethod
    def page_size(default: int = 20, max_size: int = 100, description: str = "Items per page"):
        """Page size query parameter."""
        return Query(default, ge=1, le=max_size, description=description)

    @staticmethod
    def skip(default: int = 0, description: str = "Number of items to skip"):
        """Skip query parameter for offset-based pagination."""
        return Query(default, ge=0, description=description)

    @staticmethod
    def limit(default: int = 20, max_limit: int = 100, description: str = "Maximum number of items"):
        """Limit query parameter."""
        return Query(default, ge=1, le=max_limit, description=description)

    @staticmethod
    def search(description: str = "Search query", min_length: int = 2):
        """Search query parameter."""
        return Query(None, min_length=min_length, description=description)

    @staticmethod
    def sort(default: str = "id", description: str = "Sort field"):
        """Sort field query parameter."""
        return Query(default, description=description)

    @staticmethod
    def order(default: str = "asc", description: str = "Sort order (asc/desc)"):
        """Sort order query parameter."""
        return Query(default, regex="^(asc|desc)$", description=description)


# Common path parameters
class CommonPath:
    """Common path parameter factories."""

    @staticmethod
    def id(description: str = "Resource ID"):
        """Resource ID path parameter."""
        return Path(..., description=description)

    @staticmethod
    def uuid_id(description: str = "Resource UUID"):
        """UUID path parameter."""
        return Path(..., regex=r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", description=description)

    @staticmethod
    def slug(description: str = "Resource slug"):
        """Slug path parameter."""
        return Path(..., regex=r"^[a-z0-9-]+$", description=description)


# Common header parameters
class CommonHeaders:
    """Common header parameter factories."""

    @staticmethod
    def content_type(default: str = "application/json"):
        """Content-Type header parameter."""
        return Header(default, alias="Content-Type")

    @staticmethod
    def user_agent():
        """User-Agent header parameter."""
        return Header(None, alias="User-Agent")

    @staticmethod
    def authorization():
        """Authorization header parameter."""
        return Header(None, alias="Authorization")

    @staticmethod
    def api_key():
        """API key header parameter."""
        return Header(None, alias="X-API-Key")

    @staticmethod
    def correlation_id():
        """Correlation ID header parameter."""
        return Header(None, alias="X-Correlation-ID")