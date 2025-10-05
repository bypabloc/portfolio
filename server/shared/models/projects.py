"""
Project models aligned with Atlas HCL schema.

Portfolio projects with URLs and service status tracking.

Schema alignment:
- projects.hcl -> Project model
- project_urls.hcl -> ProjectUrl model (if needed for M2M)
- project_url_types.hcl -> URL type catalog

:Authors:
    - Pablo Contreras

:Created:
    - 2025-01-19
"""

from sqlmodel import SQLModel, Field, Relationship, Column, text
from sqlalchemy import String
from typing import Optional, List
from datetime import datetime


# ============================================================================
# TABLE: projects
# Schema: portfolio.projects
# ============================================================================

class ProjectBase(SQLModel):
    """Base model for Project."""
    code_name: str = Field(description="Unique project identifier for this user")
    name: str = Field(description="Project name")
    description: str = Field(description="Project description")
    highlights: str = Field(description="Key achievements and highlights")
    url: str = Field(description="Primary project URL")
    service_status: str = Field(
        default="active",
        description="Service status (active, inactive, maintenance, deprecated)"
    )


class Project(ProjectBase, table=True):
    """
    Project table - portfolio projects.

    Stores information about personal and professional projects with
    service status tracking.

    Fields:
        id: UUID primary key
        user_id: Foreign key to users
        code_name: Unique identifier per user
        name: Project name
        description: Full description
        highlights: Key achievements
        url: Primary URL (demo, repo, etc.)
        service_status: Current status (active, inactive, etc.)
        status: Record status
        created_at/updated_at: Timestamps

    Relationships:
        user: User - Project owner

    Indexes:
        - idx_projects_user: user_id
        - idx_projects_code_name: (user_id, code_name) UNIQUE
        - idx_projects_service_status: service_status

    Atlas HCL Reference: db/atlas/schema/projects.hcl
    """
    __tablename__ = "projects"
    __table_args__ = {"schema": "portfolio"}

    # Primary Key
    id: Optional[str] = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"server_default": text("gen_random_uuid()::text")}
    )

    # Status and Timestamps
    status: str = Field(default="active", index=True)
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

    # Relationships
    user: "User" = Relationship(back_populates="projects")  # type: ignore

    @property
    def is_active(self) -> bool:
        """Check if project service is currently active."""
        return self.service_status == "active" and self.status == "active"

    @property
    def is_visible(self) -> bool:
        """Check if project should be visible in portfolio."""
        return self.status == "active" and self.service_status not in ["deprecated", "archived"]

    def get_status_badge(self) -> str:
        """
        Get status badge for UI display.

        Returns:
            str: Badge text like "Active", "Inactive", etc.
        """
        badges = {
            "active": "Active",
            "inactive": "Inactive",
            "maintenance": "Maintenance",
            "deprecated": "Deprecated",
            "archived": "Archived",
        }
        return badges.get(self.service_status, "Unknown")

    # =========================================================================
    # CLASS METHODS - Query Encapsulation (Lambda functions use ONLY these)
    # Lambda functions should NEVER import from shared.database directly
    # =========================================================================

    @classmethod
    async def get_all(cls, session, user_id: str = None, service_status: str = None, skip: int = 0, limit: int = 100):
        """
        Get all projects with optional filters.

        Args:
            session: AsyncSession from dependency injection
            user_id: Optional filter by user
            service_status: Optional filter by service status
            skip: Offset for pagination
            limit: Limit for pagination

        Returns:
            List[Project]: List of projects
        """
        from sqlalchemy import select

        statement = select(cls).offset(skip).limit(limit)

        if user_id:
            statement = statement.where(cls.user_id == user_id)

        if service_status:
            statement = statement.where(cls.service_status == service_status)

        result = await session.execute(statement)
        return result.scalars().all()

    @classmethod
    async def get_by_id(cls, session, project_id: str):
        """
        Get project by ID.

        Args:
            session: AsyncSession from dependency injection
            project_id: Project UUID

        Returns:
            Project | None: Project or None
        """
        return await session.get(cls, project_id)
