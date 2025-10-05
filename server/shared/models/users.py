"""
User models aligned with Atlas HCL schema.

Implements EAV (Entity-Attribute-Value) pattern for flexible user attributes.

Schema alignment:
- users.hcl -> User model
- users_attributes.hcl -> UserAttribute model (EAV pattern)
- attributes_types.hcl -> Referenced for attribute validation

:Authors:
    - Pablo Contreras

:Created:
    - 2025-01-19
"""

from sqlmodel import SQLModel, Field, Relationship, Column, text
from sqlalchemy import String
from typing import Optional, List, Any, Dict
from datetime import datetime
import json


# ============================================================================
# TABLE: users
# Schema: portfolio.users
# ============================================================================

class UserBase(SQLModel):
    """Base model for User - shared fields for create/update."""
    username: str = Field(
        sa_column=Column(String, unique=True, index=True, nullable=False),
        description="Unique username identifier"
    )
    status: str = Field(
        default="active",
        index=True,
        description="User status (active, inactive, etc.)"
    )


class User(UserBase, table=True):
    """
    User table - alineado con schema Atlas users.hcl.

    Implements core user entity with EAV pattern for flexible attributes
    via users_attributes table.

    Fields:
        id: UUID primary key (auto-generated)
        username: Unique username (required)
        status: User status (default 'active')
        created_at: Timestamp of creation
        updated_at: Timestamp of last update

    Relationships:
        attributes: List[UserAttribute] - User attributes via EAV pattern
        works: List[Work] - Professional experience
        projects: List[Project] - Portfolio projects

    Atlas HCL Reference: db/atlas/schema/users.hcl
    """
    __tablename__ = "users"
    __table_args__ = {"schema": "portfolio"}

    # Primary Key
    id: Optional[str] = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={
            "server_default": text("gen_random_uuid()::text")
        },
        description="UUID primary key"
    )

    # Timestamps
    created_at: datetime = Field(
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
            "nullable": False
        },
        description="Creation timestamp"
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description="Last update timestamp"
    )

    # Relationships (forward references as strings)
    # Using lazy="selectin" for async compatibility
    attributes: List["UserAttribute"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "lazy": "selectin"  # Async-compatible lazy loading
        }
    )
    works: List["Work"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "lazy": "selectin"  # Async-compatible lazy loading
        }
    )
    projects: List["Project"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "lazy": "selectin"  # Async-compatible lazy loading
        }
    )

    # =========================================================================
    # CLASS METHODS - Query Encapsulation (Lambda functions use ONLY these)
    # Lambda functions should NEVER import from shared.database directly
    # =========================================================================

    @classmethod
    async def get_all(cls, session, skip: int = 0, limit: int = 100):
        """
        Get all users with attributes (eager loaded).

        Args:
            session: AsyncSession from dependency injection
            skip: Offset for pagination
            limit: Limit for pagination

        Returns:
            List[User]: Users with attributes loaded
        """
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload

        statement = (
            select(cls)
            .options(selectinload(cls.attributes))
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(statement)
        return result.scalars().all()

    @classmethod
    async def get_by_id(cls, session, user_id: str):
        """
        Get user by ID with attributes (eager loaded).

        Args:
            session: AsyncSession from dependency injection
            user_id: User UUID

        Returns:
            User | None: User with attributes or None
        """
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload

        statement = (
            select(cls)
            .options(selectinload(cls.attributes))
            .where(cls.id == user_id)
        )
        result = await session.execute(statement)
        return result.scalars().first()

    @classmethod
    async def get_by_username(cls, session, username: str):
        """
        Get user by username with attributes (eager loaded).

        Args:
            session: AsyncSession from dependency injection
            username: Username

        Returns:
            User | None: User with attributes or None
        """
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload

        statement = (
            select(cls)
            .options(selectinload(cls.attributes))
            .where(cls.username == username)
        )
        result = await session.execute(statement)
        return result.scalars().first()


# ============================================================================
# TABLE: users_attributes (EAV Pattern)
# Schema: portfolio.users_attributes
# ============================================================================

class UserAttributeBase(SQLModel):
    """Base model for UserAttribute - EAV pattern."""
    code_name: str = Field(
        description="Unique identifier for this attribute (e.g., 'name', 'email', 'title')"
    )
    attribute_value: str = Field(
        description="Value of the attribute (JSON for complex objects)"
    )


class UserAttribute(UserAttributeBase, table=True):
    """
    UserAttribute table - EAV pattern for flexible user data.

    Allows storing dynamic attributes like:
    - name, title, email, phone, location
    - linkedin, github, website URLs
    - bio, summary, description

    The attribute_value is stored as JSON string for complex values.

    Fields:
        id: UUID primary key
        code_name: Attribute identifier (e.g., 'email', 'linkedin')
        attribute_value: JSON string value
        user_id: Foreign key to users
        attribute_type_id: Foreign key to attributes_types
        status: Attribute status
        created_at/updated_at: Timestamps

    Atlas HCL Reference: db/atlas/schema/users_attributes.hcl
    """
    __tablename__ = "users_attributes"
    __table_args__ = {"schema": "portfolio"}

    # Primary Key
    id: Optional[str] = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={
            "server_default": text("gen_random_uuid()::text")
        }
    )

    # Status and Timestamps
    status: str = Field(default="active")
    created_at: datetime = Field(
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")}
    )
    updated_at: Optional[datetime] = None

    # Foreign Keys
    user_id: str = Field(
        foreign_key="portfolio.users.id",
        index=True,
        description="Reference to user"
    )
    # Note: attribute_type_id FK is enforced at DB level only (no SQLModel FK)
    # This avoids metadata issues when AttributeType model doesn't exist
    attribute_type_id: str = Field(
        index=True,
        description="Reference to attribute type (FK at DB level)"
    )

    # Relationships
    user: User = Relationship(back_populates="attributes")

    @property
    def value_parsed(self) -> Any:
        """
        Parse JSON attribute_value to Python object.

        Returns:
            Any: Parsed value (str, dict, list, etc.)

        Example:
            attribute.attribute_value = '{"first": "Pablo", "last": "Contreras"}'
            attribute.value_parsed  # {'first': 'Pablo', 'last': 'Contreras'}
        """
        try:
            return json.loads(self.attribute_value)
        except (json.JSONDecodeError, TypeError):
            return self.attribute_value

    @classmethod
    def create_from_dict(cls, user_id: str, code_name: str, value: Any, attribute_type_id: str) -> "UserAttribute":
        """
        Helper to create UserAttribute from Python value.

        Args:
            user_id: User ID
            code_name: Attribute name
            value: Python value (will be JSON-serialized if needed)
            attribute_type_id: Attribute type ID

        Returns:
            UserAttribute: New instance

        Example:
            attr = UserAttribute.create_from_dict(
                user_id="123",
                code_name="name",
                value={"first": "Pablo", "last": "Contreras"},
                attribute_type_id="name_type_id"
            )
        """
        if isinstance(value, (dict, list)):
            attribute_value = json.dumps(value)
        else:
            attribute_value = str(value)

        return cls(
            user_id=user_id,
            code_name=code_name,
            attribute_value=attribute_value,
            attribute_type_id=attribute_type_id
        )


# ============================================================================
# Helper Functions for EAV Pattern
# ============================================================================

def attributes_to_dict(attributes: List[UserAttribute]) -> Dict[str, Any]:
    """
    Convert list of UserAttribute to flat dictionary.

    Args:
        attributes: List of user attributes

    Returns:
        Dict with code_name as keys and parsed values

    Example:
        attributes = [
            UserAttribute(code_name="name", attribute_value="Pablo"),
            UserAttribute(code_name="email", attribute_value="pablo@example.com"),
        ]
        result = attributes_to_dict(attributes)
        # {'name': 'Pablo', 'email': 'pablo@example.com'}
    """
    return {
        attr.code_name: attr.value_parsed
        for attr in attributes
        if attr.status == "active"
    }


def dict_to_attributes(
    user_id: str,
    data: Dict[str, Any],
    attribute_type_mapping: Dict[str, str]
) -> List[UserAttribute]:
    """
    Convert dictionary to list of UserAttribute instances.

    Args:
        user_id: User ID
        data: Dictionary with attribute values
        attribute_type_mapping: Map of code_name -> attribute_type_id

    Returns:
        List of UserAttribute instances

    Example:
        data = {"name": "Pablo", "email": "pablo@example.com"}
        mapping = {"name": "name_type_id", "email": "email_type_id"}
        attributes = dict_to_attributes("user_123", data, mapping)
    """
    attributes = []
    for code_name, value in data.items():
        if code_name in attribute_type_mapping:
            attr = UserAttribute.create_from_dict(
                user_id=user_id,
                code_name=code_name,
                value=value,
                attribute_type_id=attribute_type_mapping[code_name]
            )
            attributes.append(attr)
    return attributes
