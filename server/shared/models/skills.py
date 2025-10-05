"""
Skill models aligned with Atlas HCL schema.

IMPORTANT: Uses 'type' field instead of 'category' as per Atlas schema.

Schema alignment:
- skills.hcl -> Skill model
- works_technical_skills -> M2M relationship with works
- works_soft_skills -> M2M relationship with works
- skills_keywords -> M2M relationship with keywords

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
# TABLE: skills
# Schema: portfolio.skills
# ============================================================================

class SkillBase(SQLModel):
    """
    Base model for Skill.

    CRITICAL CORRECTION from documentation:
    - Uses 'type' field (technical, soft, language, etc.)
    - NO 'category' field (does not exist in Atlas schema)
    - NO 'level' field (does not exist in Atlas schema)
    - NO 'years_experience' field (does not exist in Atlas schema)
    - NO 'is_featured' field (does not exist in Atlas schema)
    """
    code_name: str = Field(
        sa_column=Column(String, unique=True, index=True),
        description="Unique skill identifier (e.g., 'python', 'fastapi')"
    )
    name: str = Field(description="Skill name (e.g., 'Python', 'FastAPI')")
    description: Optional[str] = Field(
        default=None,
        description="Skill description and context"
    )
    type: str = Field(
        index=True,
        description="Skill type: 'technical', 'soft', 'language', etc."
    )


class Skill(SkillBase, table=True):
    """
    Skill table - technical and soft skills catalog.

    Stores skills with type classification. Relationships to works
    are managed through separate M2M tables.

    Fields:
        id: UUID primary key
        code_name: Unique identifier (e.g., 'python')
        name: Display name
        description: Skill description
        type: Skill type (technical, soft, language, etc.)
        status: Record status
        created_at/updated_at: Timestamps

    Relationships:
        (M2M relationships via works_technical_skills and works_soft_skills
         are typically defined in the Link tables, not here)

    Indexes:
        - idx_skills_code_name: code_name UNIQUE
        - idx_skills_type: type

    Atlas HCL Reference: db/atlas/schema/skills.hcl

    Example usage:
        # Create a technical skill
        skill = Skill(
            code_name="python",
            name="Python",
            description="High-level programming language",
            type="technical"
        )

        # Create a soft skill
        soft_skill = Skill(
            code_name="leadership",
            name="Leadership",
            description="Team leadership and mentoring",
            type="soft"
        )

        # Create a language skill
        lang_skill = Skill(
            code_name="spanish",
            name="Spanish",
            description="Native fluency",
            type="language"
        )
    """
    __tablename__ = "skills"
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

    @property
    def is_technical(self) -> bool:
        """Check if this is a technical skill."""
        return self.type == "technical"

    @property
    def is_soft(self) -> bool:
        """Check if this is a soft skill."""
        return self.type == "soft"

    @property
    def is_language(self) -> bool:
        """Check if this is a language skill."""
        return self.type == "language"

    def get_type_badge(self) -> str:
        """
        Get type badge for UI display.

        Returns:
            str: Badge text like "Technical", "Soft", "Language"
        """
        badges = {
            "technical": "Technical",
            "soft": "Soft",
            "language": "Language",
            "tool": "Tool",
            "framework": "Framework",
            "methodology": "Methodology",
        }
        return badges.get(self.type, self.type.capitalize())

    # =========================================================================
    # CLASS METHODS - Query Encapsulation (Lambda functions use ONLY these)
    # Lambda functions should NEVER import from shared.database directly
    # =========================================================================

    @classmethod
    async def get_all(cls, session, skill_type: str = None, skip: int = 0, limit: int = 100):
        """
        Get all skills with optional type filter.

        Args:
            session: AsyncSession from dependency injection
            skill_type: Optional filter by type (technical, soft, language)
            skip: Offset for pagination
            limit: Limit for pagination

        Returns:
            List[Skill]: List of skills
        """
        from sqlalchemy import select

        statement = select(cls).offset(skip).limit(limit)

        if skill_type:
            statement = statement.where(cls.type == skill_type)

        result = await session.execute(statement)
        return result.scalars().all()

    @classmethod
    async def get_by_id(cls, session, skill_id: str):
        """
        Get skill by ID.

        Args:
            session: AsyncSession from dependency injection
            skill_id: Skill UUID

        Returns:
            Skill | None: Skill or None
        """
        return await session.get(cls, skill_id)
