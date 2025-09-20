"""
Logging configuration and utilities.

Provides structured logging setup optimized for AWS Lambda and local development
with correlation IDs and structured output.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/20
"""

import logging
import sys
import json
import uuid
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from aws_lambda_powertools import Logger as PowertoolsLogger
from aws_lambda_powertools.logging import correlation_paths
from contextvars import ContextVar
from functools import wraps

# Context variables for request tracking
request_id_var: ContextVar[Optional[str]] = ContextVar('request_id', default=None)
user_id_var: ContextVar[Optional[str]] = ContextVar('user_id', default=None)


class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured JSON logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured JSON."""
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add request context if available
        request_id = request_id_var.get()
        if request_id:
            log_data["request_id"] = request_id

        user_id = user_id_var.get()
        if user_id:
            log_data["user_id"] = user_id

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields if present
        if hasattr(record, 'extra') and record.extra:
            log_data.update(record.extra)

        return json.dumps(log_data, default=str)


class RequestContextFilter(logging.Filter):
    """Filter to add request context to log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        """Add request context to log record."""
        record.request_id = request_id_var.get()
        record.user_id = user_id_var.get()
        return True


def setup_logger(
    name: str,
    level: str = "INFO",
    use_json: bool = True,
    use_powertools: bool = True
) -> logging.Logger:
    """
    Setup structured logger with appropriate configuration.

    Args:
        name: Logger name
        level: Log level
        use_json: Whether to use JSON formatting
        use_powertools: Whether to use AWS Lambda Powertools logger

    Returns:
        Configured logger instance
    """
    if use_powertools:
        # Use Lambda Powertools logger for AWS Lambda
        logger = PowertoolsLogger(
            service=name,
            level=level,
            correlation_id_path=correlation_paths.API_GATEWAY_REST,
            use_datetime_directive=True,
            json_serializer=json.dumps,
            json_deserializer=json.loads,
            json_default=str,
            datefmt='%Y-%m-%d %H:%M:%S',
        )
        return logger

    # Setup standard Python logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)

    if use_json:
        handler.setFormatter(StructuredFormatter())
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)

    # Add request context filter
    handler.addFilter(RequestContextFilter())

    logger.addHandler(handler)
    logger.propagate = False

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get logger instance for the given name.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    from ..config import get_settings

    settings = get_settings()

    return setup_logger(
        name=name,
        level=settings.logging.level,
        use_json=settings.logging.json_logs,
        use_powertools=True  # Always use powertools in Lambda
    )


def set_request_context(request_id: Optional[str] = None, user_id: Optional[str] = None) -> None:
    """
    Set request context for logging.

    Args:
        request_id: Request ID for correlation
        user_id: User ID for tracking
    """
    if request_id:
        request_id_var.set(request_id)
    else:
        # Generate request ID if not provided
        request_id_var.set(str(uuid.uuid4()))

    if user_id:
        user_id_var.set(user_id)


def clear_request_context() -> None:
    """Clear request context."""
    request_id_var.set(None)
    user_id_var.set(None)


def get_request_id() -> Optional[str]:
    """Get current request ID."""
    return request_id_var.get()


def get_user_id() -> Optional[str]:
    """Get current user ID."""
    return user_id_var.get()


def log_function_call(logger: Optional[logging.Logger] = None):
    """
    Decorator to log function calls with parameters and results.

    Args:
        logger: Logger instance (uses function name if not provided)
    """
    def decorator(func):
        nonlocal logger
        if logger is None:
            logger = get_logger(func.__module__)

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            func_name = func.__name__

            # Log function entry
            logger.info(
                f"Entering function {func_name}",
                extra={
                    "function": func_name,
                    "args_count": len(args),
                    "kwargs_keys": list(kwargs.keys()),
                    "event_type": "function_entry"
                }
            )

            try:
                result = await func(*args, **kwargs)

                # Log successful completion
                logger.info(
                    f"Function {func_name} completed successfully",
                    extra={
                        "function": func_name,
                        "event_type": "function_success"
                    }
                )

                return result

            except Exception as e:
                # Log error
                logger.error(
                    f"Function {func_name} failed with error: {str(e)}",
                    extra={
                        "function": func_name,
                        "error": str(e),
                        "error_type": type(e).__name__,
                        "event_type": "function_error"
                    },
                    exc_info=True
                )
                raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            func_name = func.__name__

            # Log function entry
            logger.info(
                f"Entering function {func_name}",
                extra={
                    "function": func_name,
                    "args_count": len(args),
                    "kwargs_keys": list(kwargs.keys()),
                    "event_type": "function_entry"
                }
            )

            try:
                result = func(*args, **kwargs)

                # Log successful completion
                logger.info(
                    f"Function {func_name} completed successfully",
                    extra={
                        "function": func_name,
                        "event_type": "function_success"
                    }
                )

                return result

            except Exception as e:
                # Log error
                logger.error(
                    f"Function {func_name} failed with error: {str(e)}",
                    extra={
                        "function": func_name,
                        "error": str(e),
                        "error_type": type(e).__name__,
                        "event_type": "function_error"
                    },
                    exc_info=True
                )
                raise

        # Return appropriate wrapper based on function type
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def log_performance(logger: Optional[logging.Logger] = None, threshold_ms: int = 1000):
    """
    Decorator to log function performance metrics.

    Args:
        logger: Logger instance
        threshold_ms: Threshold in milliseconds to log slow operations
    """
    def decorator(func):
        nonlocal logger
        if logger is None:
            logger = get_logger(func.__module__)

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            import time
            start_time = time.time()
            func_name = func.__name__

            try:
                result = await func(*args, **kwargs)
                execution_time = (time.time() - start_time) * 1000

                log_level = logging.WARNING if execution_time > threshold_ms else logging.INFO
                logger.log(
                    log_level,
                    f"Function {func_name} executed in {execution_time:.2f}ms",
                    extra={
                        "function": func_name,
                        "execution_time_ms": execution_time,
                        "slow_operation": execution_time > threshold_ms,
                        "event_type": "performance_metric"
                    }
                )

                return result

            except Exception as e:
                execution_time = (time.time() - start_time) * 1000
                logger.error(
                    f"Function {func_name} failed after {execution_time:.2f}ms",
                    extra={
                        "function": func_name,
                        "execution_time_ms": execution_time,
                        "error": str(e),
                        "event_type": "performance_error"
                    }
                )
                raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            import time
            start_time = time.time()
            func_name = func.__name__

            try:
                result = func(*args, **kwargs)
                execution_time = (time.time() - start_time) * 1000

                log_level = logging.WARNING if execution_time > threshold_ms else logging.INFO
                logger.log(
                    log_level,
                    f"Function {func_name} executed in {execution_time:.2f}ms",
                    extra={
                        "function": func_name,
                        "execution_time_ms": execution_time,
                        "slow_operation": execution_time > threshold_ms,
                        "event_type": "performance_metric"
                    }
                )

                return result

            except Exception as e:
                execution_time = (time.time() - start_time) * 1000
                logger.error(
                    f"Function {func_name} failed after {execution_time:.2f}ms",
                    extra={
                        "function": func_name,
                        "execution_time_ms": execution_time,
                        "error": str(e),
                        "event_type": "performance_error"
                    }
                )
                raise

        # Return appropriate wrapper based on function type
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator