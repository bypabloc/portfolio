"""
Date and time utilities.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/20
"""

from datetime import datetime, timezone, date
from typing import Optional


def utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


def to_utc(dt: datetime) -> datetime:
    """Convert datetime to UTC."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def format_date(dt: Optional[date]) -> Optional[str]:
    """Format date as ISO string."""
    return dt.isoformat() if dt else None


def format_datetime(dt: Optional[datetime]) -> Optional[str]:
    """Format datetime as ISO string."""
    return dt.isoformat() if dt else None


def parse_date(date_str: str) -> Optional[date]:
    """Parse date from ISO string."""
    try:
        return datetime.fromisoformat(date_str).date()
    except (ValueError, TypeError):
        return None


def parse_datetime(datetime_str: str) -> Optional[datetime]:
    """Parse datetime from ISO string."""
    try:
        return datetime.fromisoformat(datetime_str)
    except (ValueError, TypeError):
        return None