"""
Búsqueda y detección de archivos de configuración Docker y del proyecto.
"""

import os
from typing import Dict, Optional
from pathlib import Path


def detect_project_root(start_path: str = None) -> str:
    """
    Detecta la raíz del proyecto buscando docker-compose.yml o .git.

    Args:
        start_path: Ruta desde donde empezar la búsqueda

    Returns:
        str: Ruta de la raíz del proyecto
    """
    if start_path is None:
        start_path = os.getcwd()

    current_path = Path(start_path).resolve()

    # Buscar hacia arriba hasta encontrar docker-compose.yml, package.json o .git
    for parent in [current_path] + list(current_path.parents):
        docker_compose_paths = [
            parent / 'docker-compose.yml',
            parent / 'docker' / 'docker-compose.yml',
            parent / 'setup' / 'docker-compose.yml'
        ]

        for docker_path in docker_compose_paths:
            if docker_path.exists():
                return str(parent)

        if (parent / 'package.json').exists() or (parent / '.git').exists():
            return str(parent)

    # Si no se encuentra, usar directorio actual
    return str(current_path)


def find_docker_config_files(project_path: str) -> Dict[str, str]:
    """
    Busca archivos de configuración Docker en el proyecto.

    Args:
        project_path: Ruta del proyecto

    Returns:
        Dict[str, str]: Mapping de archivos encontrados
    """
    config_files = {}

    # Buscar docker-compose.yml en diferentes ubicaciones
    compose_locations = [
        Path(project_path) / 'docker-compose.yml',
        Path(project_path) / 'docker' / 'docker-compose.yml',
        Path(project_path) / 'setup' / 'docker-compose.yml'
    ]

    for location in compose_locations:
        if location.exists():
            config_files['base'] = str(location)
            docker_dir = location.parent
            break
    else:
        return {}  # No se encontró docker-compose.yml

    # Buscar archivos de override por entorno
    docker_dir = Path(config_files['base']).parent
    env_overrides = {
        'local': docker_dir / 'docker-compose.local.yml',
        'test': docker_dir / 'docker-compose.test.yml',
        'dev': docker_dir / 'docker-compose.dev.yml',
        'release': docker_dir / 'docker-compose.release.yml',
        'prod': docker_dir / 'docker-compose.prod.yml'
    }

    for env, override_path in env_overrides.items():
        if override_path.exists():
            config_files[env] = str(override_path)

    return config_files


def validate_docker_config_structure(project_path: str) -> Dict[str, bool]:
    """
    Valida que la estructura de configuración Docker sea correcta.

    Args:
        project_path: Ruta del proyecto

    Returns:
        Dict[str, bool]: Resultados de validación
    """
    results = {
        'base_compose_found': False,
        'docker_dir_found': False,
        'setup_dir_found': False,
        'has_env_overrides': False,
        'valid_structure': False
    }

    project_dir = Path(project_path)

    # Verificar estructura de directorios
    docker_dir = project_dir / 'docker'
    setup_dir = project_dir / 'setup'

    results['docker_dir_found'] = docker_dir.exists()
    results['setup_dir_found'] = setup_dir.exists()

    # Buscar docker-compose.yml base
    base_compose_locations = [
        project_dir / 'docker-compose.yml',
        docker_dir / 'docker-compose.yml',
        setup_dir / 'docker-compose.yml'
    ]

    for location in base_compose_locations:
        if location.exists():
            results['base_compose_found'] = True
            break

    # Verificar si hay archivos de override
    config_files = find_docker_config_files(project_path)
    env_overrides = [key for key in config_files.keys() if key != 'base']
    results['has_env_overrides'] = len(env_overrides) > 0

    # Determinar si la estructura es válida
    results['valid_structure'] = (
        results['base_compose_found'] and
        (results['docker_dir_found'] or results['setup_dir_found'])
    )

    return results


def get_docker_config_recommendations(project_path: str) -> Dict[str, str]:
    """
    Obtiene recomendaciones para mejorar la configuración Docker.

    Args:
        project_path: Ruta del proyecto

    Returns:
        Dict[str, str]: Recomendaciones por categoría
    """
    validation = validate_docker_config_structure(project_path)
    recommendations = {}

    if not validation['base_compose_found']:
        recommendations['base_compose'] = (
            "Crear docker-compose.yml base en una de estas ubicaciones: "
            "./docker-compose.yml, ./docker/docker-compose.yml, ./setup/docker-compose.yml"
        )

    if not validation['docker_dir_found'] and not validation['setup_dir_found']:
        recommendations['structure'] = (
            "Crear directorio 'docker/' o 'setup/' para organizar archivos de configuración"
        )

    if not validation['has_env_overrides']:
        recommendations['environments'] = (
            "Considerar crear archivos de override por entorno: "
            "docker-compose.local.yml, docker-compose.test.yml, docker-compose.prod.yml"
        )

    if validation['valid_structure']:
        recommendations['optimization'] = (
            "Estructura Docker válida. Considerar optimizaciones como: "
            "health checks, variables de entorno por archivo, profiles para servicios opcionales"
        )

    return recommendations