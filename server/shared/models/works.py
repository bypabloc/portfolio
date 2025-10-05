"""
Work experience models aligned with Atlas HCL schema.

Includes Work, Employer, and JobType models with proper relationships.

Schema alignment:
- works.hcl -> Work model
- employers.hcl -> Employer model
- job_types.hcl -> JobType model

:Authors:
    - Pablo Contreras

:Created:
    - 2025-01-19
"""

from sqlmodel import SQLModel, Field, Relationship, Column, text
from sqlalchemy import String, Date
from typing import Optional, List
from datetime import datetime, date


# ============================================================================
# TABLE: employers
# Schema: portfolio.employers
# ============================================================================

class EmployerBase(SQLModel):
    """Base model for Employer."""
    code_name: str = Field(
        sa_column=Column(String, unique=True, index=True),
        description="Unique employer code (e.g., 'destacame', 'apple')"
    )
    name: str = Field(description="Company name")
    description: Optional[str] = Field(default=None, description="Company description")
    location: Optional[str] = Field(default=None, description="Company location")
    url: Optional[str] = Field(default=None, description="Company website")


class Employer(EmployerBase, table=True):
    """
    Employer table - companies and organizations.

    Stores information about employers referenced in work experience.

    Fields:
        id: UUID primary key
        code_name: Unique identifier (e.g., 'destacame')
        name: Company name
        description: Company description
        location: Company location
        url: Company website
        status: Record status
        created_at/updated_at: Timestamps

    Relationships:
        works: List[Work] - Work experiences at this employer

    Atlas HCL Reference: db/atlas/schema/employers.hcl
    """
    __tablename__ = "employers"
    __table_args__ = {"schema": "portfolio"}

    # Primary Key
    id: Optional[str] = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"server_default": text("gen_random_uuid()::text")}
    )

    # Status and Timestamps
    status: str = Field(default="active")
    created_at: datetime = Field(
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")}
    )
    updated_at: Optional[datetime] = None

    # Relationships
    works: List["Work"] = Relationship(back_populates="employer")

    # =========================================================================
    # CLASS METHODS - Query Encapsulation (Lambda functions use ONLY these)
    # Lambda functions should NEVER import from shared.database directly
    # =========================================================================

    @classmethod
    async def get_all(cls, session, skip: int = 0, limit: int = 100):
        """Get all employers."""
        from sqlalchemy import select

        statement = select(cls).offset(skip).limit(limit)
        result = await session.execute(statement)
        return result.scalars().all()

    @classmethod
    async def get_by_id(cls, session, employer_id: str):
        """Get employer by ID."""
        return await session.get(cls, employer_id)


# ============================================================================
# TABLE: job_types
# Schema: portfolio.job_types
# ============================================================================

class JobTypeBase(SQLModel):
    """Base model for JobType."""
    code_name: str = Field(
        sa_column=Column(String, unique=True, index=True),
        description="Unique job type code (e.g., 'full_time', 'contract')"
    )
    name: str = Field(description="Job type name (e.g., 'Full Time', 'Contract')")
    description: Optional[str] = Field(default=None, description="Job type description")


class JobType(JobTypeBase, table=True):
    """
    JobType table - types of employment.

    Defines employment types: full-time, part-time, contract, freelance, etc.

    Fields:
        id: UUID primary key
        code_name: Unique identifier (e.g., 'full_time')
        name: Display name
        description: Type description
        status: Record status
        created_at/updated_at: Timestamps

    Relationships:
        works: List[Work] - Work experiences of this type

    Atlas HCL Reference: db/atlas/schema/job_types.hcl
    """
    __tablename__ = "job_types"
    __table_args__ = {"schema": "portfolio"}

    # Primary Key
    id: Optional[str] = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"server_default": text("gen_random_uuid()::text")}
    )

    # Status and Timestamps
    status: str = Field(default="active")
    created_at: datetime = Field(
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")}
    )
    updated_at: Optional[datetime] = None

    # Relationships
    works: List["Work"] = Relationship(back_populates="job_type")

    # =========================================================================
    # CLASS METHODS - Query Encapsulation (Lambda functions use ONLY these)
    # Lambda functions should NEVER import from shared.database directly
    # =========================================================================

    @classmethod
    async def get_all(cls, session, skip: int = 0, limit: int = 100):
        """Get all job types."""
        from sqlalchemy import select

        statement = select(cls).offset(skip).limit(limit)
        result = await session.execute(statement)
        return result.scalars().all()

    @classmethod
    async def get_by_id(cls, session, job_type_id: str):
        """Get job type by ID."""
        return await session.get(cls, job_type_id)


# ============================================================================
# TABLE: works
# Schema: portfolio.works
# ============================================================================

class WorkBase(SQLModel):
    """Base model for Work experience."""
    code_name: str = Field(description="Unique work identifier for this user")
    name: str = Field(description="Job title / Position name")
    position: str = Field(description="Position held")
    summary: Optional[str] = Field(default=None, description="Work summary")
    responsibilities_n_projects: Optional[str] = Field(
        default=None,
        description="Responsibilities and projects undertaken"
    )
    achievements: Optional[str] = Field(default=None, description="Key achievements")
    start_date: date = Field(
        sa_column=Column(Date, nullable=False),
        description="Employment start date"
    )
    end_date: Optional[date] = Field(
        default=None,
        sa_column=Column(Date, nullable=True),
        description="Employment end date (NULL if current)"
    )


class Work(WorkBase, table=True):
    """
    Work table - professional experience.

    Stores work experience history with relationships to employers and job types.

    Fields:
        id: UUID primary key
        user_id: Foreign key to users
        employer_id: Foreign key to employers (nullable)
        job_type_id: Foreign key to job_types
        code_name: Unique identifier per user
        name: Job title
        position: Position held
        start_date: Start date
        end_date: End date (NULL if current)
        summary: Work summary
        responsibilities_n_projects: Detailed responsibilities
        achievements: Key achievements
        status: Record status
        created_at/updated_at: Timestamps

    Relationships:
        user: User - User who had this experience
        employer: Employer - Employer for this work (optional)
        job_type: JobType - Type of employment

    Indexes:
        - idx_works_user: user_id
        - idx_works_dates: (start_date, end_date)
        - idx_works_code_name: (user_id, code_name) UNIQUE

    Atlas HCL Reference: db/atlas/schema/works.hcl
    """
    __tablename__ = "works"
    __table_args__ = {"schema": "portfolio"}

    # Primary Key
    id: Optional[str] = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"server_default": text("gen_random_uuid()::text")}
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
    employer_id: Optional[str] = Field(
        default=None,
        foreign_key="portfolio.employers.id",
        description="Reference to employer (optional)"
    )
    job_type_id: str = Field(
        foreign_key="portfolio.job_types.id",
        description="Reference to job type"
    )

    # Relationships
    user: "User" = Relationship(back_populates="works")  # type: ignore
    employer: Optional[Employer] = Relationship(back_populates="works")
    job_type: JobType = Relationship(back_populates="works")

    @property
    def is_current(self) -> bool:
        """Check if this is current employment (end_date is NULL)."""
        return self.end_date is None

    @property
    def duration_months(self) -> Optional[int]:
        """
        Calculate duration in months.

        Returns:
            int: Duration in months, or None if start_date missing
        """
        if not self.start_date:
            return None

        end = self.end_date or date.today()
        years = end.year - self.start_date.year
        months = end.month - self.start_date.month
        return years * 12 + months

    def duration_str(self) -> str:
        """
        Get human-readable duration.

        Returns:
            str: Duration like "2 years 3 months" or "Present"

        Example:
            work.duration_str()  # "1 year 6 months"
        """
        months = self.duration_months
        if months is None:
            return "Unknown duration"

        years = months // 12
        remaining_months = months % 12

        parts = []
        if years > 0:
            parts.append(f"{years} year{'s' if years != 1 else ''}")
        if remaining_months > 0:
            parts.append(f"{remaining_months} month{'s' if remaining_months != 1 else ''}")

        return " ".join(parts) if parts else "Less than a month"

    # =========================================================================
    # CLASS METHODS - Query Encapsulation (Lambda functions use ONLY these)
    # Lambda functions should NEVER import from shared.database directly
    # =========================================================================

    @classmethod
    async def get_all(cls, session, user_id: str = None, skip: int = 0, limit: int = 100):
        """
        Get all works with optional user filter.

        Args:
            session: AsyncSession from dependency injection
            user_id: Optional user ID to filter by
            skip: Offset for pagination
            limit: Limit for pagination

        Returns:
            List[Work]: Works with eager loaded relationships
        """
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload

        statement = (
            select(cls)
            .options(selectinload(cls.employer))
            .options(selectinload(cls.job_type))
            .offset(skip)
            .limit(limit)
        )

        if user_id:
            statement = statement.where(cls.user_id == user_id)

        result = await session.execute(statement)
        return result.scalars().all()

    @classmethod
    async def get_by_id(cls, session, work_id: str):
        """
        Get work by ID with eager loaded relationships.

        Args:
            session: AsyncSession from dependency injection
            work_id: Work UUID

        Returns:
            Work | None: Work with relationships or None
        """
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload

        statement = (
            select(cls)
            .options(selectinload(cls.employer))
            .options(selectinload(cls.job_type))
            .where(cls.id == work_id)
        )
        result = await session.execute(statement)
        return result.scalars().first()
