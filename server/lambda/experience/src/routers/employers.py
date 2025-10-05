"""
Employer routes.

Implements CRUD operations for employers.
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

from shared.repositories import EmployerRepository

router = APIRouter()


# ============================================================================
# Schemas for API Requests/Responses
# ============================================================================


class EmployerCreateRequest(BaseModel):
    """Request schema for creating employer."""

    code_name: str
    name: str


class EmployerResponse(BaseModel):
    """Response schema for employer data."""
    id: str
    code_name: str
    name: str
    created_at: str


# ============================================================================
# Employer Endpoints (Repository-Based)
# ============================================================================


@router.get("/employers", response_model=List[EmployerResponse])
async def get_employers(skip: int = 0, limit: int = 100):
    """
    Get list of employers.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of employers
    """
    try:
        # Use repository method (database-agnostic)
        employers = await EmployerRepository.get_all(skip=skip, limit=limit)

        return [
            EmployerResponse(
                id=emp.id,
                code_name=emp.code_name,
                name=emp.name,
                created_at=emp.created_at.isoformat()
            )
            for emp in employers
        ]

    except Exception as e:
        logger.error(f"Error getting employers: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving employers"
        )


@router.get("/employers/{employer_id}", response_model=EmployerResponse)
async def get_employer(employer_id: str):
    """
    Get specific employer by ID.

    Args:
        employer_id: Employer ID

    Returns:
        Employer data
    """
    try:
        # Use repository method (database-agnostic)
        employer = await EmployerRepository.get_by_id(employer_id)

        if not employer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employer with ID {employer_id} not found"
            )

        return EmployerResponse(
            id=employer.id,
            code_name=employer.code_name,
            name=employer.name,
            created_at=employer.created_at.isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting employer: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving employer"
        )


@router.post("/employers", response_model=EmployerResponse, status_code=status.HTTP_201_CREATED)
async def create_employer(employer_data: EmployerCreateRequest):
    """
    Create new employer.

    Args:
        employer_data: Employer creation data

    Returns:
        Created employer
    """
    try:
        # Use repository method (database-agnostic)
        employer = await EmployerRepository.create(employer_data.model_dump())

        return EmployerResponse(
            id=employer.id,
            code_name=employer.code_name,
            name=employer.name,
            created_at=employer.created_at.isoformat(),
        )

    except Exception as e:
        logger.error(f'Error creating employer: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error creating employer',
        )
