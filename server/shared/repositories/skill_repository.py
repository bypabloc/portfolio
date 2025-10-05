"""
Skill Repository - Database access layer for Skill operations.

Lambda functions should ONLY import this repository, not models or database.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/01/19
"""

from typing import List, Optional, Dict, Any

# Repository imports from shared (models and database)
from shared.models import Skill, SkillBase
from shared.database import get_db_session


class SkillRepository:
    """
    Repository for Skill entity operations.

    Encapsulates all database access logic for Skills.
    Lambda functions use ONLY this repository.
    """

    @classmethod
    async def get_all(
        cls,
        skill_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Skill]:
        """
        Get all skills with optional type filter.

        Args:
            skill_type: Optional type filter
            skip: Offset for pagination
            limit: Limit for pagination

        Returns:
            List[Skill]: Skills matching criteria
        """
        async for session in get_db_session():
            try:
                skills = await Skill.get_all(
                    session,
                    skill_type=skill_type,
                    skip=skip,
                    limit=limit
                )
                return skills
            finally:
                await session.close()

    @classmethod
    async def get_by_id(cls, skill_id: str) -> Optional[Skill]:
        """
        Get skill by ID.

        Args:
            skill_id: Skill UUID

        Returns:
            Skill | None: Skill or None
        """
        async for session in get_db_session():
            try:
                skill = await Skill.get_by_id(session, skill_id)
                return skill
            finally:
                await session.close()

    @classmethod
    async def create(cls, skill_data: Dict[str, Any]) -> Skill:
        """
        Create new skill.

        Args:
            skill_data: Skill data

        Returns:
            Skill: Created skill
        """
        async for session in get_db_session():
            try:
                db_skill = Skill(**skill_data)
                session.add(db_skill)
                await session.commit()
                await session.refresh(db_skill)
                return db_skill
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    @classmethod
    async def update(cls, skill_id: str, skill_data: Dict[str, Any]) -> Optional[Skill]:
        """
        Update skill.

        Args:
            skill_id: Skill UUID
            skill_data: Data to update

        Returns:
            Skill | None: Updated skill or None if not found
        """
        from datetime import datetime

        async for session in get_db_session():
            try:
                skill = await session.get(Skill, skill_id)
                if not skill:
                    return None

                for field, value in skill_data.items():
                    setattr(skill, field, value)

                skill.updated_at = datetime.utcnow()
                await session.commit()
                await session.refresh(skill)
                return skill
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    @classmethod
    async def delete(cls, skill_id: str) -> bool:
        """
        Delete skill.

        Args:
            skill_id: Skill UUID

        Returns:
            bool: True if deleted, False if not found
        """
        async for session in get_db_session():
            try:
                skill = await session.get(Skill, skill_id)
                if not skill:
                    return False

                await session.delete(skill)
                await session.commit()
                return True
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
