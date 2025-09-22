"""
Lógica para la acción 'down' - Bajar servicios Docker.
"""

import sys
import os
from typing import Dict, List, Any

# Añadir src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from docker.compose_utils import execute_docker_compose_command


def execute_down_action(cmd_parts: List[str], project_path: str, flags: Dict[str, Any]) -> int:
    """
    Ejecuta la acción 'down' para bajar servicios.

    Args:
        cmd_parts: Comando base docker-compose
        project_path: Ruta del proyecto
        flags: Flags procesadas

    Returns:
        int: Código de salida (0 = éxito)
    """

    verbose = flags.get('verbose', False)

    if verbose:
        print(f"⬇️  Bajando servicios...")

    exit_code, stdout, stderr = execute_docker_compose_command(
        cmd_parts, 'down', [], project_path, verbose, ['--remove-orphans']
    )

    if exit_code == 0:
        print("✅ Servicios bajados exitosamente")
    else:
        print("❌ Error bajando servicios")
        if verbose:
            print(f"stderr: {stderr}")
        return exit_code

    return 0