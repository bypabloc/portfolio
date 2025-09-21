"""
Skills Service
Business logic layer for skills management
"""

from typing import Optional, List, Dict, Any
import logging

from models import Skill, SkillResponse, SkillsListResponse, SkillsCategoryResponse
from repository import SkillRepositoryWrapper

logger = logging.getLogger(__name__)


class SkillsService:
    """Business logic service for skills management"""

    def __init__(self, repository: Optional[SkillRepositoryWrapper] = None):
        self.repository = repository or SkillRepositoryWrapper()

    async def get_skills_by_category(self, category: str) -> SkillsListResponse:
        """
        Get skills by category

        Args:
            category: Category name to filter by

        Returns:
            SkillsListResponse with filtered skills
        """
        try:
            skills = await self.repository.get_skills_by_category(category)

            skills_response = [
                SkillResponse(
                    id=skill.id,
                    name=skill.name,
                    category=skill.category,
                    level=skill.level,
                    years_of_experience=skill.years_of_experience,
                    is_featured=skill.is_featured,
                    description=skill.description
                )
                for skill in skills
            ]

            return SkillsListResponse(
                skills=skills_response,
                total=len(skills_response),
                category=category
            )

        except Exception as e:
            logger.error(f"Service error getting skills by category: {str(e)}")
            raise

    async def get_featured_skills(self) -> SkillsListResponse:
        """
        Get featured skills only

        Returns:
            SkillsListResponse with featured skills
        """
        try:
            skills = await self.repository.get_featured_skills()

            skills_response = [
                SkillResponse(
                    id=skill.id,
                    name=skill.name,
                    category=skill.category,
                    level=skill.level,
                    years_of_experience=skill.years_of_experience,
                    is_featured=skill.is_featured,
                    description=skill.description
                )
                for skill in skills
            ]

            return SkillsListResponse(
                skills=skills_response,
                total=len(skills_response),
                category=None
            )

        except Exception as e:
            logger.error(f"Service error getting featured skills: {str(e)}")
            raise

    async def get_all_skills(self, skip: int = 0, limit: int = 100) -> SkillsListResponse:
        """
        Get all skills with pagination

        Args:
            skip: Number of skills to skip
            limit: Maximum number of skills to return

        Returns:
            SkillsListResponse with all skills
        """
        try:
            skills = await self.repository.get_all_skills(skip=skip, limit=limit)

            skills_response = [
                SkillResponse(
                    id=skill.id,
                    name=skill.name,
                    category=skill.category,
                    level=skill.level,
                    years_of_experience=skill.years_of_experience,
                    is_featured=skill.is_featured,
                    description=skill.description
                )
                for skill in skills
            ]

            return SkillsListResponse(
                skills=skills_response,
                total=len(skills_response),
                category=None
            )

        except Exception as e:
            logger.error(f"Service error getting all skills: {str(e)}")
            raise

    async def get_skills_grouped_by_category(self) -> SkillsCategoryResponse:
        """
        Get skills grouped by category

        Returns:
            SkillsCategoryResponse with categorized skills
        """
        try:
            grouped_skills = await self.repository.get_skills_grouped_by_category()

            # Convert to response format
            categories = {}
            for category, skills in grouped_skills.items():
                categories[category] = [
                    SkillResponse(
                        id=skill.id,
                        name=skill.name,
                        category=skill.category,
                        level=skill.level,
                        years_of_experience=skill.years_of_experience,
                        is_featured=skill.is_featured,
                        description=skill.description
                    ).dict()
                    for skill in skills
                ]

            return SkillsCategoryResponse(categories=categories)

        except Exception as e:
            logger.error(f"Service error getting skills grouped by category: {str(e)}")
            raise

    async def search_skills(self, query: str) -> SkillsListResponse:
        """
        Search skills by name or description

        Args:
            query: Search query

        Returns:
            SkillsListResponse with matching skills
        """
        try:
            if not query or len(query.strip()) < 2:
                raise ValueError("Search query must be at least 2 characters")

            skills = await self.repository.search_skills(query.strip())

            skills_response = [
                SkillResponse(
                    id=skill.id,
                    name=skill.name,
                    category=skill.category,
                    level=skill.level,
                    years_of_experience=skill.years_of_experience,
                    is_featured=skill.is_featured,
                    description=skill.description
                )
                for skill in skills
            ]

            return SkillsListResponse(
                skills=skills_response,
                total=len(skills_response),
                category=None
            )

        except Exception as e:
            logger.error(f"Service error searching skills: {str(e)}")
            raise

    async def get_skills_by_level(self, level: str) -> SkillsListResponse:
        """
        Get skills by proficiency level

        Args:
            level: Proficiency level (beginner, intermediate, advanced, expert)

        Returns:
            SkillsListResponse with skills of specified level
        """
        try:
            valid_levels = ['beginner', 'intermediate', 'advanced', 'expert']
            if level.lower() not in valid_levels:
                raise ValueError(f"Invalid level. Must be one of: {valid_levels}")

            skills = await self.repository.get_by_level(level.lower())

            skills_response = [
                SkillResponse(
                    id=skill.id,
                    name=skill.name,
                    category=skill.category,
                    level=skill.level,
                    years_of_experience=skill.years_of_experience,
                    is_featured=skill.is_featured,
                    description=skill.description
                )
                for skill in skills
            ]

            return SkillsListResponse(
                skills=skills_response,
                total=len(skills_response),
                category=None
            )

        except Exception as e:
            logger.error(f"Service error getting skills by level: {str(e)}")
            raise

    async def health_check(self) -> Dict[str, Any]:
        """
        Health check for the service

        Returns:
            Health status information
        """
        try:
            # Try to get skills to test database connection
            skills = await self.repository.get_featured_skills()

            return {
                "status": "healthy",
                "database_connected": True,
                "skills_count": len(skills),
                "service": "skills"
            }

        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "database_connected": False,
                "error": str(e),
                "service": "skills"
            }