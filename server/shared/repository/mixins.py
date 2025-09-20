"""
Repository mixins for common functionality.

Provides reusable repository functionality that can be mixed into specific
repository implementations.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/20
"""

from typing import List, Optional, Any, Dict
from sqlmodel import select, or_, and_, desc, asc
from sqlalchemy import func, text
from ..exceptions import RepositoryError


class SearchMixin:
    """
    Mixin for full-text search functionality.
    """

    async def search(
        self,
        query: str,
        fields: List[str],
        limit: int = 50,
        fuzzy: bool = False
    ) -> List[Any]:
        """
        Search records by text query in specified fields.

        Args:
            query: Search query
            fields: List of field names to search in
            limit: Maximum number of results
            fuzzy: Whether to use fuzzy matching

        Returns:
            List of matching records

        Raises:
            RepositoryError: If search operation fails
        """
        try:
            # Validate fields exist on model
            valid_fields = [field for field in fields if hasattr(self.model, field)]
            if not valid_fields:
                return []

            # Build search conditions
            search_conditions = []
            for field_name in valid_fields:
                field = getattr(self.model, field_name)
                if fuzzy:
                    # Use ILIKE for case-insensitive fuzzy search
                    search_conditions.append(field.ilike(f"%{query}%"))
                else:
                    # Use exact word matching
                    search_conditions.append(field.ilike(f"%{query}%"))

            # Create statement with OR conditions
            statement = select(self.model).where(or_(*search_conditions)).limit(limit)

            result = await self.session.exec(statement)
            return result.all()

        except Exception as e:
            raise RepositoryError(f"Search failed for {self.model.__name__}: {str(e)}")

    async def search_by_tags(self, tags: List[str]) -> List[Any]:
        """
        Search records by tags.

        Args:
            tags: List of tags to search for

        Returns:
            List of matching records

        Raises:
            RepositoryError: If search operation fails
        """
        try:
            if not tags or not hasattr(self.model, 'tags'):
                return []

            # Build tag search conditions
            tag_conditions = []
            for tag in tags:
                tag_field = getattr(self.model, 'tags')
                tag_conditions.append(tag_field.like(f"%{tag.lower()}%"))

            statement = select(self.model).where(or_(*tag_conditions))
            result = await self.session.exec(statement)
            return result.all()

        except Exception as e:
            raise RepositoryError(f"Tag search failed for {self.model.__name__}: {str(e)}")


class StatusMixin:
    """
    Mixin for status-based queries.
    """

    async def get_active(self, limit: Optional[int] = None) -> List[Any]:
        """
        Get all active records.

        Args:
            limit: Maximum number of records to return

        Returns:
            List of active records

        Raises:
            RepositoryError: If operation fails
        """
        try:
            if not hasattr(self.model, 'is_active'):
                raise RepositoryError(f"{self.model.__name__} does not have is_active field")

            statement = select(self.model).where(self.model.is_active == True)
            if limit:
                statement = statement.limit(limit)

            result = await self.session.exec(statement)
            return result.all()

        except Exception as e:
            raise RepositoryError(f"Failed to get active {self.model.__name__}: {str(e)}")

    async def get_inactive(self, limit: Optional[int] = None) -> List[Any]:
        """
        Get all inactive records.

        Args:
            limit: Maximum number of records to return

        Returns:
            List of inactive records

        Raises:
            RepositoryError: If operation fails
        """
        try:
            if not hasattr(self.model, 'is_active'):
                raise RepositoryError(f"{self.model.__name__} does not have is_active field")

            statement = select(self.model).where(self.model.is_active == False)
            if limit:
                statement = statement.limit(limit)

            result = await self.session.exec(statement)
            return result.all()

        except Exception as e:
            raise RepositoryError(f"Failed to get inactive {self.model.__name__}: {str(e)}")

    async def activate_bulk(self, ids: List[int]) -> int:
        """
        Activate multiple records by IDs.

        Args:
            ids: List of record IDs to activate

        Returns:
            Number of records activated

        Raises:
            RepositoryError: If operation fails
        """
        try:
            if not hasattr(self.model, 'is_active'):
                raise RepositoryError(f"{self.model.__name__} does not have is_active field")

            statement = select(self.model).where(self.model.id.in_(ids))
            result = await self.session.exec(statement)
            records = result.all()

            activated_count = 0
            for record in records:
                if not record.is_active:
                    record.is_active = True
                    if hasattr(record, 'update_timestamp'):
                        record.update_timestamp()
                    activated_count += 1

            await self.session.commit()
            return activated_count

        except Exception as e:
            await self.session.rollback()
            raise RepositoryError(f"Failed to activate {self.model.__name__} records: {str(e)}")


class FeaturedMixin:
    """
    Mixin for featured content queries.
    """

    async def get_featured(
        self,
        limit: Optional[int] = None,
        active_only: bool = True
    ) -> List[Any]:
        """
        Get featured records.

        Args:
            limit: Maximum number of records to return
            active_only: Whether to only return active records

        Returns:
            List of featured records

        Raises:
            RepositoryError: If operation fails
        """
        try:
            if not hasattr(self.model, 'is_featured'):
                raise RepositoryError(f"{self.model.__name__} does not have is_featured field")

            conditions = [self.model.is_featured == True]

            if active_only and hasattr(self.model, 'is_active'):
                conditions.append(self.model.is_active == True)

            statement = select(self.model).where(and_(*conditions))

            # Order by order_index if available
            if hasattr(self.model, 'order_index'):
                statement = statement.order_by(asc(self.model.order_index))

            if limit:
                statement = statement.limit(limit)

            result = await self.session.exec(statement)
            return result.all()

        except Exception as e:
            raise RepositoryError(f"Failed to get featured {self.model.__name__}: {str(e)}")

    async def set_featured_bulk(self, ids: List[int], featured: bool = True) -> int:
        """
        Set featured status for multiple records.

        Args:
            ids: List of record IDs
            featured: Whether to feature or unfeature

        Returns:
            Number of records updated

        Raises:
            RepositoryError: If operation fails
        """
        try:
            if not hasattr(self.model, 'is_featured'):
                raise RepositoryError(f"{self.model.__name__} does not have is_featured field")

            statement = select(self.model).where(self.model.id.in_(ids))
            result = await self.session.exec(statement)
            records = result.all()

            updated_count = 0
            for record in records:
                if record.is_featured != featured:
                    record.is_featured = featured
                    if hasattr(record, 'update_timestamp'):
                        record.update_timestamp()
                    updated_count += 1

            await self.session.commit()
            return updated_count

        except Exception as e:
            await self.session.rollback()
            raise RepositoryError(f"Failed to update featured status for {self.model.__name__}: {str(e)}")


class OrderingMixin:
    """
    Mixin for ordering and sorting functionality.
    """

    async def get_ordered(
        self,
        ascending: bool = True,
        limit: Optional[int] = None
    ) -> List[Any]:
        """
        Get records ordered by order_index.

        Args:
            ascending: Whether to sort in ascending order
            limit: Maximum number of records to return

        Returns:
            List of ordered records

        Raises:
            RepositoryError: If operation fails
        """
        try:
            if not hasattr(self.model, 'order_index'):
                raise RepositoryError(f"{self.model.__name__} does not have order_index field")

            order_field = self.model.order_index
            statement = select(self.model).order_by(asc(order_field) if ascending else desc(order_field))

            if limit:
                statement = statement.limit(limit)

            result = await self.session.exec(statement)
            return result.all()

        except Exception as e:
            raise RepositoryError(f"Failed to get ordered {self.model.__name__}: {str(e)}")

    async def reorder(self, id_order_pairs: List[Dict[str, int]]) -> int:
        """
        Reorder records by setting new order indices.

        Args:
            id_order_pairs: List of dicts with 'id' and 'order_index' keys

        Returns:
            Number of records reordered

        Raises:
            RepositoryError: If operation fails
        """
        try:
            if not hasattr(self.model, 'order_index'):
                raise RepositoryError(f"{self.model.__name__} does not have order_index field")

            reordered_count = 0
            for pair in id_order_pairs:
                record_id = pair.get('id')
                new_order = pair.get('order_index')

                if record_id is None or new_order is None:
                    continue

                record = await self.get_by_id(record_id)
                if record and record.order_index != new_order:
                    record.order_index = new_order
                    if hasattr(record, 'update_timestamp'):
                        record.update_timestamp()
                    reordered_count += 1

            await self.session.commit()
            return reordered_count

        except Exception as e:
            await self.session.rollback()
            raise RepositoryError(f"Failed to reorder {self.model.__name__}: {str(e)}")


class CategoryMixin:
    """
    Mixin for category-based queries.
    """

    async def get_by_category(
        self,
        category: str,
        limit: Optional[int] = None
    ) -> List[Any]:
        """
        Get records by category.

        Args:
            category: Category name
            limit: Maximum number of records to return

        Returns:
            List of records in the category

        Raises:
            RepositoryError: If operation fails
        """
        try:
            if not hasattr(self.model, 'category'):
                raise RepositoryError(f"{self.model.__name__} does not have category field")

            statement = select(self.model).where(self.model.category.ilike(category))

            if limit:
                statement = statement.limit(limit)

            result = await self.session.exec(statement)
            return result.all()

        except Exception as e:
            raise RepositoryError(f"Failed to get {self.model.__name__} by category: {str(e)}")

    async def get_categories(self) -> List[str]:
        """
        Get all unique categories.

        Returns:
            List of category names

        Raises:
            RepositoryError: If operation fails
        """
        try:
            if not hasattr(self.model, 'category'):
                raise RepositoryError(f"{self.model.__name__} does not have category field")

            statement = select(self.model.category).distinct()
            result = await self.session.exec(statement)
            categories = [cat for cat in result.all() if cat]
            return sorted(categories)

        except Exception as e:
            raise RepositoryError(f"Failed to get categories for {self.model.__name__}: {str(e)}")


class DateRangeMixin:
    """
    Mixin for date range queries.
    """

    async def get_by_date_range(
        self,
        start_date,
        end_date,
        date_field: str = 'created_at'
    ) -> List[Any]:
        """
        Get records within a date range.

        Args:
            start_date: Start of date range
            end_date: End of date range
            date_field: Name of the date field to filter on

        Returns:
            List of records in the date range

        Raises:
            RepositoryError: If operation fails
        """
        try:
            if not hasattr(self.model, date_field):
                raise RepositoryError(f"{self.model.__name__} does not have {date_field} field")

            field = getattr(self.model, date_field)
            statement = select(self.model).where(
                and_(
                    field >= start_date,
                    field <= end_date
                )
            )

            result = await self.session.exec(statement)
            return result.all()

        except Exception as e:
            raise RepositoryError(f"Failed to get {self.model.__name__} by date range: {str(e)}")

    async def get_recent(
        self,
        days: int = 7,
        limit: Optional[int] = None,
        date_field: str = 'created_at'
    ) -> List[Any]:
        """
        Get recent records.

        Args:
            days: Number of days to look back
            limit: Maximum number of records to return
            date_field: Name of the date field to filter on

        Returns:
            List of recent records

        Raises:
            RepositoryError: If operation fails
        """
        try:
            if not hasattr(self.model, date_field):
                raise RepositoryError(f"{self.model.__name__} does not have {date_field} field")

            from datetime import datetime, timedelta, timezone
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

            field = getattr(self.model, date_field)
            statement = select(self.model).where(field >= cutoff_date).order_by(desc(field))

            if limit:
                statement = statement.limit(limit)

            result = await self.session.exec(statement)
            return result.all()

        except Exception as e:
            raise RepositoryError(f"Failed to get recent {self.model.__name__}: {str(e)}")