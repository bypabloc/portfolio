"""
Project management routes.

Implements CRUD operations for projects.
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

from shared.repositories import ProjectRepository

router = APIRouter()


# ============================================================================
# Schemas for API Requests/Responses
# ============================================================================


class ProjectCreateRequest(BaseModel):
    """Request schema for creating project."""

    user_id: str
    code_name: str
    name: str
    description: Optional[str] = None
    highlights: Optional[str] = None
    url: Optional[str] = None
    service_status: str = 'active'


class ProjectUpdateRequest(BaseModel):
    """Request schema for updating project."""

    code_name: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    highlights: Optional[str] = None
    url: Optional[str] = None
    service_status: Optional[str] = None


class ProjectPublicResponse(BaseModel):
    """Public response schema for project data."""

    id: str
    code_name: str
    name: str
    description: Optional[str]
    highlights: Optional[str]
    url: Optional[str]
    service_status: str
    user_id: str
    created_at: str


# ============================================================================
# Project CRUD Endpoints (Repository-Based)
# ============================================================================


@router.get('/projects', response_model=List[ProjectPublicResponse])
async def get_projects(
    user_id: Optional[str] = None,
    service_status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
):
    """
    Get list of projects.

    Args:
        user_id: Optional user filter
        service_status: Optional status filter
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of projects
    """
    try:
        # Use repository method (database-agnostic)
        projects = await ProjectRepository.get_all(
            user_id=user_id, service_status=service_status, skip=skip, limit=limit
        )

        return [
            ProjectPublicResponse(
                id=proj.id,
                code_name=proj.code_name,
                name=proj.name,
                description=proj.description,
                highlights=proj.highlights,
                url=proj.url,
                service_status=proj.service_status,
                user_id=proj.user_id,
                created_at=proj.created_at.isoformat(),
            )
            for proj in projects
        ]

    except Exception as e:
        logger.error(f'Error getting projects: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error retrieving projects',
        )


@router.get('/projects/{project_id}', response_model=ProjectPublicResponse)
async def get_project(project_id: str):
    """
    Get specific project by ID.

    Args:
        project_id: Project ID

    Returns:
        Project data
    """
    try:
        # Use repository method (database-agnostic)
        project = await ProjectRepository.get_by_id(project_id)

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Project with ID {project_id} not found',
            )

        return ProjectPublicResponse(
            id=project.id,
            code_name=project.code_name,
            name=project.name,
            description=project.description,
            highlights=project.highlights,
            url=project.url,
            service_status=project.service_status,
            user_id=project.user_id,
            created_at=project.created_at.isoformat(),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Error getting project: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error retrieving project',
        )


@router.post(
    '/projects',
    response_model=ProjectPublicResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(project_data: ProjectCreateRequest):
    """
    Create new project.

    Args:
        project_data: Project creation data

    Returns:
        Created project
    """
    try:
        # Use repository method (database-agnostic)
        project = await ProjectRepository.create(project_data.model_dump())

        return ProjectPublicResponse(
            id=project.id,
            code_name=project.code_name,
            name=project.name,
            description=project.description,
            highlights=project.highlights,
            url=project.url,
            service_status=project.service_status,
            user_id=project.user_id,
            created_at=project.created_at.isoformat(),
        )

    except Exception as e:
        logger.error(f'Error creating project: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error creating project',
        )


@router.patch('/projects/{project_id}', response_model=ProjectPublicResponse)
async def update_project(project_id: str, update_data: ProjectUpdateRequest):
    """
    Update project.

    Args:
        project_id: Project ID
        update_data: Data to update

    Returns:
        Updated project
    """
    try:
        # Use repository method (database-agnostic)
        project = await ProjectRepository.update(
            project_id, update_data.model_dump(exclude_unset=True)
        )

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Project with ID {project_id} not found',
            )

        return ProjectPublicResponse(
            id=project.id,
            code_name=project.code_name,
            name=project.name,
            description=project.description,
            highlights=project.highlights,
            url=project.url,
            service_status=project.service_status,
            user_id=project.user_id,
            created_at=project.created_at.isoformat(),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Error updating project: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error updating project',
        )


@router.delete('/projects/{project_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: str):
    """
    Delete project.

    Args:
        project_id: Project ID

    Returns:
        No content
    """
    try:
        # Use repository method (database-agnostic)
        deleted = await ProjectRepository.delete(project_id)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Project with ID {project_id} not found',
            )

        return None

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Error deleting project: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error deleting project',
        )
