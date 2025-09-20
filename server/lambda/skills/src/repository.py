"""
Skills Repository
Uses SQLModel from shared layer
"""

from typing import Optional, List, Dict, Any
import logging

# Import from the shared layer
try:
    from database import get_session, SessionDep
    from repositories import skill_repo, SkillRepository
    from models import Skill, SkillCreate, SkillUpdate
except ImportError:
    # Fallback if layer not available - implement basic repository
    import asyncio
    from .models import Skill, SkillCreate, SkillUpdate

    class SkillRepository:
        """Fallback repository implementation"""

        async def get_skills_by_category(self, category: str) -> List[Skill]:
            # Mock data for fallback
            return [
                Skill(
                    id=1,
                    name="Python",
                    category="programming",
                    level="expert",
                    years_of_experience=5,
                    is_featured=True,
                    description="Advanced Python development"
                ),
                Skill(
                    id=2,
                    name="JavaScript",
                    category="programming",
                    level="advanced",
                    years_of_experience=4,
                    is_featured=True,
                    description="Modern JavaScript development"
                )
            ]

        async def get_featured_skills(self) -> List[Skill]:
            skills = await self.get_skills_by_category("programming")
            return [skill for skill in skills if skill.is_featured]

        async def get_all_skills(self) -> List[Skill]:
            return await self.get_skills_by_category("programming")

        async def get_skills_grouped_by_category(self) -> Dict[str, List[Skill]]:
            skills = await self.get_all_skills()
            grouped = {}
            for skill in skills:
                if skill.category not in grouped:
                    grouped[skill.category] = []
                grouped[skill.category].append(skill)
            return grouped

logger = logging.getLogger(__name__)


class SkillRepositoryWrapper:
    """Wrapper for Skill repository with session management"""

    def __init__(self):
        try:
            self._repo = skill_repo
            self._has_layer = True
        except NameError:
            self._repo = SkillRepository()
            self._has_layer = False

    async def get_skills_by_category(self, category: str) -> List[Skill]:
        """Get skills by category"""
        try:
            if self._has_layer:
                async with get_session() as session:
                    return await self._repo.get_skills_by_category(session, category)
            else:
                return await self._repo.get_skills_by_category(category)
        except Exception as e:
            logger.error(f"Error getting skills by category: {str(e)}")
            raise

    async def get_featured_skills(self) -> List[Skill]:
        """Get featured skills only"""
        try:
            if self._has_layer:
                async with get_session() as session:
                    return await self._repo.get_featured_skills(session)
            else:
                return await self._repo.get_featured_skills()
        except Exception as e:
            logger.error(f"Error getting featured skills: {str(e)}")
            raise

    async def get_all_skills(self, skip: int = 0, limit: int = 100) -> List[Skill]:
        """Get all skills with pagination"""
        try:
            if self._has_layer:
                async with get_session() as session:
                    return await self._repo.get_all(session, skip=skip, limit=limit)
            else:
                return await self._repo.get_all_skills()
        except Exception as e:
            logger.error(f"Error getting all skills: {str(e)}")
            raise

    async def get_skills_grouped_by_category(self) -> Dict[str, List[Skill]]:
        """Get skills grouped by category"""
        try:
            if self._has_layer:
                async with get_session() as session:
                    return await self._repo.get_skills_grouped_by_category(session)
            else:
                return await self._repo.get_skills_grouped_by_category()
        except Exception as e:
            logger.error(f"Error getting skills grouped by category: {str(e)}")
            raise

    async def search_skills(self, query: str) -> List[Skill]:
        """Search skills by name or description"""
        try:
            if self._has_layer:
                async with get_session() as session:
                    return await self._repo.search_skills(session, query)
            else:
                # Fallback implementation
                all_skills = await self.get_all_skills()
                return [
                    skill for skill in all_skills
                    if query.lower() in skill.name.lower()
                    or (skill.description and query.lower() in skill.description.lower())
                ]
        except Exception as e:
            logger.error(f"Error searching skills: {str(e)}")
            raise

    async def get_by_level(self, level: str) -> List[Skill]:
        """Get skills by proficiency level"""
        try:
            if self._has_layer:
                async with get_session() as session:
                    return await self._repo.get_by_level(session, level)
            else:
                # Fallback implementation
                all_skills = await self.get_all_skills()
                return [skill for skill in all_skills if skill.level == level]
        except Exception as e:
            logger.error(f"Error getting skills by level: {str(e)}")
            raise