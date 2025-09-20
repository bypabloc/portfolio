"""
Skills Service Models
Using SQLModel from shared layer
"""

from typing import Optional, List
from sqlmodel import SQLModel


# Import SQLModel models from the layer
try:
    from models import (
        Skill,
        SkillBase,
        SkillCreate,
        SkillUpdate
    )
except ImportError:
    # Fallback Pydantic models if layer not available
    class SkillBase(SQLModel):
        name: str
        category: str
        level: str
        years_of_experience: Optional[int] = None
        is_featured: bool = False
        description: Optional[str] = None

    class Skill(SkillBase):
        id: Optional[int] = None

    class SkillCreate(SkillBase):
        pass

    class SkillUpdate(SQLModel):
        name: Optional[str] = None
        category: Optional[str] = None
        level: Optional[str] = None
        years_of_experience: Optional[int] = None
        is_featured: Optional[bool] = None
        description: Optional[str] = None


# Response models for API
class SkillResponse(SkillBase):
    """Response model for skill API"""
    id: int

    @property
    def proficiency_percentage(self) -> int:
        """Get proficiency as percentage."""
        level_mapping = {
            'beginner': 25,
            'intermediate': 50,
            'advanced': 75,
            'expert': 100
        }
        return level_mapping.get(self.level, 0)


class SkillsListResponse(SQLModel):
    """Response model for skills list"""
    skills: List[SkillResponse]
    total: int
    category: Optional[str] = None


class SkillsCategoryResponse(SQLModel):
    """Response model for skills grouped by category"""
    categories: dict  # Dict[str, List[SkillResponse]] but using dict for JSON compatibility