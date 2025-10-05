"""
Base models and schemas for the portfolio system.

These models serve as base classes for all Lambda functions and provide
common field types and validation patterns.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/20
"""

from sqlmodel import SQLModel, Field
from pydantic import BaseModel, EmailStr, HttpUrl, field_validator, ConfigDict
from typing import Optional, List, Union, Any
from datetime import datetime, date
from enum import Enum


# Common Enums
class StatusEnum(str, Enum):
    """Common status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class PriorityEnum(str, Enum):
    """Priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class VisibilityEnum(str, Enum):
    """Visibility levels."""
    PUBLIC = "public"
    PRIVATE = "private"
    UNLISTED = "unlisted"


# Base Response Models
class HealthResponse(BaseModel):
    """Standard health check response."""
    model_config = ConfigDict(extra='forbid')

    status: str = Field(description="Service health status")
    service: str = Field(description="Service name")
    timestamp: datetime = Field(description="Response timestamp")
    version: str = Field(description="Service version")
    database: Optional[str] = Field(None, description="Database status")


class APIResponse(BaseModel):
    """Standard API response wrapper."""
    model_config = ConfigDict(extra='forbid')

    success: bool = Field(description="Request success status")
    data: Optional[Any] = Field(None, description="Response data")
    message: Optional[str] = Field(None, description="Response message")
    error: Optional[str] = Field(None, description="Error message if any")
    timestamp: datetime = Field(description="Response timestamp")
    request_id: Optional[str] = Field(None, description="Request correlation ID")


class PaginationParams(BaseModel):
    """Standard pagination parameters."""
    model_config = ConfigDict(extra='forbid')

    limit: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Number of items per page"
    )
    offset: int = Field(
        default=0,
        ge=0,
        description="Number of items to skip"
    )
    order_by: Optional[str] = Field(
        None,
        description="Field to order by"
    )
    order_direction: str = Field(
        default="asc",
        description="Order direction (asc or desc)"
    )


class PaginatedResponse(BaseModel):
    """Standard paginated response."""
    model_config = ConfigDict(extra='forbid')

    items: List[Any] = Field(description="List of items")
    total: int = Field(description="Total number of items")
    limit: int = Field(description="Items per page limit")
    offset: int = Field(description="Items offset")
    has_next: bool = Field(description="Whether there are more items")
    has_previous: bool = Field(description="Whether there are previous items")


# Contact Information Models
class ContactInfo(BaseModel):
    """Base contact information model."""
    model_config = ConfigDict(extra='forbid')

    email: Optional[EmailStr] = Field(None, description="Email address")
    phone: Optional[str] = Field(
        None,
        max_length=20,
        description="Phone number"
    )
    website: Optional[HttpUrl] = Field(None, description="Website URL")
    linkedin: Optional[HttpUrl] = Field(None, description="LinkedIn profile")
    github: Optional[HttpUrl] = Field(None, description="GitHub profile")
    twitter: Optional[HttpUrl] = Field(None, description="Twitter profile")


class Address(BaseModel):
    """Address information model."""
    model_config = ConfigDict(extra='forbid')

    street: Optional[str] = Field(None, max_length=255, description="Street address")
    city: Optional[str] = Field(None, max_length=100, description="City")
    state: Optional[str] = Field(None, max_length=100, description="State/Province")
    country: Optional[str] = Field(None, max_length=100, description="Country")
    postal_code: Optional[str] = Field(None, max_length=20, description="Postal code")

    def __str__(self) -> str:
        """String representation of address."""
        parts = [self.city, self.state, self.country]
        return ", ".join(filter(None, parts))


# Technology and Skills Models
class Technology(BaseModel):
    """Technology/tool representation."""
    model_config = ConfigDict(extra='forbid')

    name: str = Field(max_length=100, description="Technology name")
    category: Optional[str] = Field(None, max_length=50, description="Technology category")
    proficiency: Optional[int] = Field(
        None,
        ge=1,
        le=5,
        description="Proficiency level (1-5)"
    )
    years_experience: Optional[float] = Field(
        None,
        ge=0,
        description="Years of experience"
    )
    icon_url: Optional[HttpUrl] = Field(None, description="Technology icon URL")
    official_url: Optional[HttpUrl] = Field(None, description="Official website")


class SkillLevel(BaseModel):
    """Skill level representation."""
    model_config = ConfigDict(extra='forbid')

    level: int = Field(ge=1, le=5, description="Skill level (1-5)")
    description: str = Field(description="Level description")

    @field_validator('level')
    @classmethod
    def validate_level(cls, v):
        """Validate skill level is within range."""
        if not 1 <= v <= 5:
            raise ValueError('Skill level must be between 1 and 5')
        return v


# Date Range Models
class DateRange(BaseModel):
    """Date range representation."""
    model_config = ConfigDict(extra='forbid')

    start_date: date = Field(description="Start date")
    end_date: Optional[date] = Field(None, description="End date (null if current)")
    is_current: bool = Field(default=False, description="Whether this is current")

    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v, info):
        """Validate end date is after start date."""
        if v and 'start_date' in info.data and v < info.data['start_date']:
            raise ValueError('End date must be after start date')
        return v

    def duration_in_months(self) -> Optional[int]:
        """Calculate duration in months."""
        if not self.start_date:
            return None

        end = self.end_date or date.today()
        years = end.year - self.start_date.year
        months = end.month - self.start_date.month
        return years * 12 + months

    def __str__(self) -> str:
        """String representation of date range."""
        start = self.start_date.strftime("%b %Y")
        if self.is_current:
            return f"{start} - Present"
        elif self.end_date:
            end = self.end_date.strftime("%b %Y")
            return f"{start} - {end}"
        return start


# File and Media Models
class FileInfo(BaseModel):
    """File information model."""
    model_config = ConfigDict(extra='forbid')

    filename: str = Field(description="Original filename")
    url: HttpUrl = Field(description="File URL")
    mime_type: Optional[str] = Field(None, description="MIME type")
    size_bytes: Optional[int] = Field(None, ge=0, description="File size in bytes")
    alt_text: Optional[str] = Field(None, description="Alternative text for accessibility")


class ImageInfo(FileInfo):
    """Image-specific information."""
    width: Optional[int] = Field(None, ge=1, description="Image width in pixels")
    height: Optional[int] = Field(None, ge=1, description="Image height in pixels")
    aspect_ratio: Optional[str] = Field(None, description="Aspect ratio (e.g., '16:9')")


# Validation Helpers
class URLList(BaseModel):
    """List of URLs with validation."""
    model_config = ConfigDict(extra='forbid')

    urls: List[HttpUrl] = Field(description="List of URLs")

    @field_validator('urls')
    @classmethod
    def validate_unique_urls(cls, v):
        """Ensure URLs are unique."""
        url_strings = [str(url) for url in v]
        if len(url_strings) != len(set(url_strings)):
            raise ValueError('URLs must be unique')
        return v


class TagList(BaseModel):
    """List of tags with validation."""
    model_config = ConfigDict(extra='forbid')

    tags: List[str] = Field(description="List of tags")

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v):
        """Clean and validate tags."""
        # Clean whitespace and convert to lowercase
        cleaned_tags = [tag.strip().lower() for tag in v if tag.strip()]
        # Remove duplicates while preserving order
        unique_tags = []
        seen = set()
        for tag in cleaned_tags:
            if tag not in seen:
                unique_tags.append(tag)
                seen.add(tag)
        return unique_tags


# Search and Filter Models
class SearchParams(BaseModel):
    """Search parameters."""
    model_config = ConfigDict(extra='forbid')

    query: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="Search query"
    )
    tags: Optional[List[str]] = Field(
        None,
        description="Filter by tags"
    )
    category: Optional[str] = Field(
        None,
        max_length=100,
        description="Filter by category"
    )
    status: Optional[StatusEnum] = Field(
        None,
        description="Filter by status"
    )
    date_from: Optional[date] = Field(
        None,
        description="Filter from date"
    )
    date_to: Optional[date] = Field(
        None,
        description="Filter to date"
    )