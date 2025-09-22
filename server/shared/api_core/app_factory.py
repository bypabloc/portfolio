"""
FastAPI application factory for Lambda services.

Provides standardized FastAPI application creation with common
configuration, middleware, and error handling.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/21
"""

from typing import Optional, List, Dict, Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from ..utils.logger import get_logger, set_request_context
from .middleware import setup_logging_middleware
from .responses import ErrorResponse


def create_fastapi_app(
    title: str,
    description: str,
    version: str = "1.0.0",
    service_name: Optional[str] = None,
    allowed_origins: Optional[List[str]] = None,
    trusted_hosts: Optional[List[str]] = None,
    debug: bool = False,
) -> FastAPI:
    """
    Create FastAPI application with standard configuration.

    Args:
        title: Application title
        description: Application description
        version: Application version
        service_name: Service name for logging (defaults to title)
        allowed_origins: CORS allowed origins
        trusted_hosts: Trusted host headers
        debug: Enable debug mode

    Returns:
        Configured FastAPI application
    """
    if service_name is None:
        service_name = title.lower().replace(" ", "-")

    # Create logger for the service
    logger = get_logger(service_name)

    # Initialize request context
    set_request_context()

    app = FastAPI(
        title=title,
        description=description,
        version=version,
        debug=debug,
        docs_url="/docs" if debug else None,
        redoc_url="/redoc" if debug else None,
        openapi_url="/openapi.json" if debug else None,
    )

    # Setup CORS middleware
    if allowed_origins is None:
        allowed_origins = ["*"]  # Configure appropriately for production

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Setup trusted hosts
    if trusted_hosts:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=trusted_hosts
        )

    # Setup logging middleware
    setup_logging_middleware(app, logger)

    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        """Global exception handler for unhandled errors."""
        logger.error(
            f"Unhandled exception: {str(exc)}",
            extra={
                "path": request.url.path,
                "method": request.method,
                "error_type": type(exc).__name__,
                "event_type": "unhandled_exception"
            },
            exc_info=True
        )

        return ErrorResponse(
            success=False,
            error="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500
        ).to_json_response()

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        from ..utils.datetime_utils import get_current_utc_timestamp

        return {
            "status": "healthy",
            "service": service_name,
            "version": version,
            "timestamp": get_current_utc_timestamp()
        }

    logger.info(
        f"FastAPI application '{title}' created successfully",
        extra={
            "service": service_name,
            "version": version,
            "debug": debug,
            "event_type": "app_created"
        }
    )

    return app


def configure_openapi(app: FastAPI, service_name: str) -> None:
    """
    Configure OpenAPI documentation with additional metadata.

    Args:
        app: FastAPI application
        service_name: Service name for documentation
    """
    def custom_openapi() -> Dict[str, Any]:
        if app.openapi_schema:
            return app.openapi_schema

        from fastapi.openapi.utils import get_openapi

        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )

        # Add custom metadata
        openapi_schema["info"]["x-service-name"] = service_name
        openapi_schema["info"]["contact"] = {
            "name": "Pablo Contreras",
            "email": "pablo@bypabloc.dev"
        }

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi