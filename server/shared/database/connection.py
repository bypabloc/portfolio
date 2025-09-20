"""
Database connection management for AWS Lambda functions.
Optimized for serverless environments with connection pooling.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/20
"""

import os
from typing import Optional, AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from aws_lambda_powertools import Logger
from functools import lru_cache

logger = Logger()


class DatabaseManager:
    """
    Singleton database manager optimized for AWS Lambda.

    Manages connection pooling and session lifecycle for serverless environments.
    Implements lazy initialization and connection reuse patterns.
    """

    _engine = None
    _session_factory = None

    @classmethod
    @lru_cache(maxsize=1)
    def get_database_url(cls) -> str:
        """
        Get database URL from environment variables.
        Cached to avoid repeated environment variable lookups.

        Returns:
            str: Database connection URL

        Raises:
            ValueError: If DATABASE_URL is not set
        """
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable is required")
        return database_url

    @classmethod
    async def get_engine(cls):
        """
        Get or create async database engine.
        Singleton pattern for Lambda container reuse.

        Returns:
            AsyncEngine: SQLAlchemy async engine
        """
        if cls._engine is None:
            database_url = cls.get_database_url()

            cls._engine = create_async_engine(
                database_url,
                echo=False,  # Set to True for SQL debugging
                pool_size=3,        # Low for Lambda memory limits
                max_overflow=0,     # No overflow connections
                pool_pre_ping=True, # Verify connections before use
                pool_recycle=300,   # Recycle connections every 5 minutes
                pool_timeout=30,    # Timeout for getting connection
                # Lambda-specific optimizations
                connect_args={
                    "server_settings": {
                        "jit": "off",  # Disable JIT for faster connections
                        "application_name": "portfolio_lambda",
                    }
                }
            )

            logger.info("Database engine created", extra={
                "pool_size": 3,
                "pool_recycle": 300,
                "database_url_host": database_url.split('@')[1].split('/')[0] if '@' in database_url else "unknown"
            })

        return cls._engine

    @classmethod
    async def get_session_factory(cls):
        """
        Get or create session factory.

        Returns:
            sessionmaker: Configured session factory
        """
        if cls._session_factory is None:
            engine = await cls.get_engine()
            cls._session_factory = sessionmaker(
                bind=engine,
                class_=AsyncSession,
                expire_on_commit=False,  # Important for Lambda
                autoflush=False,
                autocommit=False
            )

        return cls._session_factory

    @classmethod
    async def create_tables(cls) -> None:
        """
        Create all tables defined in SQLModel.
        Used for database initialization.
        """
        engine = await cls.get_engine()
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
            logger.info("Database tables created successfully")

    @classmethod
    async def close_connections(cls) -> None:
        """
        Close all database connections.
        Call this during Lambda cleanup to prevent connection leaks.
        """
        if cls._engine:
            await cls._engine.dispose()
            cls._engine = None
            cls._session_factory = None
            logger.info("Database connections closed")


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Context manager for database sessions.

    Yields:
        AsyncSession: Database session with automatic cleanup

    Example:
        async with get_async_session() as session:
            result = await session.exec(select(User))
    """
    session_factory = await DatabaseManager.get_session_factory()
    async with session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# FastAPI dependency function
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for database sessions.

    Usage:
        @app.get("/users")
        async def get_users(session: AsyncSession = Depends(get_db_session)):
            return await session.exec(select(User))
    """
    async with get_async_session() as session:
        yield session


# Lambda lifecycle management
async def init_database() -> None:
    """
    Initialize database for Lambda cold starts.
    Call this in Lambda initialization phase.
    """
    await DatabaseManager.get_engine()
    logger.info("Database initialized for Lambda")


async def cleanup_database() -> None:
    """
    Cleanup database connections.
    Call this when Lambda is about to timeout or shutdown.
    """
    await DatabaseManager.close_connections()