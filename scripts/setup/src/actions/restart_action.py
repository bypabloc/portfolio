"""
Lógica para la acción 'restart' - Reiniciar servicios Docker.
"""

import sys
import os
from typing import Dict, List, Any

# Añadir src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from docker.compose_utils import execute_docker_compose_command
from display.status_display import show_services_status


def execute_restart_action(cmd_parts: List[str], compose_services: List[str],
                          project_path: str, flags: Dict[str, Any]) -> int:
    """
    Ejecuta la acción 'restart' para reiniciar servicios.

    Args:
        cmd_parts: Comando base docker-compose
        compose_services: Servicios específicos de Docker Compose
        project_path: Ruta del proyecto
        flags: Flags procesadas

    Returns:
        int: Código de salida (0 = éxito)
    """

    verbose = flags.get('verbose', False)

    if verbose:
        print(f"🔄 Reiniciando servicios...")

    exit_code, stdout, stderr = execute_docker_compose_command(
        cmd_parts, 'restart', compose_services, project_path, verbose
    )

    if exit_code == 0:
        print("✅ Servicios reiniciados exitosamente")
        show_services_status(cmd_parts, project_path, verbose)
    else:
        print("❌ Error reiniciando servicios")
        if verbose:
            print(f"stderr: {stderr}")
        return exit_code

    return 0