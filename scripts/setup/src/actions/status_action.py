"""
Lógica para la acción 'status' - Mostrar estado de servicios Docker.
"""

import sys
import os
from typing import Dict, List, Any

# Añadir src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from display.status_display import show_services_status


def execute_status_action(cmd_parts: List[str], project_path: str, flags: Dict[str, Any]) -> int:
    """
    Ejecuta la acción 'status' para mostrar estado de servicios.

    Args:
        cmd_parts: Comando base docker-compose
        project_path: Ruta del proyecto
        flags: Flags procesadas

    Returns:
        int: Código de salida (0 = éxito)
    """
    verbose = flags.get('verbose', False)

    show_services_status(cmd_parts, project_path, verbose)

    return 0