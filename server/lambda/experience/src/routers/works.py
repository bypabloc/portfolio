"""
Work experience routes.

CRUD operations for work experience records.
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
from datetime import date

from shared.repositories import WorkRepository

router = APIRouter()


# ============================================================================
# Schemas for API Requests/Responses
# ============================================================================


class WorkCreateRequest(BaseModel):
    """Request schema for creating work experience."""

    user_id: str
    employer_id: Optional[str] = None
    job_type_id: str
    start_date: date
    end_date: Optional[date] = None
    description: Optional[str] = None


class WorkUpdateRequest(BaseModel):
    """Request schema for updating work experience."""

    employer_id: Optional[str] = None
    job_type_id: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None


class WorkPublicResponse(BaseModel):
    """Public response schema for work data."""

    id: str
    user_id: str
    employer_id: Optional[str]
    job_type_id: str
    start_date: str
    end_date: Optional[str]
    summary: Optional[str]  # Corregido: description → summary para match con Work model
    created_at: str
    is_current: bool


# ============================================================================
# Work CRUD Endpoints (Repository-Based)
# ============================================================================


@router.get('/works', response_model=List[WorkPublicResponse])
async def get_works(user_id: Optional[str] = None, skip: int = 0, limit: int = 100):
    """
    Get list of work experiences.

    Args:
        user_id: Optional user filter
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of works
    """
    try:
        # Use repository method (database-agnostic)
        works = await WorkRepository.get_all(user_id=user_id, skip=skip, limit=limit)

        return [
            WorkPublicResponse(
                id=work.id,
                user_id=work.user_id,
                employer_id=work.employer_id,
                job_type_id=work.job_type_id,
                start_date=work.start_date.isoformat(),
                end_date=work.end_date.isoformat() if work.end_date else None,
                summary=work.summary,  # Corregido: description → summary
                created_at=work.created_at.isoformat(),
                is_current=work.is_current,
            )
            for work in works
        ]

    except Exception as e:
        logger.error(f'Error getting works: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error retrieving work experiences',
        )


@router.get('/works/{work_id}', response_model=WorkPublicResponse)
async def get_work(work_id: str):
    """
    Get specific work experience by ID.

    Args:
        work_id: Work ID

    Returns:
        Work data
    """
    try:
        # Use repository method (database-agnostic)
        work = await WorkRepository.get_by_id(work_id)

        if not work:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Work with ID {work_id} not found',
            )

        return WorkPublicResponse(
            id=work.id,
            user_id=work.user_id,
            employer_id=work.employer_id,
            job_type_id=work.job_type_id,
            start_date=work.start_date.isoformat(),
            end_date=work.end_date.isoformat() if work.end_date else None,
            summary=work.summary,  # Corregido: description → summary
            created_at=work.created_at.isoformat(),
            is_current=work.is_current,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Error getting work: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error retrieving work experience',
        )


@router.post(
    '/works', response_model=WorkPublicResponse, status_code=status.HTTP_201_CREATED
)
async def create_work(work_data: WorkCreateRequest):
    """
    Create new work experience.

    Args:
        work_data: Work creation data

    Returns:
        Created work
    """
    try:
        # Use repository method (database-agnostic)
        work = await WorkRepository.create(work_data.model_dump())

        return WorkPublicResponse(
            id=work.id,
            user_id=work.user_id,
            employer_id=work.employer_id,
            job_type_id=work.job_type_id,
            start_date=work.start_date.isoformat(),
            end_date=work.end_date.isoformat() if work.end_date else None,
            summary=work.summary,  # Corregido: description → summary
            created_at=work.created_at.isoformat(),
            is_current=work.is_current,
        )

    except Exception as e:
        logger.error(f'Error creating work: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error creating work experience',
        )


@router.patch('/works/{work_id}', response_model=WorkPublicResponse)
async def update_work(work_id: str, update_data: WorkUpdateRequest):
    """
    Update work experience.

    Args:
        work_id: Work ID
        update_data: Data to update

    Returns:
        Updated work
    """
    try:
        # Use repository method (database-agnostic)
        work = await WorkRepository.update(
            work_id, update_data.model_dump(exclude_unset=True)
        )

        if not work:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Work with ID {work_id} not found',
            )

        return WorkPublicResponse(
            id=work.id,
            user_id=work.user_id,
            employer_id=work.employer_id,
            job_type_id=work.job_type_id,
            start_date=work.start_date.isoformat(),
            end_date=work.end_date.isoformat() if work.end_date else None,
            summary=work.summary,  # Corregido: description → summary
            created_at=work.created_at.isoformat(),
            is_current=work.is_current,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Error updating work: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error updating work experience',
        )


@router.delete('/works/{work_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_work(work_id: str):
    """
    Delete work experience.

    Args:
        work_id: Work ID

    Returns:
        No content
    """
    try:
        # Use repository method (database-agnostic)
        deleted = await WorkRepository.delete(work_id)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Work with ID {work_id} not found',
            )

        return None

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Error deleting work: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error deleting work',
        )
