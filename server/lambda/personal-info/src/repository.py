"""
Personal Info Repository
Uses SQLModel from shared layer
"""

from typing import Optional, Dict, Any
import logging

# Import from the shared layer
try:
    from database import get_session, SessionDep
    from repositories import personal_info_repo, PersonalInfoRepository
    from models import PersonalInfo, PersonalInfoCreate, PersonalInfoUpdate
except ImportError:
    # Fallback if layer not available - implement basic repository
    import asyncio
    from models import PersonalInfo, PersonalInfoCreate, PersonalInfoUpdate

    class PersonalInfoRepository:
        """Fallback repository implementation"""

        async def get_personal_info(self) -> Optional[PersonalInfo]:
            # Mock data for fallback
            return PersonalInfo(
                id=1,
                first_name="Pablo",
                last_name="Contreras",
                email="pablo@bypabloc.com",
                title="Full Stack Developer",
                bio="Experienced developer specializing in serverless architecture",
                location="Santiago, Chile"
            )

        async def create_or_update(self, data: PersonalInfoCreate) -> PersonalInfo:
            # Mock update for fallback
            return PersonalInfo(id=1, **data.dict())

logger = logging.getLogger(__name__)


class PersonalInfoRepositoryWrapper:
    """Wrapper for PersonalInfo repository with session management"""

    def __init__(self):
        try:
            self._repo = personal_info_repo
            self._has_layer = True
        except NameError:
            self._repo = PersonalInfoRepository()
            self._has_layer = False

    async def get_personal_info(self) -> Optional[PersonalInfo]:
        """Get personal information"""
        try:
            if self._has_layer:
                async with get_session() as session:
                    return await self._repo.get_personal_info(session)
            else:
                return await self._repo.get_personal_info()
        except Exception as e:
            logger.error(f"Error getting personal info: {str(e)}")
            raise

    async def update_personal_info(self, update_data: PersonalInfoUpdate) -> PersonalInfo:
        """Update personal information"""
        try:
            if self._has_layer:
                async with get_session() as session:
                    # Convert update to create model for create_or_update
                    create_data = PersonalInfoCreate(**update_data.dict(exclude_unset=True))
                    return await self._repo.create_or_update(session, create_data)
            else:
                # Fallback implementation
                create_data = PersonalInfoCreate(**update_data.dict(exclude_unset=True))
                return await self._repo.create_or_update(create_data)
        except Exception as e:
            logger.error(f"Error updating personal info: {str(e)}")
            raise

    async def get_contact_info(self) -> Dict[str, Any]:
        """Get contact information only"""
        try:
            personal_info = await self.get_personal_info()
            if not personal_info:
                return {}

            return {
                "email": personal_info.email,
                "phone": personal_info.phone,
                "website_url": personal_info.website_url,
                "linkedin_url": personal_info.linkedin_url,
                "github_url": personal_info.github_url
            }
        except Exception as e:
            logger.error(f"Error getting contact info: {str(e)}")
            raise