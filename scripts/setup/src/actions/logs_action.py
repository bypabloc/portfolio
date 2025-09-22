"""
Lógica para la acción 'logs' - Mostrar logs de servicios Docker.
"""

import sys
import os
from typing import Dict, List, Any

# Añadir src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from docker.compose_utils import follow_services_logs


def execute_logs_action(cmd_parts: List[str], compose_services: List[str],
                       project_path: str, flags: Dict[str, Any]) -> int:
    """
    Ejecuta la acción 'logs' para mostrar logs de servicios.

    Args:
        cmd_parts: Comando base docker-compose
        compose_services: Servicios específicos de Docker Compose
        project_path: Ruta del proyecto
        flags: Flags procesadas

    Returns:
        int: Código de salida (0 = éxito)
    """
    verbose = flags.get('verbose', False)

    follow_services_logs(cmd_parts, compose_services, project_path, verbose)

    return 0