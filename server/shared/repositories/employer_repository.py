"""
Employer Repository - Database access layer for Employer operations.

Lambda functions should ONLY import this repository, not models or database.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/01/19
"""

from typing import List, Optional, Dict, Any

# Repository imports from shared (models and database)
from shared.models import Employer, EmployerBase
from shared.database import get_db_session


class EmployerRepository:
    """
    Repository for Employer entity operations.

    Encapsulates all database access logic for Employers.
    Lambda functions use ONLY this repository.
    """

    @classmethod
    async def get_all(cls, skip: int = 0, limit: int = 100) -> List[Employer]:
        """
        Get all employers.

        Args:
            skip: Offset for pagination
            limit: Limit for pagination

        Returns:
            List[Employer]: Employers
        """
        async for session in get_db_session():
            try:
                employers = await Employer.get_all(session, skip=skip, limit=limit)
                return employers
            finally:
                await session.close()

    @classmethod
    async def get_by_id(cls, employer_id: str) -> Optional[Employer]:
        """
        Get employer by ID.

        Args:
            employer_id: Employer UUID

        Returns:
            Employer | None: Employer or None
        """
        async for session in get_db_session():
            try:
                employer = await Employer.get_by_id(session, employer_id)
                return employer
            finally:
                await session.close()

    @classmethod
    async def create(cls, employer_data: Dict[str, Any]) -> Employer:
        """
        Create new employer.

        Args:
            employer_data: Employer data

        Returns:
            Employer: Created employer
        """
        async for session in get_db_session():
            try:
                db_employer = Employer(**employer_data)
                session.add(db_employer)
                await session.commit()
                await session.refresh(db_employer)
                return db_employer
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
