"""
Security utilities for Lambda functions.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/20
"""

import hashlib
import secrets
from typing import Optional


def generate_api_key(length: int = 32) -> str:
    """Generate secure API key."""
    return secrets.token_urlsafe(length)


def hash_password(password: str) -> str:
    """Hash password with salt."""
    salt = secrets.token_hex(16)
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex() + ':' + salt


def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash."""
    try:
        password_hash, salt = hashed.split(':')
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex() == password_hash
    except ValueError:
        return False


def sanitize_input(text: str, max_length: int = 1000) -> str:
    """Sanitize user input."""
    return text.strip()[:max_length] if text else ""