"""
Path setup utilities for Lambda services.

Common utilities for setting up Python path to find shared modules
in Lambda services architecture.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/21
"""

import sys
from pathlib import Path
from typing import Optional


def add_shared_to_path(service_file: str, levels_up: int = 3) -> Path:
    """
    Add shared directory to Python path for Lambda services.

    Args:
        service_file: __file__ from calling service (usually __file__)
        levels_up: Number of directory levels to go up to reach server/ (default: 3)
                  For services in /server/lambda/*/src/ structure

    Returns:
        Path to shared directory

    Example:
        # From /server/lambda/skills/src/main.py
        add_shared_to_path(__file__)
        # Navigates: src → skills → lambda → server, then to server/shared/
    """
    current_file = Path(service_file).resolve()

    # Navigate up the specified number of levels
    server_dir = current_file.parents[levels_up]
    shared_dir = server_dir / 'shared'

    # Add to Python path if not already present
    shared_str = str(shared_dir)
    if shared_str not in sys.path:
        sys.path.append(shared_str)

    return shared_dir


def add_project_root_to_path(service_file: str, levels_up: int = 4) -> Path:
    """
    Add project root directory to Python path.

    Args:
        service_file: __file__ from calling service
        levels_up: Number of directory levels to go up to reach project root

    Returns:
        Path to project root directory
    """
    current_file = Path(service_file).resolve()
    project_root = current_file.parents[levels_up]

    root_str = str(project_root)
    if root_str not in sys.path:
        sys.path.append(root_str)

    return project_root


def setup_lambda_paths(service_file: str) -> dict:
    """
    Setup all necessary paths for Lambda service development.

    Args:
        service_file: __file__ from calling service

    Returns:
        Dictionary with resolved paths

    Example:
        # From any Lambda service main.py
        paths = setup_lambda_paths(__file__)
        # Now can import from shared modules
    """
    current_file = Path(service_file).resolve()

    paths = {
        'current_file': current_file,
        'service_dir': current_file.parent,  # src/
        'lambda_service_dir': current_file.parent.parent,  # skills/
        'lambda_dir': current_file.parent.parent.parent,  # lambda/
        'server_dir': current_file.parent.parent.parent.parent,  # server/
        'shared_dir': None,
        'project_root': None
    }

    # Add shared directory
    shared_dir = paths['server_dir'] / 'shared'
    paths['shared_dir'] = shared_dir

    # Add project root
    project_root = paths['server_dir'].parent
    paths['project_root'] = project_root

    # Add both to Python path
    for path_key in ['shared_dir', 'project_root']:
        path_str = str(paths[path_key])
        if path_str not in sys.path:
            sys.path.append(path_str)

    return paths


def validate_shared_imports() -> bool:
    """
    Validate that shared modules can be imported.

    Returns:
        True if shared modules are accessible, False otherwise
    """
    try:
        # Try importing core shared modules
        import api_core
        import utils.logger
        return True
    except ImportError as e:
        print(f"Warning: Could not import shared modules: {e}")
        return False


# Convenience function for common Lambda service pattern
def setup_lambda_service_paths(service_file: str, validate: bool = True) -> Optional[dict]:
    """
    One-liner setup for Lambda services with validation.

    Args:
        service_file: __file__ from calling service
        validate: Whether to validate imports after setup

    Returns:
        Paths dictionary if successful, None if validation fails
    """
    paths = setup_lambda_paths(service_file)

    if validate and not validate_shared_imports():
        print(f"Failed to setup paths for service: {service_file}")
        return None

    return paths