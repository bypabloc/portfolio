"""
FastAPI middleware utilities.

Common middleware for logging, request tracking, and CORS handling
optimized for Lambda environment.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/21
"""

import time
import uuid
from typing import Callable, Any
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from ..utils.logger import set_request_context, clear_request_context, get_request_id
import logging


def setup_cors_middleware(
    app: FastAPI,
    allowed_origins: list = None,
    allowed_methods: list = None,
    allowed_headers: list = None,
    allow_credentials: bool = True
) -> None:
    """
    Setup CORS middleware with sensible defaults.

    Args:
        app: FastAPI application
        allowed_origins: List of allowed origins
        allowed_methods: List of allowed methods
        allowed_headers: List of allowed headers
        allow_credentials: Allow credentials
    """
    if allowed_origins is None:
        allowed_origins = ["*"]  # Configure appropriately for production

    if allowed_methods is None:
        allowed_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]

    if allowed_headers is None:
        allowed_headers = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=allow_credentials,
        allow_methods=allowed_methods,
        allow_headers=allowed_headers,
    )


def setup_logging_middleware(app: FastAPI, logger: logging.Logger) -> None:
    """
    Setup logging middleware for request tracking.

    Args:
        app: FastAPI application
        logger: Logger instance
    """

    @app.middleware("http")
    async def logging_middleware(request: Request, call_next: Callable) -> Response:
        """
        Log all requests with timing and context.

        Args:
            request: FastAPI request
            call_next: Next middleware/handler

        Returns:
            Response with timing headers
        """
        # Generate request ID and set context
        request_id = str(uuid.uuid4())
        set_request_context(request_id=request_id)

        # Extract useful request info
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")

        # Start timing
        start_time = time.time()

        # Log request start
        logger.info(
            f"Request started: {request.method} {request.url.path}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "query_params": str(request.query_params),
                "client_ip": client_ip,
                "user_agent": user_agent,
                "event_type": "request_started"
            }
        )

        try:
            # Process request
            response = await call_next(request)

            # Calculate processing time
            process_time = time.time() - start_time
            process_time_ms = round(process_time * 1000, 2)

            # Add timing header
            response.headers["X-Process-Time"] = str(process_time_ms)
            response.headers["X-Request-ID"] = request_id

            # Log request completion
            log_level = logging.INFO
            if response.status_code >= 400:
                log_level = logging.WARNING if response.status_code < 500 else logging.ERROR

            logger.log(
                log_level,
                f"Request completed: {request.method} {request.url.path} - {response.status_code}",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "process_time_ms": process_time_ms,
                    "slow_request": process_time_ms > 1000,
                    "event_type": "request_completed"
                }
            )

            return response

        except Exception as e:
            # Calculate processing time even for errors
            process_time = time.time() - start_time
            process_time_ms = round(process_time * 1000, 2)

            # Log request error
            logger.error(
                f"Request failed: {request.method} {request.url.path} - {str(e)}",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "process_time_ms": process_time_ms,
                    "event_type": "request_failed"
                },
                exc_info=True
            )

            # Re-raise the exception
            raise

        finally:
            # Clear request context
            clear_request_context()


def setup_security_headers_middleware(app: FastAPI) -> None:
    """
    Setup security headers middleware.

    Args:
        app: FastAPI application
    """

    @app.middleware("http")
    async def security_headers_middleware(request: Request, call_next: Callable) -> Response:
        """
        Add security headers to responses.

        Args:
            request: FastAPI request
            call_next: Next middleware/handler

        Returns:
            Response with security headers
        """
        response = await call_next(request)

        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Add CSP header for API endpoints
        if request.url.path.startswith("/api/"):
            response.headers["Content-Security-Policy"] = "default-src 'none'"

        return response


def setup_rate_limiting_middleware(app: FastAPI, requests_per_minute: int = 60) -> None:
    """
    Setup basic rate limiting middleware (simple in-memory implementation).

    Args:
        app: FastAPI application
        requests_per_minute: Maximum requests per minute per IP

    Note:
        This is a simple implementation. For production, consider using
        Redis-based rate limiting or AWS API Gateway throttling.
    """
    from collections import defaultdict, deque
    from time import time

    # Simple in-memory rate limiting
    request_counts = defaultdict(deque)

    @app.middleware("http")
    async def rate_limiting_middleware(request: Request, call_next: Callable) -> Response:
        """
        Rate limiting middleware.

        Args:
            request: FastAPI request
            call_next: Next middleware/handler

        Returns:
            Response or rate limit error
        """
        client_ip = request.client.host if request.client else "unknown"
        current_time = time()
        minute_ago = current_time - 60

        # Clean old requests
        while request_counts[client_ip] and request_counts[client_ip][0] < minute_ago:
            request_counts[client_ip].popleft()

        # Check rate limit
        if len(request_counts[client_ip]) >= requests_per_minute:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Too many requests per minute."
            )

        # Add current request
        request_counts[client_ip].append(current_time)

        return await call_next(request)