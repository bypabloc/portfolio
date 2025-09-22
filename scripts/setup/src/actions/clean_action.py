"""
Lógica para la acción 'clean' - Limpiar recursos Docker.
"""

import sys
import os
from typing import Dict, List, Any

# Añadir src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from docker.compose_utils import execute_docker_compose_command
from docker.docker_utils import clean_docker_resources


def execute_clean_action(cmd_parts: List[str], project_path: str, flags: Dict[str, Any]) -> int:
    """
    Ejecuta la acción 'clean' para limpiar recursos Docker.

    Args:
        cmd_parts: Comando base docker-compose
        project_path: Ruta del proyecto
        flags: Flags procesadas

    Returns:
        int: Código de salida (0 = éxito)
    """

    verbose = flags.get('verbose', False)

    # Primero bajar servicios
    print("🛑 Bajando servicios antes de limpiar...")
    execute_docker_compose_command(cmd_parts, 'down', [], project_path, verbose,
                                 ['--remove-orphans', '--volumes'])

    # Limpiar recursos Docker
    clean_docker_resources(project_path, verbose)

    return 0