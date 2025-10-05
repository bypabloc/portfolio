"""
Job Types routes.

Implements CRUD operations for job types.
Lambda functions use ONLY repositories, not models or database directly.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/01/19
"""

from fastapi import APIRouter, HTTPException, status
from shared.logger import logger
from typing import List
from pydantic import BaseModel

from shared.repositories import JobTypeRepository

router = APIRouter()


# ============================================================================
# Schemas for API Requests/Responses
# ============================================================================


class JobTypeCreateRequest(BaseModel):
    """Request schema for creating job type."""

    code_name: str
    name: str


class JobTypeResponse(BaseModel):
    """Response schema for job type data."""
    id: str
    code_name: str
    name: str
    created_at: str


# ============================================================================
# Job Type Endpoints (Repository-Based)
# ============================================================================


@router.get("/job-types", response_model=List[JobTypeResponse])
async def get_job_types(skip: int = 0, limit: int = 100):
    """
    Get list of job types.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of job types
    """
    try:
        # Use repository method (database-agnostic)
        job_types = await JobTypeRepository.get_all(skip=skip, limit=limit)

        return [
            JobTypeResponse(
                id=jt.id,
                code_name=jt.code_name,
                name=jt.name,
                created_at=jt.created_at.isoformat()
            )
            for jt in job_types
        ]

    except Exception as e:
        logger.error(f"Error getting job types: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving job types"
        )


@router.get("/job-types/{job_type_id}", response_model=JobTypeResponse)
async def get_job_type(job_type_id: str):
    """
    Get specific job type by ID.

    Args:
        job_type_id: Job type ID

    Returns:
        Job type data
    """
    try:
        # Use repository method (database-agnostic)
        job_type = await JobTypeRepository.get_by_id(job_type_id)

        if not job_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job type with ID {job_type_id} not found"
            )

        return JobTypeResponse(
            id=job_type.id,
            code_name=job_type.code_name,
            name=job_type.name,
            created_at=job_type.created_at.isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job type: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving job type"
        )


@router.post("/job-types", response_model=JobTypeResponse, status_code=status.HTTP_201_CREATED)
async def create_job_type(job_type_data: JobTypeCreateRequest):
    """
    Create new job type.

    Args:
        job_type_data: Job type creation data

    Returns:
        Created job type
    """
    try:
        # Use repository method (database-agnostic)
        job_type = await JobTypeRepository.create(job_type_data.model_dump())

        return JobTypeResponse(
            id=job_type.id,
            code_name=job_type.code_name,
            name=job_type.name,
            created_at=job_type.created_at.isoformat(),
        )

    except Exception as e:
        logger.error(f'Error creating job type: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error creating job type',
        )
