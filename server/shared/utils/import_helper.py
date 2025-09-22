"""
Simple import helper for Lambda services.

One-liner utility to setup shared imports for Lambda services.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/09/21
"""

import sys
from pathlib import Path


def setup_shared_imports(service_file: str = None) -> None:
    """
    One-liner to setup shared imports for Lambda services.

    Args:
        service_file: __file__ from calling service (if None, auto-detect)

    Usage:
        # At the top of any Lambda service main.py:
        from utils.import_helper import setup_shared_imports
        setup_shared_imports(__file__)

        # Now you can import shared modules normally:
        from api_core import create_fastapi_app
        from utils.logger import get_logger
    """
    if service_file is None:
        # Try to auto-detect from call stack
        import inspect
        frame = inspect.currentframe().f_back
        service_file = frame.f_globals['__file__']

    # Navigate to shared directory (standard Lambda service structure)
    current_file = Path(service_file).resolve()
    shared_dir = current_file.parents[3] / 'shared'  # src → service → lambda → server → shared

    # Add to Python path if not already present
    shared_str = str(shared_dir)
    if shared_str not in sys.path:
        sys.path.insert(0, shared_str)  # Insert at beginning for priority


# Even simpler: auto-setup when imported (for ultimate convenience)
def auto_setup_shared() -> None:
    """
    Automatically setup shared imports when this module is imported.

    This version detects the calling file automatically.
    """
    import inspect

    # Get the file that imported this module
    frame = inspect.currentframe()
    while frame:
        filename = frame.f_globals.get('__file__')
        if filename and 'import_helper' not in filename:
            setup_shared_imports(filename)
            break
        frame = frame.f_back


# For ultimate convenience - just import this and you're done
class SharedImporter:
    """Context manager style importer (optional advanced usage)."""

    def __init__(self, service_file: str):
        self.service_file = service_file
        self.added_paths = []

    def __enter__(self):
        setup_shared_imports(self.service_file)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Optionally clean up paths if needed
        pass


# Convenience function that can be copied to any service
def quick_setup(file_path: str) -> None:
    """
    Super simple one-liner for copy-paste convenience.

    Args:
        file_path: Just pass __file__ here

    Example:
        # Copy this to any Lambda service:
        from pathlib import Path
        import sys
        shared = Path(__file__).resolve().parents[3] / 'shared'
        sys.path.insert(0, str(shared))
    """
    shared = Path(file_path).resolve().parents[3] / 'shared'
    sys.path.insert(0, str(shared))