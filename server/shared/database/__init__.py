"""
Database module for shared Lambda functionality.

This module provides:
- Database connection management optimized for AWS Lambda
- Base SQLModel classes and mixins
- Session management and lifecycle handling
- Centralized SQLAlchemy imports (Lambda functions should NEVER import sqlalchemy directly)

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/20
"""

# Re-export SQLAlchemy types for Lambda functions
# Lambda functions should ALWAYS import these from shared.database, NOT from sqlalchemy directly
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload, contains_eager, lazyload
from sqlalchemy import select, delete, update, text, and_, or_, not_

# Re-export connection utilities
from .connection import get_db_session, DatabaseManager

__all__ = [
    # Session types
    "AsyncSession",

    # Query utilities
    "select",
    "delete",
    "update",
    "text",

    # Logical operators
    "and_",
    "or_",
    "not_",

    # Relationship loading strategies
    "selectinload",
    "joinedload",
    "contains_eager",
    "lazyload",

    # Connection management
    "get_db_session",
    "DatabaseManager",
]