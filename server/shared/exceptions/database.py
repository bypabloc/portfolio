"""
Database-related exceptions.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/20
"""

from .base import PortfolioBaseException


class DatabaseError(PortfolioBaseException):
    """Base database error."""
    pass


class ConnectionError(DatabaseError):
    """Database connection error."""
    pass


class RepositoryError(DatabaseError):
    """Repository operation error."""
    pass


class RecordNotFoundError(DatabaseError):
    """Database record not found."""
    pass


class DuplicateRecordError(DatabaseError):
    """Duplicate database record."""
    pass


class IntegrityError(DatabaseError):
    """Database integrity constraint violation."""
    pass


class TransactionError(DatabaseError):
    """Database transaction error."""
    pass