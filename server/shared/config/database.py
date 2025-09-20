"""
Database configuration and factory functions.

Provides database connection configuration optimized for different environments
and Lambda execution contexts.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/20
"""

import os
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.pool import StaticPool, QueuePool
from .settings import get_settings


class DatabaseConfig:
    """Database configuration factory."""

    @staticmethod
    def get_engine_config(environment: Optional[str] = None) -> Dict[str, Any]:
        """
        Get database engine configuration for specific environment.

        Args:
            environment: Environment name (development, testing, production)

        Returns:
            Dictionary with engine configuration parameters
        """
        settings = get_settings()
        env = environment or settings.environment

        base_config = {
            "echo": settings.debug and env == "development",
            "pool_pre_ping": settings.database.pool_pre_ping,
            "pool_recycle": settings.database.pool_recycle,
            "pool_timeout": settings.database.pool_timeout,
        }

        if env == "development":
            return {
                **base_config,
                "pool_size": 5,
                "max_overflow": 10,
                "poolclass": QueuePool,
                "connect_args": {
                    "server_settings": {
                        "application_name": f"portfolio_dev_{settings.app_name}",
                        "jit": "off",  # Disable JIT for faster connections
                    }
                }
            }

        elif env == "testing":
            return {
                **base_config,
                "pool_size": 1,
                "max_overflow": 0,
                "poolclass": StaticPool,
                "connect_args": {
                    "server_settings": {
                        "application_name": f"portfolio_test_{settings.app_name}",
                        "jit": "off",
                    }
                }
            }

        elif env == "production":
            return {
                **base_config,
                "pool_size": settings.database.pool_size,
                "max_overflow": settings.database.max_overflow,
                "poolclass": QueuePool,
                "connect_args": {
                    "server_settings": {
                        "application_name": f"portfolio_prod_{settings.app_name}",
                        "jit": "off",  # Disable JIT for Lambda cold starts
                        "timezone": "UTC",
                    }
                }
            }

        else:  # staging or other environments
            return {
                **base_config,
                "pool_size": 3,
                "max_overflow": 5,
                "poolclass": QueuePool,
                "connect_args": {
                    "server_settings": {
                        "application_name": f"portfolio_staging_{settings.app_name}",
                        "jit": "off",
                    }
                }
            }

    @staticmethod
    def create_engine(
        database_url: Optional[str] = None,
        environment: Optional[str] = None
    ) -> AsyncEngine:
        """
        Create async database engine with appropriate configuration.

        Args:
            database_url: Custom database URL (uses settings if not provided)
            environment: Environment name

        Returns:
            Configured async SQLAlchemy engine
        """
        settings = get_settings()
        url = database_url or settings.get_database_url()
        config = DatabaseConfig.get_engine_config(environment)

        return create_async_engine(url, **config)

    @staticmethod
    def get_lambda_config() -> Dict[str, Any]:
        """
        Get optimized configuration for AWS Lambda.

        Returns:
            Dictionary with Lambda-optimized engine configuration
        """
        return {
            "echo": False,  # No verbose logging in Lambda
            "pool_size": 1,  # Single connection per Lambda container
            "max_overflow": 0,  # No overflow connections
            "pool_pre_ping": True,  # Verify connections before use
            "pool_recycle": 300,  # Recycle connections every 5 minutes
            "pool_timeout": 10,  # Short timeout for Lambda
            "poolclass": StaticPool,  # Static pool for single connection
            "connect_args": {
                "server_settings": {
                    "application_name": "portfolio_lambda",
                    "jit": "off",  # Disable JIT for fast connections
                    "timezone": "UTC",
                    "statement_timeout": "30s",  # Prevent long-running queries
                    "idle_in_transaction_session_timeout": "60s",
                }
            }
        }

    @staticmethod
    def create_lambda_engine(database_url: Optional[str] = None) -> AsyncEngine:
        """
        Create database engine optimized for AWS Lambda.

        Args:
            database_url: Custom database URL

        Returns:
            Lambda-optimized async SQLAlchemy engine
        """
        settings = get_settings()
        url = database_url or settings.get_database_url()
        config = DatabaseConfig.get_lambda_config()

        return create_async_engine(url, **config)


class NeonConfig:
    """Neon PostgreSQL specific configuration."""

    @staticmethod
    def get_branch_url(branch_name: str, base_url: Optional[str] = None) -> str:
        """
        Get Neon database URL for specific branch.

        Args:
            branch_name: Neon branch name
            base_url: Base database URL

        Returns:
            Branch-specific database URL
        """
        settings = get_settings()
        url = base_url or settings.database.url

        # Add branch parameter to URL
        separator = "&" if "?" in url else "?"
        return f"{url}{separator}branch={branch_name}"

    @staticmethod
    def get_environment_branch() -> str:
        """
        Get Neon branch name for current environment.

        Returns:
            Branch name for current environment
        """
        settings = get_settings()
        environment = settings.environment

        branch_mapping = {
            "production": "main",
            "staging": "staging",
            "development": "dev",
            "testing": "test"
        }

        return branch_mapping.get(environment, environment)

    @staticmethod
    def create_branch_engine(
        branch_name: Optional[str] = None,
        base_url: Optional[str] = None
    ) -> AsyncEngine:
        """
        Create engine for specific Neon branch.

        Args:
            branch_name: Neon branch name (uses environment default if not provided)
            base_url: Base database URL

        Returns:
            Engine configured for specific branch
        """
        branch = branch_name or NeonConfig.get_environment_branch()
        url = NeonConfig.get_branch_url(branch, base_url)

        return DatabaseConfig.create_engine(url)


class ConnectionStrings:
    """Database connection string utilities."""

    @staticmethod
    def get_sync_url(async_url: str) -> str:
        """
        Convert async database URL to sync URL.

        Args:
            async_url: Async database URL

        Returns:
            Sync database URL
        """
        return async_url.replace("postgresql+asyncpg://", "postgresql://")

    @staticmethod
    def get_async_url(sync_url: str) -> str:
        """
        Convert sync database URL to async URL.

        Args:
            sync_url: Sync database URL

        Returns:
            Async database URL
        """
        if sync_url.startswith("postgresql://") and not sync_url.startswith("postgresql+asyncpg://"):
            return sync_url.replace("postgresql://", "postgresql+asyncpg://")
        return sync_url

    @staticmethod
    def parse_url(url: str) -> Dict[str, str]:
        """
        Parse database URL into components.

        Args:
            url: Database URL

        Returns:
            Dictionary with URL components
        """
        from urllib.parse import urlparse

        parsed = urlparse(url)

        return {
            "scheme": parsed.scheme,
            "username": parsed.username,
            "password": parsed.password,
            "hostname": parsed.hostname,
            "port": str(parsed.port) if parsed.port else "5432",
            "database": parsed.path.lstrip("/"),
            "query": parsed.query,
            "fragment": parsed.fragment
        }

    @staticmethod
    def build_url(
        username: str,
        password: str,
        hostname: str,
        database: str,
        port: int = 5432,
        scheme: str = "postgresql+asyncpg",
        **kwargs
    ) -> str:
        """
        Build database URL from components.

        Args:
            username: Database username
            password: Database password
            hostname: Database hostname
            database: Database name
            port: Database port
            scheme: URL scheme
            **kwargs: Additional query parameters

        Returns:
            Complete database URL
        """
        url = f"{scheme}://{username}:{password}@{hostname}:{port}/{database}"

        if kwargs:
            query_params = "&".join([f"{k}={v}" for k, v in kwargs.items()])
            url += f"?{query_params}"

        return url


def get_database_engine() -> AsyncEngine:
    """
    Get database engine for current environment.

    Returns:
        Configured database engine
    """
    settings = get_settings()

    # Check if running in Lambda
    if os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
        return DatabaseConfig.create_lambda_engine()

    # Use environment-specific configuration
    return DatabaseConfig.create_engine()


def get_neon_engine(branch_name: Optional[str] = None) -> AsyncEngine:
    """
    Get Neon database engine for specific branch.

    Args:
        branch_name: Neon branch name

    Returns:
        Neon branch-specific engine
    """
    return NeonConfig.create_branch_engine(branch_name)