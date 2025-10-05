"""
User management routes with EAV pattern support.

Implements CRUD operations for users and user_attributes using Repository Pattern.
Lambda functions use ONLY repositories, not models or database directly.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/01/19
"""

from fastapi import APIRouter, HTTPException, status
from shared.logger import logger
from typing import List, Dict, Any
from pydantic import BaseModel

from shared.repositories import UserRepository
from shared.models import attributes_to_dict

router = APIRouter()


# ============================================================================
# Schemas for API Requests/Responses
# ============================================================================


class UserCreateRequest(BaseModel):
    """Request schema for creating a user with attributes."""

    username: str
    attributes: Dict[str, Any]  # EAV attributes as dict


class UserUpdateRequest(BaseModel):
    """Request schema for updating user attributes."""

    attributes: Dict[str, Any]  # EAV attributes to update


class UserPublicResponse(BaseModel):
    """Public response schema for user data."""

    id: str
    username: str
    status: str
    created_at: str
    attributes: Dict[str, Any]  # Parsed EAV attributes


# ============================================================================
# User CRUD Endpoints (Repository-Based)
# ============================================================================


@router.get('/users', response_model=List[UserPublicResponse])
async def get_users(skip: int = 0, limit: int = 100):
    """
    Get list of users with their attributes.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of users with parsed attributes
    """
    try:
        # Use repository method (database-agnostic)
        users = await UserRepository.get_all(skip=skip, limit=limit)

        logger.info(f'Found {len(users)} users')

        # Convert users to public response format
        return [
            UserPublicResponse(
                id=user.id,
                username=user.username,
                status=user.status,
                created_at=user.created_at.isoformat(),
                attributes=attributes_to_dict(user.attributes),
            )
            for user in users
        ]

    except Exception as e:
        logger.error(f'Error getting users: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error retrieving users',
        )


@router.get('/users/{user_id}', response_model=UserPublicResponse)
async def get_user(user_id: str):
    """
    Get specific user by ID with attributes.

    Args:
        user_id: User ID

    Returns:
        User with parsed attributes
    """
    try:
        # Use repository method (database-agnostic)
        user = await UserRepository.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'User with ID {user_id} not found',
            )

        return UserPublicResponse(
            id=user.id,
            username=user.username,
            status=user.status,
            created_at=user.created_at.isoformat(),
            attributes=attributes_to_dict(user.attributes),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Error getting user: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error retrieving user',
        )


@router.get('/users/username/{username}', response_model=UserPublicResponse)
async def get_user_by_username(username: str):
    """
    Get user by username with attributes.

    Args:
        username: Username to search

    Returns:
        User with parsed attributes
    """
    try:
        # Use repository method (database-agnostic)
        user = await UserRepository.get_by_username(username)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with username '{username}' not found",
            )

        return UserPublicResponse(
            id=user.id,
            username=user.username,
            status=user.status,
            created_at=user.created_at.isoformat(),
            attributes=attributes_to_dict(user.attributes),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Error getting user by username: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error retrieving user',
        )


@router.post(
    '/users', response_model=UserPublicResponse, status_code=status.HTTP_201_CREATED
)
async def create_user(user_data: UserCreateRequest):
    """
    Create new user with attributes using EAV pattern.

    Args:
        user_data: User creation data with attributes

    Returns:
        Created user with attributes
    """
    try:
        # Use repository method (database-agnostic)
        user = await UserRepository.create(
            user_data={'username': user_data.username}, attributes=user_data.attributes
        )

        return UserPublicResponse(
            id=user.id,
            username=user.username,
            status=user.status,
            created_at=user.created_at.isoformat(),
            attributes=attributes_to_dict(user.attributes),
        )

    except Exception as e:
        logger.error(f'Error creating user: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error creating user',
        )


@router.patch("/users/{user_id}/attributes", response_model=UserPublicResponse)
async def update_user_attributes(user_id: str, update_data: UserUpdateRequest):
    """
    Update user attributes using EAV pattern.

    Args:
        user_id: User ID
        update_data: Attributes to update

    Returns:
        Updated user with attributes
    """
    try:
        # Use repository method (database-agnostic)
        user = await UserRepository.update(
            user_id=user_id, attributes=update_data.attributes
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )

        return UserPublicResponse(
            id=user.id,
            username=user.username,
            status=user.status,
            created_at=user.created_at.isoformat(),
            attributes=attributes_to_dict(user.attributes),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Error updating user attributes: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error updating user attributes',
        )


@router.delete('/users/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    """
    Delete user (soft delete - sets status to inactive).

    Args:
        user_id: User ID

    Returns:
        No content
    """
    try:
        # Use repository method (database-agnostic)
        deleted = await UserRepository.delete(user_id)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'User with ID {user_id} not found',
            )

        return None

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Error deleting user: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error deleting user',
        )
