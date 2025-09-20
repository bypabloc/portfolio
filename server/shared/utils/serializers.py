"""
Custom serializers for common data types.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/20
"""

import json
from datetime import datetime, date
from typing import Any, Dict, List, Optional
from decimal import Decimal
from uuid import UUID


class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for common Python types."""

    def default(self, obj: Any) -> Any:
        """Convert custom types to JSON serializable format."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, UUID):
            return str(obj)
        elif hasattr(obj, 'model_dump'):
            # SQLModel/Pydantic objects
            return obj.model_dump()
        elif hasattr(obj, '__dict__'):
            # Generic objects
            return obj.__dict__
        return super().default(obj)


def serialize_json(data: Any) -> str:
    """Serialize data to JSON string with custom encoder."""
    return json.dumps(data, cls=CustomJSONEncoder, ensure_ascii=False)


def deserialize_json(json_str: str) -> Any:
    """Deserialize JSON string to Python object."""
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return None


def to_dict(obj: Any, exclude_none: bool = True) -> Dict[str, Any]:
    """Convert object to dictionary."""
    if hasattr(obj, 'model_dump'):
        return obj.model_dump(exclude_none=exclude_none)
    elif hasattr(obj, '__dict__'):
        result = obj.__dict__.copy()
        if exclude_none:
            return {k: v for k, v in result.items() if v is not None}
        return result
    return {}


def clean_dict(data: Dict[str, Any], remove_empty: bool = True) -> Dict[str, Any]:
    """Clean dictionary by removing None/empty values."""
    if not isinstance(data, dict):
        return data

    result = {}
    for key, value in data.items():
        if remove_empty and (value is None or value == "" or value == []):
            continue
        result[key] = value

    return result