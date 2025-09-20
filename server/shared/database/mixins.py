"""
Database mixins for common model functionality.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/20
"""

from sqlmodel import SQLModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from pydantic import field_validator
import json


class JSONFieldMixin(SQLModel):
    """
    Mixin for storing JSON data in database fields.
    Provides serialization/deserialization helpers.
    """

    @staticmethod
    def serialize_json(data: Any) -> Optional[str]:
        """
        Serialize data to JSON string.

        Args:
            data: Data to serialize

        Returns:
            JSON string or None
        """
        if data is None:
            return None
        try:
            return json.dumps(data, default=str, ensure_ascii=False)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def deserialize_json(data: Optional[str]) -> Any:
        """
        Deserialize JSON string to Python object.

        Args:
            data: JSON string to deserialize

        Returns:
            Deserialized object or None
        """
        if not data:
            return None
        try:
            return json.loads(data)
        except (TypeError, ValueError, json.JSONDecodeError):
            return None


class MetadataMixin(JSONFieldMixin):
    """
    Mixin for storing flexible metadata as JSON.
    Useful for storing arbitrary key-value data.
    """

    metadata: Optional[str] = Field(
        default=None,
        description="JSON metadata for flexible data storage"
    )

    def set_metadata(self, key: str, value: Any) -> None:
        """
        Set a metadata value.

        Args:
            key: Metadata key
            value: Metadata value
        """
        current_metadata = self.get_metadata_dict()
        current_metadata[key] = value
        self.metadata = self.serialize_json(current_metadata)

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
        return self.deserialize_json(self.metadata) or {}

    def remove_metadata(self, key: str) -> None:
        """
        Remove a metadata key.

        Args:
            key: Metadata key to remove
        """
        metadata_dict = self.get_metadata_dict()
        metadata_dict.pop(key, None)
        self.metadata = self.serialize_json(metadata_dict) if metadata_dict else None


class TagMixin(SQLModel):
    """
    Mixin for tagging functionality.
    Stores tags as comma-separated string with helper methods.
    """

    tags: Optional[str] = Field(
        default=None,
        description="Comma-separated tags"
    )

    def set_tags(self, tag_list: List[str]) -> None:
        """
        Set tags from a list.

        Args:
            tag_list: List of tags
        """
        if not tag_list:
            self.tags = None
        else:
            # Clean and normalize tags
            clean_tags = [tag.strip().lower() for tag in tag_list if tag.strip()]
            self.tags = ",".join(clean_tags) if clean_tags else None

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


class SlugMixin(SQLModel):
    """
    Mixin for URL-friendly slug generation.
    """

    slug: Optional[str] = Field(
        default=None,
        description="URL-friendly slug",
        max_length=255,
        unique=True
    )

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

    def set_slug_from_title(self, title: str) -> None:
        """
        Set slug from a title field.

        Args:
            title: Title to convert to slug
        """
        self.slug = self.generate_slug(title)


class OrderingMixin(SQLModel):
    """
    Mixin for manual ordering of records.
    """

    order_index: int = Field(
        default=0,
        description="Manual ordering index"
    )

    def move_up(self) -> None:
        """Move item up in order (decrease order_index)."""
        if self.order_index > 0:
            self.order_index -= 1

    def move_down(self) -> None:
        """Move item down in order (increase order_index)."""
        self.order_index += 1

    def set_order(self, index: int) -> None:
        """
        Set specific order index.

        Args:
            index: New order index
        """
        self.order_index = max(0, index)


class VersionMixin(SQLModel):
    """
    Mixin for optimistic locking with version control.
    """

    version: int = Field(
        default=1,
        description="Version number for optimistic locking"
    )

    def increment_version(self) -> None:
        """Increment version for optimistic locking."""
        self.version += 1


class ArchiveMixin(SQLModel):
    """
    Mixin for archiving records instead of hard deletion.
    """

    is_archived: bool = Field(
        default=False,
        description="Archive status"
    )
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