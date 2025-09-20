"""
Shared module for Lambda functions.

This module provides common functionality across all Lambda functions including:
- Database connection and session management
- Base models and schemas with validation
- Repository pattern implementations
- Configuration management
- Utility functions and logging
- Custom exception handling

Usage:
    from server.shared.database import get_async_session
    from server.shared.repository import CRUDRepository
    from server.shared.models import HealthResponse, APIResponse
    from server.shared.utils import get_logger

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/20
"""

__version__ = "1.0.0"