"""
Personal Info Service Models
Using SQLModel from shared layer
"""

from typing import Optional
from sqlmodel import SQLModel


# Import SQLModel models from the layer
try:
    from models import (
        PersonalInfo,
        PersonalInfoBase,
        PersonalInfoCreate,
        PersonalInfoUpdate
    )
except ImportError:
    # Fallback Pydantic models if layer not available
    class PersonalInfoBase(SQLModel):
        first_name: str
        last_name: str
        email: str
        phone: Optional[str] = None
        location: Optional[str] = None
        title: str
        bio: str
        website_url: Optional[str] = None
        linkedin_url: Optional[str] = None
        github_url: Optional[str] = None

    class PersonalInfo(PersonalInfoBase):
        id: Optional[int] = None

    class PersonalInfoCreate(PersonalInfoBase):
        pass

    class PersonalInfoUpdate(SQLModel):
        first_name: Optional[str] = None
        last_name: Optional[str] = None
        email: Optional[str] = None
        phone: Optional[str] = None
        location: Optional[str] = None
        title: Optional[str] = None
        bio: Optional[str] = None
        website_url: Optional[str] = None
        linkedin_url: Optional[str] = None
        github_url: Optional[str] = None


# Response models for API
class PersonalInfoResponse(PersonalInfoBase):
    """Response model for personal info API"""
    id: int

    @property
    def full_name(self) -> str:
        """Get full name."""
        return f"{self.first_name} {self.last_name}"


class ContactInfoResponse(SQLModel):
    """Response model for contact info only"""
    email: str
    phone: Optional[str] = None
    website_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None