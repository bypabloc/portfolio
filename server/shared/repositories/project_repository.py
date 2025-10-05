"""
Project Repository - Database access layer for Project operations.

Lambda functions should ONLY import this repository, not models or database.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/01/19
"""

from typing import List, Optional, Dict, Any

# Repository imports from shared (models and database)
from shared.models import Project, ProjectBase
from shared.database import get_db_session


class ProjectRepository:
    """
    Repository for Project entity operations.

    Encapsulates all database access logic for Projects.
    Lambda functions use ONLY this repository.
    """

    @classmethod
    async def get_all(
        cls,
        user_id: Optional[str] = None,
        service_status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Project]:
        """
        Get all projects with optional filters.

        Args:
            user_id: Optional user filter
            service_status: Optional status filter
            skip: Offset for pagination
            limit: Limit for pagination

        Returns:
            List[Project]: Projects matching criteria
        """
        async for session in get_db_session():
            try:
                projects = await Project.get_all(
                    session,
                    user_id=user_id,
                    service_status=service_status,
                    skip=skip,
                    limit=limit
                )
                return projects
            finally:
                await session.close()

    @classmethod
    async def get_by_id(cls, project_id: str) -> Optional[Project]:
        """
        Get project by ID.

        Args:
            project_id: Project UUID

        Returns:
            Project | None: Project or None
        """
        async for session in get_db_session():
            try:
                project = await Project.get_by_id(session, project_id)
                return project
            finally:
                await session.close()

    @classmethod
    async def create(cls, project_data: Dict[str, Any]) -> Project:
        """
        Create new project.

        Args:
            project_data: Project data

        Returns:
            Project: Created project
        """
        async for session in get_db_session():
            try:
                db_project = Project(**project_data)
                session.add(db_project)
                await session.commit()
                await session.refresh(db_project)
                return db_project
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    @classmethod
    async def update(cls, project_id: str, project_data: Dict[str, Any]) -> Optional[Project]:
        """
        Update project.

        Args:
            project_id: Project UUID
            project_data: Data to update

        Returns:
            Project | None: Updated project or None if not found
        """
        from datetime import datetime

        async for session in get_db_session():
            try:
                project = await session.get(Project, project_id)
                if not project:
                    return None

                for field, value in project_data.items():
                    setattr(project, field, value)

                project.updated_at = datetime.utcnow()
                await session.commit()
                await session.refresh(project)
                return project
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    @classmethod
    async def delete(cls, project_id: str) -> bool:
        """
        Delete project.

        Args:
            project_id: Project UUID

        Returns:
            bool: True if deleted, False if not found
        """
        async for session in get_db_session():
            try:
                project = await session.get(Project, project_id)
                if not project:
                    return False

                await session.delete(project)
                await session.commit()
                return True
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
