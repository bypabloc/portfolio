"""
Application settings using Pydantic Settings.

Centralized configuration management for all Lambda functions with
environment-specific overrides and validation.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/20
"""

import os
from typing import Optional, List, Dict, Any
from pydantic import Field, validator, root_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8"
    )

    url: str = Field(
        default="postgresql://postgres:password@localhost:5432/portfolio",
        description="Database connection URL"
    )
    host: str = Field(default="localhost", description="Database host")
    port: int = Field(default=5432, description="Database port")
    name: str = Field(default="portfolio", description="Database name")
    user: str = Field(default="postgres", description="Database user")
    password: str = Field(default="password", description="Database password")
    ssl_mode: str = Field(default="prefer", description="SSL mode")

    # Connection pool settings
    pool_size: int = Field(default=5, description="Connection pool size")
    max_overflow: int = Field(default=0, description="Max overflow connections")
    pool_timeout: int = Field(default=30, description="Pool timeout in seconds")
    pool_recycle: int = Field(default=300, description="Pool recycle time in seconds")
    pool_pre_ping: bool = Field(default=True, description="Enable pool pre-ping")

    @validator('url', pre=True)
    def build_database_url(cls, v, values):
        """Build database URL from components if not provided."""
        if v and v != "postgresql://postgres:password@localhost:5432/portfolio":
            return v

        # Build URL from components
        host = values.get('host', 'localhost')
        port = values.get('port', 5432)
        name = values.get('name', 'portfolio')
        user = values.get('user', 'postgres')
        password = values.get('password', 'password')

        return f"postgresql://{user}:{password}@{host}:{port}/{name}"


class AWSSettings(BaseSettings):
    """AWS configuration settings."""

    model_config = SettingsConfigDict(
        env_prefix="AWS_",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8"
    )

    region: str = Field(default="us-east-1", description="AWS region")
    access_key_id: Optional[str] = Field(None, description="AWS access key ID")
    secret_access_key: Optional[str] = Field(None, description="AWS secret access key")
    session_token: Optional[str] = Field(None, description="AWS session token")

    # Lambda settings
    function_name: Optional[str] = Field(None, description="Lambda function name")
    function_version: str = Field(default="$LATEST", description="Lambda function version")
    log_group: Optional[str] = Field(None, description="CloudWatch log group")
    log_stream: Optional[str] = Field(None, description="CloudWatch log stream")

    # X-Ray tracing
    xray_enabled: bool = Field(default=False, description="Enable X-Ray tracing")
    xray_sampling_rate: float = Field(default=0.1, description="X-Ray sampling rate")


class CORSSettings(BaseSettings):
    """CORS configuration settings."""

    model_config = SettingsConfigDict(
        env_prefix="CORS_",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8"
    )

    allow_origins: List[str] = Field(
        default=["*"],
        description="Allowed origins for CORS"
    )
    allow_methods: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        description="Allowed HTTP methods"
    )
    allow_headers: List[str] = Field(
        default=["*"],
        description="Allowed headers"
    )
    allow_credentials: bool = Field(default=True, description="Allow credentials")
    max_age: int = Field(default=600, description="Max age for preflight requests")

    @validator('allow_origins', pre=True)
    def parse_origins(cls, v):
        """Parse origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    @validator('allow_methods', pre=True)
    def parse_methods(cls, v):
        """Parse methods from string or list."""
        if isinstance(v, str):
            return [method.strip().upper() for method in v.split(",") if method.strip()]
        return v

    @validator('allow_headers', pre=True)
    def parse_headers(cls, v):
        """Parse headers from string or list."""
        if isinstance(v, str):
            return [header.strip() for header in v.split(",") if header.strip()]
        return v


class SecuritySettings(BaseSettings):
    """Security configuration settings."""

    model_config = SettingsConfigDict(
        env_prefix="SECURITY_",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8"
    )

    secret_key: str = Field(
        default="dev-secret-key-change-in-production",
        description="Secret key for encryption"
    )
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(
        default=30,
        description="Access token expiration in minutes"
    )

    # Rate limiting
    rate_limit_enabled: bool = Field(default=True, description="Enable rate limiting")
    rate_limit_requests: int = Field(default=100, description="Requests per window")
    rate_limit_window: int = Field(default=3600, description="Rate limit window in seconds")

    # Input validation
    max_request_size: int = Field(default=1048576, description="Max request size in bytes")  # 1MB
    max_query_params: int = Field(default=100, description="Max query parameters")
    max_headers: int = Field(default=50, description="Max headers")


class LoggingSettings(BaseSettings):
    """Logging configuration settings."""

    model_config = SettingsConfigDict(
        env_prefix="LOG_",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8"
    )

    level: str = Field(default="INFO", description="Log level")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format"
    )
    json_logs: bool = Field(default=True, description="Use JSON logging")
    include_request_id: bool = Field(default=True, description="Include request ID")
    include_user_id: bool = Field(default=False, description="Include user ID")

    # CloudWatch settings
    cloudwatch_enabled: bool = Field(default=True, description="Enable CloudWatch logging")
    cloudwatch_group: Optional[str] = Field(None, description="CloudWatch log group")
    cloudwatch_stream: Optional[str] = Field(None, description="CloudWatch log stream")

    @validator('level')
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {valid_levels}")
        return v.upper()


class CacheSettings(BaseSettings):
    """Cache configuration settings."""

    model_config = SettingsConfigDict(
        env_prefix="CACHE_",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8"
    )

    enabled: bool = Field(default=True, description="Enable caching")
    ttl: int = Field(default=300, description="Default TTL in seconds")
    max_size: int = Field(default=1000, description="Max cache size")

    # Redis settings (if using external cache)
    redis_url: Optional[str] = Field(None, description="Redis connection URL")
    redis_enabled: bool = Field(default=False, description="Enable Redis cache")


class ApplicationSettings(BaseSettings):
    """Main application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    # Application info
    app_name: str = Field(default="Portfolio API", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    description: str = Field(
        default="Portfolio serverless API",
        description="Application description"
    )

    # Environment
    environment: str = Field(default="development", description="Environment name")
    debug: bool = Field(default=False, description="Debug mode")
    testing: bool = Field(default=False, description="Testing mode")

    # API settings
    api_prefix: str = Field(default="/api/v1", description="API prefix")
    docs_url: Optional[str] = Field(default="/docs", description="API docs URL")
    redoc_url: Optional[str] = Field(default="/redoc", description="ReDoc URL")
    openapi_url: Optional[str] = Field(default="/openapi.json", description="OpenAPI URL")

    # Sub-settings
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    aws: AWSSettings = Field(default_factory=AWSSettings)
    cors: CORSSettings = Field(default_factory=CORSSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    cache: CacheSettings = Field(default_factory=CacheSettings)

    @validator('environment')
    def validate_environment(cls, v):
        """Validate environment name."""
        valid_envs = ["development", "testing", "staging", "production"]
        if v not in valid_envs:
            raise ValueError(f"Environment must be one of: {valid_envs}")
        return v

    @root_validator
    def validate_production_settings(cls, values):
        """Validate production-specific settings."""
        environment = values.get('environment')
        debug = values.get('debug')
        security = values.get('security')

        if environment == 'production':
            if debug:
                raise ValueError("Debug mode cannot be enabled in production")

            if security and security.secret_key == "dev-secret-key-change-in-production":
                raise ValueError("Secret key must be changed in production")

        return values

    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == "production"

    @property
    def is_testing(self) -> bool:
        """Check if running in testing."""
        return self.testing or self.environment == "testing"

    def get_database_url(self) -> str:
        """Get database URL for async engine."""
        url = self.database.url
        if not url.startswith(("postgresql+asyncpg://", "postgresql://")):
            # Convert to asyncpg URL
            if url.startswith("postgresql://"):
                url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return url


@lru_cache()
def get_settings() -> ApplicationSettings:
    """
    Get cached application settings.

    Returns:
        ApplicationSettings instance

    Note:
        This function is cached to avoid re-reading environment variables
        on every call in Lambda functions.
    """
    return ApplicationSettings()