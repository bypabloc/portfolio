"""
Base repository classes for the Repository Pattern implementation.

Provides abstract base classes and common functionality for data access layers
across all Lambda functions.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/20
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Dict, Any, Type, Union
from sqlmodel import SQLModel, select, and_, or_, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import func, text
from ..models import PaginationParams, PaginatedResponse
from ..exceptions import (
    RepositoryError,
    RecordNotFoundError,
    DuplicateRecordError,
    ValidationError
)

# Type variables for generic repository
ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType], ABC):
    """
    Abstract base repository class implementing common CRUD operations.

    This class provides a consistent interface for data access operations
    across all Lambda functions, following the Repository pattern.
    """

    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        """
        Initialize repository with database session and model.

        Args:
            session: Database session
            model: SQLModel class for this repository
        """
        self.session = session
        self.model = model

    async def get_by_id(self, id: int) -> Optional[ModelType]:
        """
        Get a record by its ID.

        Args:
            id: Record ID

        Returns:
            Model instance or None if not found

        Raises:
            RepositoryError: If database operation fails
        """
        try:
            statement = select(self.model).where(self.model.id == id)
            result = await self.session.exec(statement)
            return result.first()
        except Exception as e:
            raise RepositoryError(f"Failed to get {self.model.__name__} by id {id}: {str(e)}")

    async def get_by_id_or_raise(self, id: int) -> ModelType:
        """
        Get a record by ID or raise exception if not found.

        Args:
            id: Record ID

        Returns:
            Model instance

        Raises:
            RecordNotFoundError: If record not found
            RepositoryError: If database operation fails
        """
        record = await self.get_by_id(id)
        if not record:
            raise RecordNotFoundError(f"{self.model.__name__} with id {id} not found")
        return record

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        order_by: Optional[str] = None,
        order_direction: str = "asc"
    ) -> List[ModelType]:
        """
        Get all records with optional pagination and ordering.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            order_by: Field to order by
            order_direction: Order direction ("asc" or "desc")

        Returns:
            List of model instances

        Raises:
            RepositoryError: If database operation fails
        """
        try:
            statement = select(self.model)

            # Apply ordering
            if order_by and hasattr(self.model, order_by):
                order_field = getattr(self.model, order_by)
                if order_direction.lower() == "desc":
                    statement = statement.order_by(desc(order_field))
                else:
                    statement = statement.order_by(asc(order_field))

            # Apply pagination
            statement = statement.offset(skip).limit(limit)

            result = await self.session.exec(statement)
            return result.all()
        except Exception as e:
            raise RepositoryError(f"Failed to get all {self.model.__name__}: {str(e)}")

    async def get_paginated(
        self,
        pagination: PaginationParams,
        filters: Optional[Dict[str, Any]] = None
    ) -> PaginatedResponse:
        """
        Get paginated results with optional filters.

        Args:
            pagination: Pagination parameters
            filters: Optional filters to apply

        Returns:
            Paginated response with items and metadata

        Raises:
            RepositoryError: If database operation fails
        """
        try:
            # Build base query
            statement = select(self.model)

            # Apply filters
            if filters:
                statement = self._apply_filters(statement, filters)

            # Count total items
            count_statement = select(func.count()).select_from(statement.subquery())
            count_result = await self.session.exec(count_statement)
            total = count_result.one()

            # Apply ordering
            if pagination.order_by and hasattr(self.model, pagination.order_by):
                order_field = getattr(self.model, pagination.order_by)
                if pagination.order_direction.lower() == "desc":
                    statement = statement.order_by(desc(order_field))
                else:
                    statement = statement.order_by(asc(order_field))

            # Apply pagination
            statement = statement.offset(pagination.offset).limit(pagination.limit)

            # Execute query
            result = await self.session.exec(statement)
            items = result.all()

            return PaginatedResponse(
                items=items,
                total=total,
                limit=pagination.limit,
                offset=pagination.offset,
                has_next=pagination.offset + pagination.limit < total,
                has_previous=pagination.offset > 0
            )
        except Exception as e:
            raise RepositoryError(f"Failed to get paginated {self.model.__name__}: {str(e)}")

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record.

        Args:
            obj_in: Data for creating the record

        Returns:
            Created model instance

        Raises:
            DuplicateRecordError: If record violates unique constraints
            ValidationError: If data validation fails
            RepositoryError: If database operation fails
        """
        try:
            # Convert to model instance
            if isinstance(obj_in, dict):
                db_obj = self.model(**obj_in)
            else:
                db_obj = self.model.model_validate(obj_in)

            # Set timestamp if available
            if hasattr(db_obj, 'update_timestamp'):
                db_obj.update_timestamp()

            self.session.add(db_obj)
            await self.session.commit()
            await self.session.refresh(db_obj)
            return db_obj

        except IntegrityError as e:
            await self.session.rollback()
            raise DuplicateRecordError(f"Duplicate {self.model.__name__}: {str(e)}")
        except Exception as e:
            await self.session.rollback()
            raise RepositoryError(f"Failed to create {self.model.__name__}: {str(e)}")

    async def update(self, id: int, obj_in: UpdateSchemaType) -> Optional[ModelType]:
        """
        Update an existing record.

        Args:
            id: Record ID
            obj_in: Data for updating the record

        Returns:
            Updated model instance or None if not found

        Raises:
            DuplicateRecordError: If update violates unique constraints
            ValidationError: If data validation fails
            RepositoryError: If database operation fails
        """
        try:
            db_obj = await self.get_by_id(id)
            if not db_obj:
                return None

            # Update fields
            update_data = obj_in.model_dump(exclude_unset=True) if hasattr(obj_in, 'model_dump') else obj_in
            for field, value in update_data.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)

            # Update timestamp if available
            if hasattr(db_obj, 'update_timestamp'):
                db_obj.update_timestamp()

            self.session.add(db_obj)
            await self.session.commit()
            await self.session.refresh(db_obj)
            return db_obj

        except IntegrityError as e:
            await self.session.rollback()
            raise DuplicateRecordError(f"Duplicate {self.model.__name__}: {str(e)}")
        except Exception as e:
            await self.session.rollback()
            raise RepositoryError(f"Failed to update {self.model.__name__}: {str(e)}")

    async def delete(self, id: int) -> bool:
        """
        Delete a record by ID.

        Args:
            id: Record ID

        Returns:
            True if deleted, False if not found

        Raises:
            RepositoryError: If database operation fails
        """
        try:
            db_obj = await self.get_by_id(id)
            if not db_obj:
                return False

            await self.session.delete(db_obj)
            await self.session.commit()
            return True

        except Exception as e:
            await self.session.rollback()
            raise RepositoryError(f"Failed to delete {self.model.__name__}: {str(e)}")

    async def soft_delete(self, id: int) -> Optional[ModelType]:
        """
        Soft delete a record (if model supports it).

        Args:
            id: Record ID

        Returns:
            Updated model instance or None if not found

        Raises:
            RepositoryError: If database operation fails
        """
        try:
            db_obj = await self.get_by_id(id)
            if not db_obj:
                return None

            if hasattr(db_obj, 'soft_delete'):
                db_obj.soft_delete()
                self.session.add(db_obj)
                await self.session.commit()
                await self.session.refresh(db_obj)
                return db_obj
            else:
                raise RepositoryError(f"{self.model.__name__} does not support soft delete")

        except Exception as e:
            await self.session.rollback()
            raise RepositoryError(f"Failed to soft delete {self.model.__name__}: {str(e)}")

    async def exists(self, id: int) -> bool:
        """
        Check if a record exists by ID.

        Args:
            id: Record ID

        Returns:
            True if exists, False otherwise

        Raises:
            RepositoryError: If database operation fails
        """
        try:
            statement = select(func.count()).where(self.model.id == id)
            result = await self.session.exec(statement)
            count = result.one()
            return count > 0
        except Exception as e:
            raise RepositoryError(f"Failed to check existence of {self.model.__name__}: {str(e)}")

    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Count records with optional filters.

        Args:
            filters: Optional filters to apply

        Returns:
            Number of records matching criteria

        Raises:
            RepositoryError: If database operation fails
        """
        try:
            statement = select(func.count()).select_from(self.model)

            if filters:
                statement = self._apply_filters(statement, filters)

            result = await self.session.exec(statement)
            return result.one()
        except Exception as e:
            raise RepositoryError(f"Failed to count {self.model.__name__}: {str(e)}")

    def _apply_filters(self, statement, filters: Dict[str, Any]):
        """
        Apply filters to a SQL statement.

        Args:
            statement: SQLAlchemy statement
            filters: Dictionary of field names and values

        Returns:
            Modified statement with filters applied
        """
        conditions = []

        for field_name, value in filters.items():
            if not hasattr(self.model, field_name):
                continue

            field = getattr(self.model, field_name)

            if value is None:
                conditions.append(field.is_(None))
            elif isinstance(value, list):
                conditions.append(field.in_(value))
            elif isinstance(value, dict):
                # Support for range queries
                if 'gte' in value:
                    conditions.append(field >= value['gte'])
                if 'lte' in value:
                    conditions.append(field <= value['lte'])
                if 'gt' in value:
                    conditions.append(field > value['gt'])
                if 'lt' in value:
                    conditions.append(field < value['lt'])
                if 'like' in value:
                    conditions.append(field.like(f"%{value['like']}%"))
                if 'ilike' in value:
                    conditions.append(field.ilike(f"%{value['ilike']}%"))
            else:
                conditions.append(field == value)

        if conditions:
            statement = statement.where(and_(*conditions))

        return statement

    # Abstract methods for specific implementations
    @abstractmethod
    async def get_by_field(self, field: str, value: Any) -> Optional[ModelType]:
        """Get record by specific field value."""
        pass

    @abstractmethod
    async def search(self, query: str, fields: List[str]) -> List[ModelType]:
        """Search records by text query in specified fields."""
        pass