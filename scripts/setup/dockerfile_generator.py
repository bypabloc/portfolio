"""
Dynamic Dockerfile generator for Lambda services.

Generates Dockerfiles on-demand with specific configurations per service
and environment, including eza CLI automatic installation system.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/21
:Modified:
    - 2025/09/21 - Added automatic eza installation system with template support
"""

from pathlib import Path


class LambdaDockerfileGenerator:
    """Generator for Lambda service Dockerfiles with automatic eza CLI installation."""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.server_dir = self.project_root / 'server'

    def generate_dockerfile_content(
        self,
        service_name: str,
        environment: str = "dev",
        include_tools: bool = True,
        extra_packages: list[str] | None = None,
        compose_context: bool = True
    ) -> str:
        """
        Generate Dockerfile content for a Lambda service using template.

        Args:
            service_name: Name of the Lambda service (skills, personal-info, etc.)
            environment: Environment type (dev, test, prod)
            include_tools: Whether to include tool auto-installation
            extra_packages: Additional system packages to install
            compose_context: Whether to use Docker Compose context (../server) or project root

        Returns:
            Complete Dockerfile content as string
        """
        if extra_packages is None:
            extra_packages = []

        # Load template - choose appropriate template based on context
        if compose_context:
            template_name = "dockerfile-lambda-compose.template"
        else:
            template_name = "dockerfile-lambda.template"

        template_path = self.project_root / "scripts" / "setup" / template_name
        try:
            template_content = template_path.read_text()
        except FileNotFoundError as err:
            raise FileNotFoundError(f"Template not found: {template_path}") from err

        # Development tools for dev environment
        development_tools = ""
        if environment == "dev":
            development_tools = """
# Install additional development tools for debugging and productivity
RUN pip install --no-cache-dir \\
    ipython \\
    ipdb \\
    rich \\
    typer"""

        # Development configuration for dev environment
        development_config = ""
        if environment == "dev":
            development_config = f"""
# Configure shell aliases and development environment for {service_name}
RUN echo 'alias python="python3"' >> /root/.bashrc && \\
    echo 'alias pip="pip3"' >> /root/.bashrc && \\
    echo 'export PS1="\\\\[\\\\033[1;36m\\\\][{service_name}-λ \\\\w]\\\\[\\\\033[1;32m\\\\] \\\\$ \\\\[\\\\033[0m\\\\]"' >> /root/.bashrc && \\
    echo 'echo "🚀 {service_name.title()} Lambda Development Container"' >> /root/.bashrc && \\
    echo 'echo "📂 Working Directory: $(pwd)"' >> /root/.bashrc && \\
    echo 'echo "🐍 Python: $(python --version)"' >> /root/.bashrc && \\
    echo 'echo "⚡ Lambda Development Container Ready"' >> /root/.bashrc"""

        # Template variables
        template_vars = {
            "service_name": service_name,
            "environment": environment,
            "log_level": self._get_log_level(environment),
            "debug_mode": str(environment == "dev").lower(),
            "development_tools": development_tools,
            "development_config": development_config,
        }

        # Format template with variables
        return template_content.format(**template_vars)

    def _get_log_level(self, environment: str) -> str:
        """Get appropriate log level for environment."""
        log_levels = {
            "dev": "debug",
            "test": "info",
            "prod": "warning",
            "staging": "info"
        }
        return log_levels.get(environment, "info")

    def create_dockerfile(
        self,
        service_name: str,
        environment: str = "dev",
        include_tools: bool = True,
        extra_packages: list[str] | None = None,
        compose_context: bool = True
    ) -> Path:
        """
        Create a temporary Dockerfile for a Lambda service.

        Args:
            service_name: Name of the Lambda service
            environment: Environment type
            include_tools: Whether to include tool installation
            extra_packages: Additional packages
            compose_context: Whether to use Docker Compose context

        Returns:
            Path to the created Dockerfile
        """
        service_dir = self.server_dir / "lambda" / service_name
        dockerfile_path = service_dir / f"Dockerfile.{environment}"

        # Generate content
        content = self.generate_dockerfile_content(
            service_name=service_name,
            environment=environment,
            include_tools=include_tools,
            extra_packages=extra_packages,
            compose_context=compose_context
        )

        # Write to file
        dockerfile_path.write_text(content)

        print(f"✅ Generated Dockerfile: {dockerfile_path}")
        return dockerfile_path

    def cleanup_dockerfile(self, service_name: str, environment: str = "dev") -> bool:
        """
        Remove temporary Dockerfile after use.

        Args:
            service_name: Name of the Lambda service
            environment: Environment type

        Returns:
            True if file was removed, False if not found
        """
        service_dir = self.server_dir / "lambda" / service_name
        dockerfile_path = service_dir / f"Dockerfile.{environment}"

        if dockerfile_path.exists():
            dockerfile_path.unlink()
            print(f"🧹 Cleaned up Dockerfile: {dockerfile_path}")
            return True

        return False

    def cleanup_all_dockerfiles(self, environment: str = "dev") -> int:
        """
        Remove all temporary Dockerfiles for an environment.

        Args:
            environment: Environment type

        Returns:
            Number of files cleaned up
        """
        lambda_dir = self.server_dir / "lambda"
        pattern = f"Dockerfile.{environment}"
        cleaned = 0

        for service_dir in lambda_dir.iterdir():
            if service_dir.is_dir():
                dockerfile_path = service_dir / pattern
                if dockerfile_path.exists():
                    dockerfile_path.unlink()
                    print(f"🧹 Cleaned up: {dockerfile_path}")
                    cleaned += 1

        print(f"🧹 Total Dockerfiles cleaned: {cleaned}")
        return cleaned


# Convenience functions for script usage
def generate_lambda_dockerfile(
    project_root: str,
    service_name: str,
    environment: str = "dev",
    include_tools: bool = True
) -> Path:
    """Generate a Lambda service Dockerfile."""
    generator = LambdaDockerfileGenerator(project_root)
    return generator.create_dockerfile(
        service_name=service_name,
        environment=environment,
        include_tools=include_tools
    )


def cleanup_lambda_dockerfile(
    project_root: str,
    service_name: str,
    environment: str = "dev"
) -> bool:
    """Clean up a Lambda service Dockerfile."""
    generator = LambdaDockerfileGenerator(project_root)
    return generator.cleanup_dockerfile(service_name, environment)


def cleanup_all_lambda_dockerfiles(
    project_root: str,
    environment: str = "dev"
) -> int:
    """Clean up all Lambda service Dockerfiles."""
    generator = LambdaDockerfileGenerator(project_root)
    return generator.cleanup_all_dockerfiles(environment)
