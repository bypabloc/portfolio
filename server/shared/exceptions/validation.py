"""
Validation exceptions.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/20
"""

from .base import PortfolioBaseException


class ValidationError(PortfolioBaseException):
    """Data validation error."""
    pass


class SchemaValidationError(ValidationError):
    """Schema validation error."""
    pass


class FieldValidationError(ValidationError):
    """Field validation error."""
    pass


class FormatError(ValidationError):
    """Data format error."""
    pass


class RangeError(ValidationError):
    """Value out of range error."""
    pass