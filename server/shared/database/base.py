"""
Base SQLModel classes and configurations.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/20
"""

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
from pydantic import field_validator


class BaseTable(SQLModel):
    """
    Base class for all database tables.
    Provides common fields and functionality for all models.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Record creation timestamp"
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description="Record last update timestamp"
    )

    @field_validator('created_at', 'updated_at', mode='before')
    @classmethod
    def validate_datetime(cls, v):
        """Ensure datetime objects are timezone-aware."""
        if v is not None and v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v

    def update_timestamp(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now(timezone.utc)

    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda dt: dt.isoformat() if dt else None
        }


class BaseSchema(SQLModel):
    """
    Base class for API schemas (request/response models).
    Used for models that don't map to database tables.
    """

    class Config:
        """Pydantic configuration for schemas."""
        json_encoders = {
            datetime: lambda dt: dt.isoformat() if dt else None
        }
        extra = "forbid"  # Forbid extra fields in API requests


class TimestampMixin(SQLModel):
    """
    Mixin for adding timestamp fields to models.
    Use when you need timestamps but don't want to inherit from BaseTable.
    """

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Record creation timestamp"
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description="Record last update timestamp"
    )

    @field_validator('created_at', 'updated_at', mode='before')
    @classmethod
    def validate_datetime(cls, v):
        """Ensure datetime objects are timezone-aware."""
        if v is not None and v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v

    def update_timestamp(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now(timezone.utc)


class ActiveRecordMixin(SQLModel):
    """
    Mixin for soft delete functionality.
    Adds is_active field for logical deletion.
    """

    is_active: bool = Field(default=True, description="Record active status")

    def soft_delete(self) -> None:
        """Mark record as inactive (soft delete)."""
        self.is_active = False
        if hasattr(self, 'update_timestamp'):
            self.update_timestamp()

    def activate(self) -> None:
        """Mark record as active."""
        self.is_active = True
        if hasattr(self, 'update_timestamp'):
            self.update_timestamp()


class AuditMixin(SQLModel):
    """
    Mixin for audit fields.
    Tracks who created and modified records.
    """

    created_by: Optional[str] = Field(
        default=None,
        description="User who created the record"
    )
    updated_by: Optional[str] = Field(
        default=None,
        description="User who last updated the record"
    )