"""
Environment detection and configuration.

Provides utilities for detecting the runtime environment and configuring
application behavior accordingly.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/20
"""

import os
from typing import Dict, Any, Optional, List
from enum import Enum
from dataclasses import dataclass
from functools import lru_cache


class Environment(str, Enum):
    """Environment enumeration."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class Runtime(str, Enum):
    """Runtime environment enumeration."""
    LOCAL = "local"
    LAMBDA = "lambda"
    CONTAINER = "container"
    UNKNOWN = "unknown"


@dataclass
class EnvironmentInfo:
    """Environment information container."""
    name: Environment
    runtime: Runtime
    is_local: bool
    is_lambda: bool
    is_container: bool
    is_development: bool
    is_production: bool
    is_testing: bool
    aws_region: Optional[str]
    function_name: Optional[str]
    function_version: Optional[str]
    log_group: Optional[str]


class EnvironmentDetector:
    """Environment detection utilities."""

    @staticmethod
    def get_current_environment() -> Environment:
        """
        Detect current environment from environment variables.

        Returns:
            Current environment enum
        """
        env_name = os.getenv("ENVIRONMENT", os.getenv("ENV", "development")).lower()

        # Map common variations
        env_mapping = {
            "dev": Environment.DEVELOPMENT,
            "develop": Environment.DEVELOPMENT,
            "development": Environment.DEVELOPMENT,
            "test": Environment.TESTING,
            "testing": Environment.TESTING,
            "stage": Environment.STAGING,
            "staging": Environment.STAGING,
            "prod": Environment.PRODUCTION,
            "production": Environment.PRODUCTION,
        }

        return env_mapping.get(env_name, Environment.DEVELOPMENT)

    @staticmethod
    def get_current_runtime() -> Runtime:
        """
        Detect current runtime environment.

        Returns:
            Current runtime enum
        """
        # Check for AWS Lambda
        if os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
            return Runtime.LAMBDA

        # Check for container environment
        if (
            os.path.exists("/.dockerenv") or
            os.getenv("CONTAINER") or
            os.getenv("DOCKER_CONTAINER")
        ):
            return Runtime.CONTAINER

        # Check for local development indicators
        if (
            os.getenv("LOCAL_DEVELOPMENT") or
            os.getenv("PYTHONPATH") or
            os.path.exists("./venv") or
            os.path.exists("./.env")
        ):
            return Runtime.LOCAL

        return Runtime.UNKNOWN

    @staticmethod
    def is_lambda() -> bool:
        """Check if running in AWS Lambda."""
        return EnvironmentDetector.get_current_runtime() == Runtime.LAMBDA

    @staticmethod
    def is_local() -> bool:
        """Check if running locally."""
        return EnvironmentDetector.get_current_runtime() == Runtime.LOCAL

    @staticmethod
    def is_container() -> bool:
        """Check if running in container."""
        return EnvironmentDetector.get_current_runtime() == Runtime.CONTAINER

    @staticmethod
    def get_aws_info() -> Dict[str, Optional[str]]:
        """
        Get AWS-specific environment information.

        Returns:
            Dictionary with AWS environment info
        """
        return {
            "region": os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION")),
            "function_name": os.getenv("AWS_LAMBDA_FUNCTION_NAME"),
            "function_version": os.getenv("AWS_LAMBDA_FUNCTION_VERSION"),
            "log_group": os.getenv("AWS_LAMBDA_LOG_GROUP_NAME"),
            "log_stream": os.getenv("AWS_LAMBDA_LOG_STREAM_NAME"),
            "execution_env": os.getenv("AWS_EXECUTION_ENV"),
            "runtime_dir": os.getenv("LAMBDA_RUNTIME_DIR"),
            "task_root": os.getenv("LAMBDA_TASK_ROOT"),
        }


@lru_cache()
def get_environment_info() -> EnvironmentInfo:
    """
    Get comprehensive environment information.

    Returns:
        EnvironmentInfo with all detected information
    """
    env = EnvironmentDetector.get_current_environment()
    runtime = EnvironmentDetector.get_current_runtime()
    aws_info = EnvironmentDetector.get_aws_info()

    return EnvironmentInfo(
        name=env,
        runtime=runtime,
        is_local=runtime == Runtime.LOCAL,
        is_lambda=runtime == Runtime.LAMBDA,
        is_container=runtime == Runtime.CONTAINER,
        is_development=env == Environment.DEVELOPMENT,
        is_production=env == Environment.PRODUCTION,
        is_testing=env == Environment.TESTING,
        aws_region=aws_info["region"],
        function_name=aws_info["function_name"],
        function_version=aws_info["function_version"],
        log_group=aws_info["log_group"],
    )


class EnvironmentConfig:
    """Environment-specific configuration utilities."""

    @staticmethod
    def get_feature_flags(environment: Optional[Environment] = None) -> Dict[str, bool]:
        """
        Get environment-specific feature flags.

        Args:
            environment: Environment to get flags for

        Returns:
            Dictionary of feature flags
        """
        env = environment or EnvironmentDetector.get_current_environment()

        base_flags = {
            "debug_mode": False,
            "verbose_logging": False,
            "api_docs_enabled": False,
            "cors_enabled": True,
            "rate_limiting": True,
            "caching": True,
            "metrics_enabled": True,
            "health_checks": True,
        }

        if env == Environment.DEVELOPMENT:
            return {
                **base_flags,
                "debug_mode": True,
                "verbose_logging": True,
                "api_docs_enabled": True,
                "rate_limiting": False,
            }

        elif env == Environment.TESTING:
            return {
                **base_flags,
                "debug_mode": True,
                "verbose_logging": False,
                "api_docs_enabled": False,
                "rate_limiting": False,
                "caching": False,
            }

        elif env == Environment.STAGING:
            return {
                **base_flags,
                "debug_mode": False,
                "verbose_logging": True,
                "api_docs_enabled": True,
            }

        else:  # Production
            return {
                **base_flags,
                "debug_mode": False,
                "verbose_logging": False,
                "api_docs_enabled": False,
            }

    @staticmethod
    def get_lambda_config() -> Dict[str, Any]:
        """
        Get Lambda-specific configuration.

        Returns:
            Dictionary with Lambda configuration
        """
        env_info = get_environment_info()

        if not env_info.is_lambda:
            return {}

        return {
            "function_name": env_info.function_name,
            "function_version": env_info.function_version,
            "log_group": env_info.log_group,
            "region": env_info.aws_region,
            "timeout_buffer": 5,  # seconds before timeout to cleanup
            "memory_limit": int(os.getenv("AWS_LAMBDA_FUNCTION_MEMORY_SIZE", "128")),
            "cold_start": not bool(os.getenv("LAMBDA_WARM")),
        }

    @staticmethod
    def get_cors_origins(environment: Optional[Environment] = None) -> List[str]:
        """
        Get environment-specific CORS origins.

        Args:
            environment: Environment to get origins for

        Returns:
            List of allowed origins
        """
        env = environment or EnvironmentDetector.get_current_environment()

        if env == Environment.DEVELOPMENT:
            return [
                "http://localhost:3000",
                "http://localhost:4321",
                "http://localhost:8080",
                "http://127.0.0.1:3000",
                "http://127.0.0.1:4321",
                "http://127.0.0.1:8080",
            ]

        elif env == Environment.TESTING:
            return [
                "http://localhost:*",
                "http://127.0.0.1:*",
            ]

        elif env == Environment.STAGING:
            return [
                "https://staging.portfolio.com",
                "https://staging-portfolio.netlify.app",
                "https://staging-portfolio.vercel.app",
            ]

        else:  # Production
            return [
                "https://portfolio.com",
                "https://www.portfolio.com",
                "https://portfolio.netlify.app",
                "https://portfolio.vercel.app",
            ]

    @staticmethod
    def get_database_config() -> Dict[str, Any]:
        """
        Get environment-specific database configuration.

        Returns:
            Dictionary with database configuration
        """
        env = EnvironmentDetector.get_current_environment()
        runtime = EnvironmentDetector.get_current_runtime()

        config = {
            "pool_pre_ping": True,
            "pool_recycle": 300,
        }

        if runtime == Runtime.LAMBDA:
            # Lambda-optimized settings
            config.update({
                "pool_size": 1,
                "max_overflow": 0,
                "pool_timeout": 10,
            })
        elif env == Environment.DEVELOPMENT:
            config.update({
                "pool_size": 5,
                "max_overflow": 10,
                "pool_timeout": 30,
                "echo": True,
            })
        elif env == Environment.TESTING:
            config.update({
                "pool_size": 1,
                "max_overflow": 0,
                "pool_timeout": 5,
                "echo": False,
            })
        else:  # Staging/Production
            config.update({
                "pool_size": 3,
                "max_overflow": 5,
                "pool_timeout": 30,
                "echo": False,
            })

        return config


def require_environment(*allowed_environments: Environment) -> None:
    """
    Require that the current environment is one of the allowed environments.

    Args:
        allowed_environments: Allowed environment values

    Raises:
        RuntimeError: If current environment is not allowed
    """
    current_env = EnvironmentDetector.get_current_environment()
    if current_env not in allowed_environments:
        allowed_names = [env.value for env in allowed_environments]
        raise RuntimeError(
            f"This operation requires environment to be one of {allowed_names}, "
            f"but current environment is {current_env.value}"
        )


def require_local() -> None:
    """
    Require that the code is running locally.

    Raises:
        RuntimeError: If not running locally
    """
    if not EnvironmentDetector.is_local():
        raise RuntimeError("This operation can only be performed in local environment")


def require_lambda() -> None:
    """
    Require that the code is running in Lambda.

    Raises:
        RuntimeError: If not running in Lambda
    """
    if not EnvironmentDetector.is_lambda():
        raise RuntimeError("This operation can only be performed in Lambda environment")