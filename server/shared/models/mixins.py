"""
Model mixins for common functionality.

These mixins provide reusable model functionality that can be mixed into
different SQLModel classes to add common features.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/20
"""

from sqlmodel import SQLModel, Field
from pydantic import field_validator, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from .common import (
    IsActiveField,
    IsFeaturedField,
    OrderIndexField,
    TagsField,
    MetadataField,
    VersionField
)
import json


class TimestampMixin(SQLModel):
    """
    Mixin for automatic timestamp management.
    Adds created_at and updated_at fields with automatic handling.
    """

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Record creation timestamp"
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description="Record last update timestamp"
    )

    def update_timestamp(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now(timezone.utc)

    @field_validator('created_at', 'updated_at', mode='before')
    @classmethod
    def validate_timezone(cls, v):
        """Ensure datetime has timezone info."""
        if v and isinstance(v, datetime) and v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v


class StatusMixin(SQLModel):
    """
    Mixin for status management.
    Adds is_active field and related methods.
    """

    is_active: IsActiveField

    def activate(self) -> None:
        """Mark record as active."""
        self.is_active = True
        if hasattr(self, 'update_timestamp'):
            self.update_timestamp()

    def deactivate(self) -> None:
        """Mark record as inactive."""
        self.is_active = False
        if hasattr(self, 'update_timestamp'):
            self.update_timestamp()

    @property
    def status_text(self) -> str:
        """Get human-readable status."""
        return "Active" if self.is_active else "Inactive"


class FeaturedMixin(SQLModel):
    """
    Mixin for featured content management.
    Adds is_featured field and related methods.
    """

    is_featured: IsFeaturedField

    def set_featured(self, featured: bool = True) -> None:
        """Set featured status."""
        self.is_featured = featured
        if hasattr(self, 'update_timestamp'):
            self.update_timestamp()

    def feature(self) -> None:
        """Mark as featured."""
        self.set_featured(True)

    def unfeature(self) -> None:
        """Remove featured status."""
        self.set_featured(False)


class OrderingMixin(SQLModel):
    """
    Mixin for manual ordering of records.
    Adds order_index field and ordering methods.
    """

    order_index: OrderIndexField

    def move_up(self, steps: int = 1) -> None:
        """Move item up in order (decrease order_index)."""
        self.order_index = max(0, self.order_index - steps)
        if hasattr(self, 'update_timestamp'):
            self.update_timestamp()

    def move_down(self, steps: int = 1) -> None:
        """Move item down in order (increase order_index)."""
        self.order_index += steps
        if hasattr(self, 'update_timestamp'):
            self.update_timestamp()

    def set_order(self, index: int) -> None:
        """Set specific order index."""
        self.order_index = max(0, index)
        if hasattr(self, 'update_timestamp'):
            self.update_timestamp()


class TagMixin(SQLModel):
    """
    Mixin for tag management.
    Stores tags as comma-separated string with helper methods.
    """

    tags: TagsField

    def set_tags(self, tag_list: List[str]) -> None:
        """
        Set tags from a list.

        Args:
            tag_list: List of tags to set
        """
        if not tag_list:
            self.tags = None
        else:
            # Clean and normalize tags
            clean_tags = [tag.strip().lower() for tag in tag_list if tag.strip()]
            self.tags = ",".join(clean_tags) if clean_tags else None

        if hasattr(self, 'update_timestamp'):
            self.update_timestamp()

    def get_tags(self) -> List[str]:
        """
        Get tags as a list.

        Returns:
            List of tags
        """
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]

    def add_tag(self, tag: str) -> None:
        """
        Add a single tag.

        Args:
            tag: Tag to add
        """
        current_tags = self.get_tags()
        clean_tag = tag.strip().lower()
        if clean_tag and clean_tag not in current_tags:
            current_tags.append(clean_tag)
            self.set_tags(current_tags)

    def remove_tag(self, tag: str) -> None:
        """
        Remove a single tag.

        Args:
            tag: Tag to remove
        """
        current_tags = self.get_tags()
        clean_tag = tag.strip().lower()
        if clean_tag in current_tags:
            current_tags.remove(clean_tag)
            self.set_tags(current_tags)

    def has_tag(self, tag: str) -> bool:
        """
        Check if a tag exists.

        Args:
            tag: Tag to check

        Returns:
            True if tag exists
        """
        return tag.strip().lower() in self.get_tags()

    def clear_tags(self) -> None:
        """Remove all tags."""
        self.tags = None
        if hasattr(self, 'update_timestamp'):
            self.update_timestamp()


class MetadataMixin(SQLModel):
    """
    Mixin for flexible metadata storage as JSON.
    Useful for storing arbitrary key-value data.
    """

    metadata: MetadataField

    def set_metadata(self, key: str, value: Any) -> None:
        """
        Set a metadata value.

        Args:
            key: Metadata key
            value: Metadata value
        """
        current_metadata = self.get_metadata_dict()
        current_metadata[key] = value
        self.metadata = self._serialize_metadata(current_metadata)

        if hasattr(self, 'update_timestamp'):
            self.update_timestamp()

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """
        Get a metadata value.

        Args:
            key: Metadata key
            default: Default value if key not found

        Returns:
            Metadata value or default
        """
        metadata_dict = self.get_metadata_dict()
        return metadata_dict.get(key, default)

    def get_metadata_dict(self) -> Dict[str, Any]:
        """
        Get metadata as dictionary.

        Returns:
            Dictionary of metadata
        """
        return self._deserialize_metadata(self.metadata) or {}

    def remove_metadata(self, key: str) -> None:
        """
        Remove a metadata key.

        Args:
            key: Metadata key to remove
        """
        metadata_dict = self.get_metadata_dict()
        metadata_dict.pop(key, None)
        self.metadata = self._serialize_metadata(metadata_dict) if metadata_dict else None

        if hasattr(self, 'update_timestamp'):
            self.update_timestamp()

    def clear_metadata(self) -> None:
        """Remove all metadata."""
        self.metadata = None
        if hasattr(self, 'update_timestamp'):
            self.update_timestamp()

    @staticmethod
    def _serialize_metadata(data: Dict[str, Any]) -> Optional[str]:
        """Serialize metadata to JSON string."""
        if not data:
            return None
        try:
            return json.dumps(data, default=str, ensure_ascii=False)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _deserialize_metadata(data: Optional[str]) -> Optional[Dict[str, Any]]:
        """Deserialize JSON string to dictionary."""
        if not data:
            return None
        try:
            return json.loads(data)
        except (TypeError, ValueError, json.JSONDecodeError):
            return None


class VersionMixin(SQLModel):
    """
    Mixin for optimistic locking with version control.
    Useful for preventing concurrent modification issues.
    """

    version: VersionField

    def increment_version(self) -> None:
        """Increment version for optimistic locking."""
        self.version += 1
        if hasattr(self, 'update_timestamp'):
            self.update_timestamp()


class SlugMixin(SQLModel):
    """
    Mixin for URL-friendly slug generation.
    """

    slug: Optional[str] = Field(
        default=None,
        max_length=255,
        regex=r'^[a-z0-9-]+$',
        description="URL-friendly slug"
    )

    def set_slug_from_title(self, title: str) -> None:
        """
        Generate and set slug from a title.

        Args:
            title: Title to convert to slug
        """
        self.slug = self.generate_slug(title)
        if hasattr(self, 'update_timestamp'):
            self.update_timestamp()

    @staticmethod
    def generate_slug(text: str) -> str:
        """
        Generate a URL-friendly slug from text.

        Args:
            text: Text to convert to slug

        Returns:
            URL-friendly slug
        """
        import re
        # Convert to lowercase and replace spaces with hyphens
        slug = re.sub(r'\s+', '-', text.lower().strip())
        # Remove non-alphanumeric characters except hyphens
        slug = re.sub(r'[^a-z0-9\-]', '', slug)
        # Remove multiple consecutive hyphens
        slug = re.sub(r'-+', '-', slug)
        # Remove leading/trailing hyphens
        return slug.strip('-')


class ArchiveMixin(SQLModel):
    """
    Mixin for archiving records instead of hard deletion.
    """

    is_archived: bool = Field(default=False, description="Archive status")
    archived_at: Optional[datetime] = Field(
        default=None,
        description="Archive timestamp"
    )

    def archive(self) -> None:
        """Archive the record."""
        self.is_archived = True
        self.archived_at = datetime.now(timezone.utc)
        if hasattr(self, 'update_timestamp'):
            self.update_timestamp()

    def unarchive(self) -> None:
        """Unarchive the record."""
        self.is_archived = False
        self.archived_at = None
        if hasattr(self, 'update_timestamp'):
            self.update_timestamp()

    @property
    def archive_status(self) -> str:
        """Get human-readable archive status."""
        return "Archived" if self.is_archived else "Active"


class PublishMixin(SQLModel):
    """
    Mixin for content publishing workflow.
    """

    is_published: bool = Field(default=False, description="Published status")
    published_at: Optional[datetime] = Field(
        default=None,
        description="Publish timestamp"
    )

    def publish(self) -> None:
        """Publish the content."""
        self.is_published = True
        self.published_at = datetime.now(timezone.utc)
        if hasattr(self, 'update_timestamp'):
            self.update_timestamp()

    def unpublish(self) -> None:
        """Unpublish the content."""
        self.is_published = False
        self.published_at = None
        if hasattr(self, 'update_timestamp'):
            self.update_timestamp()

    @property
    def publish_status(self) -> str:
        """Get human-readable publish status."""
        return "Published" if self.is_published else "Draft"


# Combined mixins for common use cases
class BaseContentMixin(TimestampMixin, StatusMixin, OrderingMixin):
    """
    Combined mixin for basic content functionality.
    Includes timestamps, status, and ordering.
    """
    pass


class FullContentMixin(
    TimestampMixin,
    StatusMixin,
    FeaturedMixin,
    OrderingMixin,
    TagMixin,
    MetadataMixin,
    SlugMixin
):
    """
    Combined mixin for full content functionality.
    Includes all common content features.
    """
    pass