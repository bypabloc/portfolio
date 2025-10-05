"""
Custom Logger for Portfolio Serverless System.

Provides structured logging with colorized output for local development
and JSON formatting for production environments.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/01/19

:Updated:
    - 2025/01/19 - Initial implementation adapted from Django logger
"""

import sys
import os
import traceback
from datetime import datetime
from typing import Any, Dict, Optional
import json
from pathlib import Path


# ANSI color codes for terminal output
class Colors:
    """ANSI color codes for colorized terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright foreground colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"


class Logger:
    """
    Custom logger with colorized output and structured logging.

    Features:
    - Colorized console output for local development
    - Structured logging with timestamps and file/line information
    - Support for extra fields for additional context
    - Methods: info, warning, error, critical, debug
    - Automatic environment detection (local vs production)

    Usage:
        from shared.logger import logger

        logger.info("User created", extra={"user_id": "123"})
        logger.error("Database connection failed", extra={"error": str(e)})
    """

    def __init__(self, name: str = "portfolio"):
        """
        Initialize logger.

        Args:
            name: Logger name for identification
        """
        self.name = name
        self.environment = os.getenv("ENVIRONMENT", "local")
        self.is_local = self.environment in ("local", "development", "dev")

        # Get project root for relative path calculation
        # Assuming server/shared/logger.py -> go up 2 levels to get server/
        self.project_root = Path(__file__).parent.parent

    def _get_caller_info(self) -> Dict[str, str]:
        """
        Get information about the caller (file, line, function).

        Returns:
            Dictionary with file, line, and function information
        """
        try:
            # Walk up the stack to find the actual caller (skip logger methods)
            # Stack: caller -> info/error/etc -> _log -> _get_caller_info
            frame = sys._getframe(3)  # Skip 3 levels to get to actual caller

            filename = frame.f_code.co_filename
            lineno = frame.f_lineno
            funcname = frame.f_code.co_name

            # Get relative path from project root
            try:
                file_path = Path(filename)
                relative_path = file_path.relative_to(self.project_root)
                file_location = str(relative_path)
            except (ValueError, AttributeError):
                # If not relative to project root, use basename
                file_location = os.path.basename(filename)

            return {
                "file": file_location,
                "line": str(lineno),
                "function": funcname
            }
        except Exception:
            return {
                "file": "unknown",
                "line": "0",
                "function": "unknown"
            }

    def _log(
        self,
        level: str,
        message: str,
        extra: Optional[Dict[str, Any]] = None,
        exc_info: bool = False
    ):
        """
        Internal logging method.

        Args:
            level: Log level (INFO, WARNING, ERROR, etc.)
            message: Log message
            extra: Additional context fields
            exc_info: Include exception traceback
        """
        caller = self._get_caller_info()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Color mapping for log levels
        level_colors = {
            "DEBUG": Colors.CYAN,
            "INFO": Colors.GREEN,
            "WARNING": Colors.YELLOW,
            "ERROR": Colors.RED,
            "CRITICAL": Colors.BRIGHT_RED + Colors.BOLD,
        }

        if self.is_local:
            # Local development - colorized output
            level_color = level_colors.get(level, Colors.WHITE)

            file_info = f"{caller['file']}:{caller['line']}"
            formatted = f"{Colors.GREEN}[{timestamp}]{Colors.RESET} {Colors.BLUE}[{file_info}]{Colors.RESET} {level_color}[{level}] - {message} |{Colors.RESET} |"

            if extra:
                extra_json = json.dumps(extra, indent=2, default=str)
                print(formatted, extra_json, flush=True)
            else:
                print(formatted, "{}", flush=True)

            # Add exception traceback if requested
            if exc_info:
                tb = traceback.format_exc()
                print(f"{Colors.RED}{tb}{Colors.RESET}", flush=True)
        else:
            # Production - JSON output
            extra_json = json.dumps(extra or {}, default=str)
            file_info = f"{caller['file']}:{caller['line']}"
            formatted = f"|[{timestamp}] [{file_info}] [{level}] - {message} | {extra_json} |"
            print(formatted, flush=True)

            # Add exception traceback if requested
            if exc_info:
                tb = traceback.format_exc()
                print(f"| TRACEBACK: {tb} |", flush=True)

    def info(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """
        Log info message.

        Args:
            message: Log message
            extra: Additional context fields
        """
        self._log("INFO", message, extra=extra)

    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """
        Log warning message.

        Args:
            message: Log message
            extra: Additional context fields
        """
        self._log("WARNING", message, extra=extra)

    def error(
        self,
        message: str,
        extra: Optional[Dict[str, Any]] = None,
        exc_info: bool = False
    ):
        """
        Log error message.

        Args:
            message: Log message
            extra: Additional context fields
            exc_info: Include exception traceback
        """
        self._log("ERROR", message, extra=extra, exc_info=exc_info)

    def critical(
        self,
        message: str,
        extra: Optional[Dict[str, Any]] = None,
        exc_info: bool = False
    ):
        """
        Log critical message.

        Args:
            message: Log message
            extra: Additional context fields
            exc_info: Include exception traceback
        """
        self._log("CRITICAL", message, extra=extra, exc_info=exc_info)

    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """
        Log debug message.

        Args:
            message: Log message
            extra: Additional context fields
        """
        if self.is_local:
            self._log("DEBUG", message, extra=extra)


# Instancia global del logger para uso directo
logger = Logger()


# Función de compatibilidad para código existente
def get_logger(service_name: str = "lambda-function") -> Logger:
    """
    Get a logger instance (deprecated - use logger directly).

    Args:
        service_name: Name of the service/lambda function (ignored)

    Returns:
        Logger instance

    Example:
        from shared.logger import logger

        logger.info("Processing request")
    """
    return logger
