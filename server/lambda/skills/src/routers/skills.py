"""
Skill management routes.

Implements CRUD operations for skills.
Lambda functions use ONLY repositories, not models or database directly.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/01/19
"""

from fastapi import APIRouter, HTTPException, status
from shared.logger import logger
from typing import List, Optional
from pydantic import BaseModel

from shared.repositories import SkillRepository

router = APIRouter()


# ============================================================================
# Schemas for API Requests/Responses
# ============================================================================


class SkillCreateRequest(BaseModel):
    """Request schema for creating skill."""

    code_name: str
    name: str
    description: Optional[str] = None
    type: str


class SkillUpdateRequest(BaseModel):
    """Request schema for updating skill."""

    code_name: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None


class SkillPublicResponse(BaseModel):
    """Public response schema for skill data."""

    id: str
    code_name: str
    name: str
    description: Optional[str]
    type: str
    created_at: str


# ============================================================================
# Skill CRUD Endpoints (Repository-Based)
# ============================================================================


@router.get('/skills', response_model=List[SkillPublicResponse])
async def get_skills(skill_type: Optional[str] = None, skip: int = 0, limit: int = 100):
    """
    Get list of skills.

    Args:
        skill_type: Optional type filter
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of skills
    """
    try:
        # Use repository method (database-agnostic)
        skills = await SkillRepository.get_all(
            skill_type=skill_type, skip=skip, limit=limit
        )

        return [
            SkillPublicResponse(
                id=skill.id,
                code_name=skill.code_name,
                name=skill.name,
                description=skill.description,
                type=skill.type,
                created_at=skill.created_at.isoformat(),
            )
            for skill in skills
        ]

    except Exception as e:
        logger.error(f'Error getting skills: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error retrieving skills',
        )


@router.get('/skills/{skill_id}', response_model=SkillPublicResponse)
async def get_skill(skill_id: str):
    """
    Get specific skill by ID.

    Args:
        skill_id: Skill ID

    Returns:
        Skill data
    """
    try:
        # Use repository method (database-agnostic)
        skill = await SkillRepository.get_by_id(skill_id)

        if not skill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Skill with ID {skill_id} not found',
            )

        return SkillPublicResponse(
            id=skill.id,
            code_name=skill.code_name,
            name=skill.name,
            description=skill.description,
            type=skill.type,
            created_at=skill.created_at.isoformat(),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Error getting skill: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error retrieving skill',
        )


@router.post(
    '/skills', response_model=SkillPublicResponse, status_code=status.HTTP_201_CREATED
)
async def create_skill(skill_data: SkillCreateRequest):
    """
    Create new skill.

    Args:
        skill_data: Skill creation data

    Returns:
        Created skill
    """
    try:
        # Use repository method (database-agnostic)
        skill = await SkillRepository.create(skill_data.model_dump())

        return SkillPublicResponse(
            id=skill.id,
            code_name=skill.code_name,
            name=skill.name,
            description=skill.description,
            type=skill.type,
            created_at=skill.created_at.isoformat(),
        )

    except Exception as e:
        logger.error(f'Error creating skill: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error creating skill',
        )


@router.patch('/skills/{skill_id}', response_model=SkillPublicResponse)
async def update_skill(skill_id: str, update_data: SkillUpdateRequest):
    """
    Update skill.

    Args:
        skill_id: Skill ID
        update_data: Data to update

    Returns:
        Updated skill
    """
    try:
        # Use repository method (database-agnostic)
        skill = await SkillRepository.update(
            skill_id, update_data.model_dump(exclude_unset=True)
        )

        if not skill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Skill with ID {skill_id} not found',
            )

        return SkillPublicResponse(
            id=skill.id,
            code_name=skill.code_name,
            name=skill.name,
            description=skill.description,
            type=skill.type,
            created_at=skill.created_at.isoformat(),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Error updating skill: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error updating skill',
        )


@router.delete('/skills/{skill_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(skill_id: str):
    """
    Delete skill.

    Args:
        skill_id: Skill ID

    Returns:
        No content
    """
    try:
        # Use repository method (database-agnostic)
        deleted = await SkillRepository.delete(skill_id)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Skill with ID {skill_id} not found',
            )

        return None

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Error deleting skill: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error deleting skill',
        )
