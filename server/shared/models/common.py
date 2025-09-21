"""
Common fields and types for SQLModel models.

Provides reusable field definitions and type annotations that can be
used across different models to ensure consistency.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/20
"""

from sqlmodel import Field
from pydantic import EmailStr, HttpUrl
from typing import Optional, List, Annotated
from datetime import datetime, date


# Common Field Types
IDField = Annotated[Optional[int], Field(default=None, primary_key=True)]
NameField = Annotated[str, Field(max_length=255, description="Name")]
TitleField = Annotated[str, Field(max_length=255, description="Title")]
ShortTextField = Annotated[str, Field(max_length=500, description="Short text")]
LongTextField = Annotated[str, Field(description="Long text content")]
SlugField = Annotated[str, Field(max_length=255, regex=r'^[a-z0-9-]+$', description="URL slug")]

# Contact Fields
EmailField = Annotated[EmailStr, Field(description="Email address")]
PhoneField = Annotated[Optional[str], Field(None, max_length=20, description="Phone number")]
WebsiteField = Annotated[Optional[HttpUrl], Field(None, description="Website URL")]
LinkedInField = Annotated[Optional[HttpUrl], Field(None, description="LinkedIn profile")]
GitHubField = Annotated[Optional[HttpUrl], Field(None, description="GitHub profile")]

# Location Fields
CityField = Annotated[Optional[str], Field(None, max_length=100, description="City")]
StateField = Annotated[Optional[str], Field(None, max_length=100, description="State/Province")]
CountryField = Annotated[Optional[str], Field(None, max_length=100, description="Country")]
PostalCodeField = Annotated[Optional[str], Field(None, max_length=20, description="Postal code")]

# Date Fields
DateField = Annotated[date, Field(description="Date")]
OptionalDateField = Annotated[Optional[date], Field(None, description="Optional date")]
TimestampField = Annotated[datetime, Field(description="Timestamp")]
OptionalTimestampField = Annotated[Optional[datetime], Field(None, description="Optional timestamp")]

# Status Fields
IsActiveField = Annotated[bool, Field(default=True, description="Active status")]
IsFeaturedField = Annotated[bool, Field(default=False, description="Featured status")]
IsPublishedField = Annotated[bool, Field(default=False, description="Published status")]
IsCurrentField = Annotated[bool, Field(default=False, description="Current status")]

# Numeric Fields
OrderIndexField = Annotated[int, Field(default=0, description="Order index")]
PriorityField = Annotated[int, Field(default=1, ge=1, le=5, description="Priority (1-5)")]
LevelField = Annotated[int, Field(ge=1, le=5, description="Level (1-5)")]
YearsExperienceField = Annotated[Optional[float], Field(None, ge=0, description="Years of experience")]
ViewCountField = Annotated[int, Field(default=0, ge=0, description="View count")]

# Technology and Skills Fields
TechnologyNameField = Annotated[str, Field(max_length=100, description="Technology name")]
CategoryField = Annotated[str, Field(max_length=100, description="Category")]
SubcategoryField = Annotated[Optional[str], Field(None, max_length=100, description="Subcategory")]
TagsField = Annotated[Optional[str], Field(None, description="Comma-separated tags")]

# Media Fields
ImageUrlField = Annotated[Optional[HttpUrl], Field(None, description="Image URL")]
IconUrlField = Annotated[Optional[HttpUrl], Field(None, description="Icon URL")]
AltTextField = Annotated[Optional[str], Field(None, max_length=255, description="Alt text")]

# Project Fields
ProjectStatusField = Annotated[str, Field(
    default="completed",
    max_length=50,
    description="Project status"
)]
DemoUrlField = Annotated[Optional[HttpUrl], Field(None, description="Demo URL")]
RepositoryUrlField = Annotated[Optional[HttpUrl], Field(None, description="Repository URL")]

# Company Fields
CompanyField = Annotated[str, Field(max_length=255, description="Company name")]
PositionField = Annotated[str, Field(max_length=255, description="Position/Role")]
LocationField = Annotated[Optional[str], Field(None, max_length=255, description="Location")]
CompanyUrlField = Annotated[Optional[HttpUrl], Field(None, description="Company website")]
LogoUrlField = Annotated[Optional[HttpUrl], Field(None, description="Company logo URL")]

# Metadata Fields
MetadataField = Annotated[Optional[str], Field(None, description="JSON metadata")]
NotesField = Annotated[Optional[str], Field(None, description="Additional notes")]
VersionField = Annotated[int, Field(default=1, description="Version number")]

# Array Fields (for PostgreSQL)
StringArrayField = Annotated[Optional[List[str]], Field(None, description="Array of strings")]
IntArrayField = Annotated[Optional[List[int]], Field(None, description="Array of integers")]

# Common Field Constraints
class FieldConstraints:
    """Common field validation constraints."""

    # Text lengths
    SHORT_TEXT_MAX = 255
    MEDIUM_TEXT_MAX = 500
    LONG_TEXT_MAX = 2000
    DESCRIPTION_MAX = 1000

    # Names and identifiers
    NAME_MAX = 100
    TITLE_MAX = 255
    SLUG_MAX = 255
    CATEGORY_MAX = 100
    TAG_MAX = 50

    # Contact info
    PHONE_MAX = 20
    EMAIL_MAX = 255

    # Location
    CITY_MAX = 100
    STATE_MAX = 100
    COUNTRY_MAX = 100
    POSTAL_CODE_MAX = 20

    # Numeric ranges
    PRIORITY_MIN = 1
    PRIORITY_MAX = 5
    LEVEL_MIN = 1
    LEVEL_MAX = 5
    EXPERIENCE_MIN = 0
    EXPERIENCE_MAX = 50

    # Pagination
    LIMIT_MIN = 1
    LIMIT_MAX = 100
    LIMIT_DEFAULT = 10


# Common Validators
def validate_non_empty_string(value: str) -> str:
    """Validate that string is not empty after stripping."""
    if not value.strip():
        raise ValueError("Field cannot be empty")
    return value.strip()


def validate_positive_number(value: float) -> float:
    """Validate that number is positive."""
    if value < 0:
        raise ValueError("Value must be positive")
    return value


def validate_url_list(urls: List[str]) -> List[str]:
    """Validate list of URLs."""
    if not urls:
        return []

    # Remove duplicates while preserving order
    seen = set()
    unique_urls = []
    for url in urls:
        if url not in seen:
            unique_urls.append(url)
            seen.add(url)

    return unique_urls


def validate_tag_list(tags: List[str]) -> List[str]:
    """Validate and clean list of tags."""
    if not tags:
        return []

    # Clean and normalize tags
    cleaned_tags = []
    seen = set()

    for tag in tags:
        clean_tag = tag.strip().lower()
        if clean_tag and clean_tag not in seen:
            cleaned_tags.append(clean_tag)
            seen.add(clean_tag)

    return cleaned_tags


# Common Choices
class StatusChoices:
    """Common status choices."""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    ACTIVE = "active"
    INACTIVE = "inactive"


class PriorityChoices:
    """Priority level choices."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4
    CRITICAL = 5


class ProjectStatusChoices:
    """Project status choices."""
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"


class SkillCategoryChoices:
    """Skill category choices."""
    PROGRAMMING = "programming"
    FRAMEWORK = "framework"
    DATABASE = "database"
    CLOUD = "cloud"
    DEVOPS = "devops"
    FRONTEND = "frontend"
    SERVER = "server"
    MOBILE = "mobile"
    DESIGN = "design"
    SOFT_SKILLS = "soft_skills"


class ExperienceTypeChoices:
    """Experience type choices."""
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    FREELANCE = "freelance"
    INTERNSHIP = "internship"
    VOLUNTEER = "volunteer"