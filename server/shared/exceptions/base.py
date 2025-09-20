"""
Base exception classes for the portfolio system.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/20
"""

from typing import Optional, Dict, Any


class PortfolioBaseException(Exception):
    """Base exception for all portfolio-related errors."""

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary."""
        return {
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details,
            "type": self.__class__.__name__
        }


class ValidationError(PortfolioBaseException):
    """Raised when data validation fails."""
    pass


class NotFoundError(PortfolioBaseException):
    """Raised when a resource is not found."""
    pass


class DuplicateError(PortfolioBaseException):
    """Raised when trying to create a duplicate resource."""
    pass


class PermissionError(PortfolioBaseException):
    """Raised when user lacks permission for an operation."""
    pass


class ConfigurationError(PortfolioBaseException):
    """Raised when there's a configuration issue."""
    pass


class ExternalServiceError(PortfolioBaseException):
    """Raised when an external service fails."""
    pass