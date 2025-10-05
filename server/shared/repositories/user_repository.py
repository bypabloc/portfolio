"""
User Repository - Database access layer for User operations.

Lambda functions should ONLY import this repository, not models or database.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/01/19
"""

from typing import List, Optional, Dict, Any
from uuid import UUID

# Repository imports from shared (models and database)
from shared.models import User, UserBase, UserAttribute, UserAttributeBase
from shared.database import get_db_session


class UserRepository:
    """
    Repository for User entity operations.

    Encapsulates all database access logic for Users.
    Lambda functions use ONLY this repository.
    """

    @classmethod
    async def get_all(cls, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get all users with their attributes.

        Args:
            skip: Offset for pagination
            limit: Limit for pagination

        Returns:
            List[User]: Users with eager loaded attributes
        """
        async for session in get_db_session():
            try:
                users = await User.get_all(session, skip=skip, limit=limit)
                return users
            finally:
                await session.close()

    @classmethod
    async def get_by_id(cls, user_id: str) -> Optional[User]:
        """
        Get user by ID with attributes.

        Args:
            user_id: User UUID

        Returns:
            User | None: User with attributes or None
        """
        async for session in get_db_session():
            try:
                user = await User.get_by_id(session, user_id)
                return user
            finally:
                await session.close()

    @classmethod
    async def get_by_username(cls, username: str) -> Optional[User]:
        """
        Get user by username with attributes.

        Args:
            username: Username to search

        Returns:
            User | None: User with attributes or None
        """
        async for session in get_db_session():
            try:
                user = await User.get_by_username(session, username)
                return user
            finally:
                await session.close()

    @classmethod
    async def create(cls, user_data: Dict[str, Any], attributes: Dict[str, str]) -> User:
        """
        Create new user with attributes.

        Args:
            user_data: User base data (username, status)
            attributes: User attributes as key-value dict

        Returns:
            User: Created user with attributes
        """
        from sqlalchemy import select

        async for session in get_db_session():
            try:
                # Create user base
                db_user = User(**user_data)
                session.add(db_user)
                await session.flush()

                # Create attributes
                for key, value in attributes.items():
                    attribute = UserAttribute(
                        user_id=db_user.id,
                        attribute_key=key,
                        attribute_value=value
                    )
                    session.add(attribute)

                await session.commit()
                await session.refresh(db_user)

                # Load attributes
                statement = select(User).where(User.id == db_user.id)
                from sqlalchemy.orm import selectinload
                statement = statement.options(selectinload(User.attributes))
                result = await session.execute(statement)
                user_with_attrs = result.scalars().first()

                return user_with_attrs
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    @classmethod
    async def update(
        cls,
        user_id: str,
        user_data: Optional[Dict[str, Any]] = None,
        attributes: Optional[Dict[str, str]] = None
    ) -> Optional[User]:
        """
        Update user and/or attributes.

        Args:
            user_id: User UUID
            user_data: User base data to update
            attributes: Attributes to update (replaces existing)

        Returns:
            User | None: Updated user or None if not found
        """
        from sqlalchemy import select, delete
        from sqlalchemy.orm import selectinload
        from datetime import datetime

        async for session in get_db_session():
            try:
                user = await session.get(User, user_id)
                if not user:
                    return None

                # Update user base data
                if user_data:
                    for field, value in user_data.items():
                        setattr(user, field, value)
                    user.updated_at = datetime.utcnow()

                # Update attributes if provided
                if attributes is not None:
                    # Delete old attributes
                    await session.execute(
                        delete(UserAttribute).where(UserAttribute.user_id == user_id)
                    )

                    # Create new attributes
                    for key, value in attributes.items():
                        attribute = UserAttribute(
                            user_id=user_id,
                            attribute_key=key,
                            attribute_value=value
                        )
                        session.add(attribute)

                await session.commit()

                # Reload with attributes
                statement = (
                    select(User)
                    .where(User.id == user_id)
                    .options(selectinload(User.attributes))
                )
                result = await session.execute(statement)
                updated_user = result.scalars().first()

                return updated_user
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    @classmethod
    async def delete(cls, user_id: str) -> bool:
        """
        Delete user and all attributes.

        Args:
            user_id: User UUID

        Returns:
            bool: True if deleted, False if not found
        """
        async for session in get_db_session():
            try:
                user = await session.get(User, user_id)
                if not user:
                    return False

                await session.delete(user)
                await session.commit()
                return True
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
