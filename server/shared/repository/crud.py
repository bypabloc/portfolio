"""
Generic CRUD operations for repository pattern.

Provides ready-to-use CRUD operations that can be composed into specific
repository implementations.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/20
"""

from typing import Generic, TypeVar, Optional, List, Dict, Any, Type, Union
from sqlmodel import SQLModel, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from .base import BaseRepository
from .mixins import (
    SearchMixin,
    StatusMixin,
    FeaturedMixin,
    OrderingMixin,
    CategoryMixin,
    DateRangeMixin
)
from ..exceptions import RepositoryError, RecordNotFoundError, DuplicateRecordError

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


class CRUDRepository(
    BaseRepository[ModelType, CreateSchemaType, UpdateSchemaType],
    SearchMixin,
    StatusMixin,
    FeaturedMixin,
    OrderingMixin,
    CategoryMixin,
    DateRangeMixin
):
    """
    Complete CRUD repository with all common functionality.

    This class combines the base repository with all available mixins to provide
    a comprehensive set of operations for most use cases.
    """

    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        """Initialize CRUD repository."""
        super().__init__(session, model)

    async def get_by_field(self, field: str, value: Any) -> Optional[ModelType]:
        """
        Get a record by any field value.

        Args:
            field: Field name to search by
            value: Value to search for

        Returns:
            Model instance or None if not found

        Raises:
            RepositoryError: If field doesn't exist or operation fails
        """
        try:
            if not hasattr(self.model, field):
                raise RepositoryError(f"{self.model.__name__} does not have field '{field}'")

            model_field = getattr(self.model, field)
            statement = select(self.model).where(model_field == value)
            result = await self.session.exec(statement)
            return result.first()

        except Exception as e:
            raise RepositoryError(f"Failed to get {self.model.__name__} by {field}: {str(e)}")

    async def get_all_by_field(self, field: str, value: Any) -> List[ModelType]:
        """
        Get all records matching a field value.

        Args:
            field: Field name to search by
            value: Value to search for

        Returns:
            List of matching model instances

        Raises:
            RepositoryError: If field doesn't exist or operation fails
        """
        try:
            if not hasattr(self.model, field):
                raise RepositoryError(f"{self.model.__name__} does not have field '{field}'")

            model_field = getattr(self.model, field)
            statement = select(self.model).where(model_field == value)
            result = await self.session.exec(statement)
            return result.all()

        except Exception as e:
            raise RepositoryError(f"Failed to get {self.model.__name__} by {field}: {str(e)}")

    async def upsert(
        self,
        obj_in: Union[CreateSchemaType, UpdateSchemaType],
        unique_field: str = 'id'
    ) -> ModelType:
        """
        Create or update a record based on a unique field.

        Args:
            obj_in: Data for creating or updating the record
            unique_field: Field to check for existing record

        Returns:
            Created or updated model instance

        Raises:
            RepositoryError: If operation fails
        """
        try:
            # Check if record exists
            unique_value = getattr(obj_in, unique_field, None) if hasattr(obj_in, unique_field) else None

            if unique_value is not None:
                existing_record = await self.get_by_field(unique_field, unique_value)
                if existing_record:
                    # Update existing record
                    return await self.update(existing_record.id, obj_in)

            # Create new record
            return await self.create(obj_in)

        except Exception as e:
            raise RepositoryError(f"Failed to upsert {self.model.__name__}: {str(e)}")

    async def bulk_create(self, objects: List[CreateSchemaType]) -> List[ModelType]:
        """
        Create multiple records in bulk.

        Args:
            objects: List of objects to create

        Returns:
            List of created model instances

        Raises:
            RepositoryError: If operation fails
        """
        try:
            db_objects = []
            for obj_in in objects:
                if isinstance(obj_in, dict):
                    db_obj = self.model(**obj_in)
                else:
                    db_obj = self.model.model_validate(obj_in)

                if hasattr(db_obj, 'update_timestamp'):
                    db_obj.update_timestamp()

                db_objects.append(db_obj)

            self.session.add_all(db_objects)
            await self.session.commit()

            # Refresh all objects
            for db_obj in db_objects:
                await self.session.refresh(db_obj)

            return db_objects

        except IntegrityError as e:
            await self.session.rollback()
            raise DuplicateRecordError(f"Bulk create failed for {self.model.__name__}: {str(e)}")
        except Exception as e:
            await self.session.rollback()
            raise RepositoryError(f"Failed to bulk create {self.model.__name__}: {str(e)}")

    async def bulk_update(
        self,
        updates: List[Dict[str, Any]],
        id_field: str = 'id'
    ) -> List[ModelType]:
        """
        Update multiple records in bulk.

        Args:
            updates: List of dicts containing id and update data
            id_field: Field name for identifying records

        Returns:
            List of updated model instances

        Raises:
            RepositoryError: If operation fails
        """
        try:
            updated_objects = []

            for update_data in updates:
                record_id = update_data.get(id_field)
                if not record_id:
                    continue

                db_obj = await self.get_by_id(record_id)
                if not db_obj:
                    continue

                # Update fields
                for field, value in update_data.items():
                    if field != id_field and hasattr(db_obj, field):
                        setattr(db_obj, field, value)

                if hasattr(db_obj, 'update_timestamp'):
                    db_obj.update_timestamp()

                updated_objects.append(db_obj)

            await self.session.commit()

            # Refresh all objects
            for db_obj in updated_objects:
                await self.session.refresh(db_obj)

            return updated_objects

        except Exception as e:
            await self.session.rollback()
            raise RepositoryError(f"Failed to bulk update {self.model.__name__}: {str(e)}")

    async def bulk_delete(self, ids: List[int]) -> int:
        """
        Delete multiple records by IDs.

        Args:
            ids: List of record IDs to delete

        Returns:
            Number of records deleted

        Raises:
            RepositoryError: If operation fails
        """
        try:
            statement = select(self.model).where(self.model.id.in_(ids))
            result = await self.session.exec(statement)
            records_to_delete = result.all()

            deleted_count = len(records_to_delete)

            for record in records_to_delete:
                await self.session.delete(record)

            await self.session.commit()
            return deleted_count

        except Exception as e:
            await self.session.rollback()
            raise RepositoryError(f"Failed to bulk delete {self.model.__name__}: {str(e)}")

    async def duplicate(self, id: int, exclude_fields: Optional[List[str]] = None) -> ModelType:
        """
        Duplicate a record by ID.

        Args:
            id: ID of record to duplicate
            exclude_fields: Fields to exclude from duplication

        Returns:
            Duplicated model instance

        Raises:
            RecordNotFoundError: If original record not found
            RepositoryError: If operation fails
        """
        try:
            original = await self.get_by_id_or_raise(id)

            # Get all field values except excluded ones
            exclude_fields = exclude_fields or ['id', 'created_at', 'updated_at']
            duplicate_data = {}

            for field_name in original.model_fields:
                if field_name not in exclude_fields:
                    value = getattr(original, field_name)
                    duplicate_data[field_name] = value

            # Create new record
            duplicate = self.model(**duplicate_data)

            if hasattr(duplicate, 'update_timestamp'):
                duplicate.update_timestamp()

            self.session.add(duplicate)
            await self.session.commit()
            await self.session.refresh(duplicate)

            return duplicate

        except RecordNotFoundError:
            raise
        except Exception as e:
            await self.session.rollback()
            raise RepositoryError(f"Failed to duplicate {self.model.__name__}: {str(e)}")

    async def get_random(self, limit: int = 1) -> List[ModelType]:
        """
        Get random records.

        Args:
            limit: Number of random records to return

        Returns:
            List of random model instances

        Raises:
            RepositoryError: If operation fails
        """
        try:
            from sqlalchemy import func
            statement = select(self.model).order_by(func.random()).limit(limit)
            result = await self.session.exec(statement)
            return result.all()

        except Exception as e:
            raise RepositoryError(f"Failed to get random {self.model.__name__}: {str(e)}")

    async def get_statistics(self) -> Dict[str, Any]:
        """
        Get basic statistics about the table.

        Returns:
            Dictionary with statistics

        Raises:
            RepositoryError: If operation fails
        """
        try:
            from sqlalchemy import func
            from datetime import datetime, timedelta, timezone

            stats = {}

            # Total count
            total_count = await self.count()
            stats['total_count'] = total_count

            # Active/Inactive counts if applicable
            if hasattr(self.model, 'is_active'):
                active_records = await self.get_active()
                stats['active_count'] = len(active_records)
                stats['inactive_count'] = total_count - stats['active_count']

            # Featured count if applicable
            if hasattr(self.model, 'is_featured'):
                featured_records = await self.get_featured()
                stats['featured_count'] = len(featured_records)

            # Recent activity (last 30 days) if applicable
            if hasattr(self.model, 'created_at'):
                thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
                recent_records = await self.get_by_date_range(
                    thirty_days_ago,
                    datetime.now(timezone.utc),
                    'created_at'
                )
                stats['recent_count'] = len(recent_records)

            # Categories if applicable
            if hasattr(self.model, 'category'):
                categories = await self.get_categories()
                stats['category_count'] = len(categories)
                stats['categories'] = categories

            return stats

        except Exception as e:
            raise RepositoryError(f"Failed to get statistics for {self.model.__name__}: {str(e)}")