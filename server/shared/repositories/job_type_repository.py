"""
JobType Repository - Database access layer for JobType operations.

Lambda functions should ONLY import this repository, not models or database.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/01/19
"""

from typing import List, Optional, Dict, Any

# Repository imports from shared (models and database)
from shared.models import JobType, JobTypeBase
from shared.database import get_db_session


class JobTypeRepository:
    """
    Repository for JobType entity operations.

    Encapsulates all database access logic for JobTypes.
    Lambda functions use ONLY this repository.
    """

    @classmethod
    async def get_all(cls, skip: int = 0, limit: int = 100) -> List[JobType]:
        """
        Get all job types.

        Args:
            skip: Offset for pagination
            limit: Limit for pagination

        Returns:
            List[JobType]: Job types
        """
        async for session in get_db_session():
            try:
                job_types = await JobType.get_all(session, skip=skip, limit=limit)
                return job_types
            finally:
                await session.close()

    @classmethod
    async def get_by_id(cls, job_type_id: str) -> Optional[JobType]:
        """
        Get job type by ID.

        Args:
            job_type_id: JobType UUID

        Returns:
            JobType | None: JobType or None
        """
        async for session in get_db_session():
            try:
                job_type = await JobType.get_by_id(session, job_type_id)
                return job_type
            finally:
                await session.close()

    @classmethod
    async def create(cls, job_type_data: Dict[str, Any]) -> JobType:
        """
        Create new job type.

        Args:
            job_type_data: JobType data

        Returns:
            JobType: Created job type
        """
        async for session in get_db_session():
            try:
                db_job_type = JobType(**job_type_data)
                session.add(db_job_type)
                await session.commit()
                await session.refresh(db_job_type)
                return db_job_type
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
