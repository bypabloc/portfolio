"""
Work Repository - Database access layer for Work operations.

Lambda functions should ONLY import this repository, not models or database.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/01/19
"""

from typing import List, Optional, Dict, Any

# Repository imports from shared (models and database)
from shared.models import Work, WorkBase
from shared.database import get_db_session


class WorkRepository:
    """
    Repository for Work entity operations.

    Encapsulates all database access logic for Works.
    Lambda functions use ONLY this repository.
    """

    @classmethod
    async def get_all(
        cls,
        user_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Work]:
        """
        Get all works with optional user filter.

        Includes eager loaded relationships (employer, job_type).

        Args:
            user_id: Optional user filter
            skip: Offset for pagination
            limit: Limit for pagination

        Returns:
            List[Work]: Works with relationships
        """
        async for session in get_db_session():
            try:
                works = await Work.get_all(
                    session,
                    user_id=user_id,
                    skip=skip,
                    limit=limit
                )
                return works
            finally:
                await session.close()

    @classmethod
    async def get_by_id(cls, work_id: str) -> Optional[Work]:
        """
        Get work by ID with eager loaded relationships.

        Args:
            work_id: Work UUID

        Returns:
            Work | None: Work with relationships or None
        """
        async for session in get_db_session():
            try:
                work = await Work.get_by_id(session, work_id)
                return work
            finally:
                await session.close()

    @classmethod
    async def create(cls, work_data: Dict[str, Any]) -> Work:
        """
        Create new work.

        Args:
            work_data: Work data

        Returns:
            Work: Created work
        """
        async for session in get_db_session():
            try:
                db_work = Work(**work_data)
                session.add(db_work)
                await session.commit()
                await session.refresh(db_work)
                return db_work
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    @classmethod
    async def update(cls, work_id: str, work_data: Dict[str, Any]) -> Optional[Work]:
        """
        Update work.

        Args:
            work_id: Work UUID
            work_data: Data to update

        Returns:
            Work | None: Updated work or None if not found
        """
        from datetime import datetime

        async for session in get_db_session():
            try:
                work = await session.get(Work, work_id)
                if not work:
                    return None

                for field, value in work_data.items():
                    setattr(work, field, value)

                work.updated_at = datetime.utcnow()
                await session.commit()
                await session.refresh(work)
                return work
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    @classmethod
    async def delete(cls, work_id: str) -> bool:
        """
        Delete work.

        Args:
            work_id: Work UUID

        Returns:
            bool: True if deleted, False if not found
        """
        async for session in get_db_session():
            try:
                work = await session.get(Work, work_id)
                if not work:
                    return False

                await session.delete(work)
                await session.commit()
                return True
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
