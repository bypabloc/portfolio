"""
Personal Info Service
Business logic layer for personal information management
"""

from typing import Optional, Dict, Any
import logging

from models import PersonalInfo, PersonalInfoUpdate, PersonalInfoResponse, ContactInfoResponse
from repository import PersonalInfoRepositoryWrapper

logger = logging.getLogger(__name__)


class PersonalInfoService:
    """Business logic service for personal information"""

    def __init__(self, repository: Optional[PersonalInfoRepositoryWrapper] = None):
        self.repository = repository or PersonalInfoRepositoryWrapper()

    async def get_personal_info(self) -> Optional[PersonalInfoResponse]:
        """
        Get personal information with business logic

        Returns:
            PersonalInfoResponse or None if not found
        """
        try:
            personal_info = await self.repository.get_personal_info()
            if not personal_info:
                logger.warning("Personal information not found")
                return None

            return PersonalInfoResponse(
                id=personal_info.id,
                first_name=personal_info.first_name,
                last_name=personal_info.last_name,
                email=personal_info.email,
                phone=personal_info.phone,
                location=personal_info.location,
                title=personal_info.title,
                bio=personal_info.bio,
                website_url=personal_info.website_url,
                linkedin_url=personal_info.linkedin_url,
                github_url=personal_info.github_url
            )

        except Exception as e:
            logger.error(f"Service error getting personal info: {str(e)}")
            raise

    async def update_personal_info(self, update_data: PersonalInfoUpdate) -> PersonalInfoResponse:
        """
        Update personal information with validation

        Args:
            update_data: Data to update

        Returns:
            Updated personal information
        """
        try:
            # Validate required fields if this is a first-time creation
            existing = await self.repository.get_personal_info()

            if not existing:
                # First time creation - validate required fields
                required_fields = ['first_name', 'last_name', 'email', 'title', 'bio']
                for field in required_fields:
                    if not getattr(update_data, field, None):
                        raise ValueError(f"Required field '{field}' is missing")

            # Update personal information
            updated_info = await self.repository.update_personal_info(update_data)

            return PersonalInfoResponse(
                id=updated_info.id,
                first_name=updated_info.first_name,
                last_name=updated_info.last_name,
                email=updated_info.email,
                phone=updated_info.phone,
                location=updated_info.location,
                title=updated_info.title,
                bio=updated_info.bio,
                website_url=updated_info.website_url,
                linkedin_url=updated_info.linkedin_url,
                github_url=updated_info.github_url
            )

        except Exception as e:
            logger.error(f"Service error updating personal info: {str(e)}")
            raise

    async def get_contact_info(self) -> ContactInfoResponse:
        """
        Get contact information only

        Returns:
            Contact information
        """
        try:
            contact_data = await self.repository.get_contact_info()

            return ContactInfoResponse(
                email=contact_data.get("email", ""),
                phone=contact_data.get("phone"),
                website_url=contact_data.get("website_url"),
                linkedin_url=contact_data.get("linkedin_url"),
                github_url=contact_data.get("github_url")
            )

        except Exception as e:
            logger.error(f"Service error getting contact info: {str(e)}")
            raise

    async def health_check(self) -> Dict[str, Any]:
        """
        Health check for the service

        Returns:
            Health status information
        """
        try:
            # Try to connect to database through repository
            personal_info = await self.repository.get_personal_info()

            return {
                "status": "healthy",
                "database_connected": True,
                "has_personal_info": personal_info is not None,
                "service": "personal-info"
            }

        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "database_connected": False,
                "error": str(e),
                "service": "personal-info"
            }