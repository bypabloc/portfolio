"""
Models module for shared Lambda functionality.

This module provides:
- SQLModel table models aligned with Atlas HCL schema
- Base models and schemas for API requests/responses
- Common field types and validators
- Model mixins for reusable functionality

Schema Alignment:
All models are aligned with db/atlas/schema/*.hcl definitions to ensure
consistency between database schema and application models.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/20

:Updated:
    - 2025/01/19 - Added complete Atlas-aligned models
"""

# ============================================================================
# Base Models and Common Schemas
# ============================================================================

from .base import (
    # Enums
    StatusEnum,
    PriorityEnum,
    VisibilityEnum,

    # Response Models
    HealthResponse,
    APIResponse,
    PaginationParams,
    PaginatedResponse,

    # Contact Models
    ContactInfo,
    Address,

    # Technology Models
    Technology,
    SkillLevel,

    # Date Models
    DateRange,

    # File Models
    FileInfo,
    ImageInfo,

    # Validation Helpers
    URLList,
    TagList,

    # Search Models
    SearchParams,
)


# ============================================================================
# Domain Models - Aligned with Atlas HCL Schema
# ============================================================================

# Users Domain (EAV Pattern)
from .users import (
    User,
    UserBase,
    UserAttribute,
    UserAttributeBase,
    attributes_to_dict,
    dict_to_attributes,
)

# Works Domain (Experience)
from .works import (
    Work,
    WorkBase,
    Employer,
    EmployerBase,
    JobType,
    JobTypeBase,
)

# Projects Domain
from .projects import (
    Project,
    ProjectBase,
)

# Skills Domain
from .skills import (
    Skill,
    SkillBase,
)

# ============================================================================
# Database Session Dependency (for FastAPI dependency injection)
# Lambda functions import ONLY from models, NOT from database
# ============================================================================

from ..database.connection import get_db_session


# ============================================================================
# Public API - All Exports
# ============================================================================

__all__ = [
    # Base Models
    "StatusEnum",
    "PriorityEnum",
    "VisibilityEnum",
    "HealthResponse",
    "APIResponse",
    "PaginationParams",
    "PaginatedResponse",
    "ContactInfo",
    "Address",
    "Technology",
    "SkillLevel",
    "DateRange",
    "FileInfo",
    "ImageInfo",
    "URLList",
    "TagList",
    "SearchParams",

    # Users Domain
    "User",
    "UserBase",
    "UserAttribute",
    "UserAttributeBase",
    "attributes_to_dict",
    "dict_to_attributes",

    # Works Domain
    "Work",
    "WorkBase",
    "Employer",
    "EmployerBase",
    "JobType",
    "JobTypeBase",

    # Projects Domain
    "Project",
    "ProjectBase",

    # Skills Domain
    "Skill",
    "SkillBase",

    # Database Session Dependency
    "get_db_session",
]