"""
Authentication and authorization exceptions.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/20
"""

from .base import PortfolioBaseException


class AuthenticationError(PortfolioBaseException):
    """Authentication failed."""
    pass


class AuthorizationError(PortfolioBaseException):
    """Authorization denied."""
    pass


class TokenError(PortfolioBaseException):
    """Token validation error."""
    pass


class SessionExpiredError(PortfolioBaseException):
    """Session has expired."""
    pass