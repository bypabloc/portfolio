#!/usr/bin/env python3
"""
Setup script principal refactorizado - Coordinador simple.

Este archivo coordina la ejecución de acciones delegando a módulos especializados.
La lógica específica está separada en src/ para mejor mantenimiento.

Funcionalidades:
- Gestión de entornos Docker (local, test, dev, prod)
- Orquestación de servicios (app, server, db, gateway)
- Acciones disponibles (up, down, restart, status, logs, clean)
"""

import sys
import os
from typing import Dict, Any

# Añadir src al path para imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Imports de configuración
from config.config_finder import detect_project_root, find_docker_config_files
from config.env_manager import find_env_files, set_env_for_compose
from config.port_manager import check_required_ports

# Imports de Docker
from docker.docker_utils import check_docker_available, check_docker_compose_available
from docker.compose_utils import build_docker_compose_command
from docker.dockerfile_manager import generate_temp_dockerfiles, cleanup_temp_dockerfiles

# Imports de servicios
from services.service_manager import get_service_names_for_compose, validate_services_configuration

# Imports de acciones
from actions.up_action import execute_up_action
from actions.down_action import execute_down_action
from actions.restart_action import execute_restart_action
from actions.status_action import execute_status_action
from actions.logs_action import execute_logs_action
from actions.clean_action import execute_clean_action


def main(flags: Dict[str, Any]) -> None:
    """
    Función principal coordinadora del script setup.

    Args:
        flags: Diccionario con las flags procesadas y validadas
    """
    # 1. Configuración inicial
    verbose = flags.get('verbose', False)
    project_path = flags.get('project_path') or detect_project_root()
    env = flags.get('env', 'local')
    action = flags.get('action', 'up')
    services_list = flags.get('services_list', ['all'])
    server_services_list = flags.get('server_services_list', [])

    if verbose:
        print(f"🏗️  Proyecto detectado en: {project_path}")
        print(f"🌍 Entorno: {env}")
        print(f"⚡ Acción: {action}")

    # 2. Verificaciones de pre-requisitos
    if not verify_docker_environment(verbose):
        sys.exit(2)

    if not verify_project_configuration(project_path, verbose):
        sys.exit(1)

    # 3. Configuración de entorno
    config_files = find_docker_config_files(project_path)
    setup_environment_variables(project_path, env, verbose)

    # 4. Validación de servicios
    validate_services_configuration(services_list, server_services_list)

    # 5. Verificación de puertos (solo para acción 'up')
    if action == 'up':
        check_port_conflicts(services_list, verbose)

    # 6. Preparación de comando Docker Compose
    compose_available, compose_cmd, compose_msg = check_docker_compose_available()
    cmd_parts = build_docker_compose_command(config_files, env, compose_cmd)
    compose_services = get_service_names_for_compose(services_list, server_services_list)

    # 7. Generación de Dockerfiles temporales (si es necesario)
    temp_dockerfiles = []
    if action in ['up', 'restart', 'build']:
        temp_dockerfiles = generate_temp_dockerfiles(project_path, verbose)

    try:
        # 8. Ejecución de la acción solicitada
        exit_code = execute_action(
            action, cmd_parts, compose_services, project_path, flags, temp_dockerfiles
        )

        if verbose:
            print(f"\n🎯 Operación '{action}' completada con código de salida: {exit_code}")

        sys.exit(exit_code)

    finally:
        # 9. Limpieza de recursos temporales
        if temp_dockerfiles:
            cleanup_temp_dockerfiles(temp_dockerfiles, verbose)


def verify_docker_environment(verbose: bool) -> bool:
    """
    Verifica que Docker esté disponible y configurado correctamente.

    Args:
        verbose: Mostrar información detallada

    Returns:
        bool: True si Docker está disponible
    """
    # Verificar Docker
    docker_available, docker_msg, platform_info = check_docker_available()
    if not docker_available:
        print(f"❌ {docker_msg}")

        # Mostrar instrucciones específicas por plataforma
        if platform_info.get('installation_instructions'):
            print("\n📋 Instrucciones de instalación:")
            for instruction in platform_info['installation_instructions']:
                print(f"   {instruction}")

        if platform_info.get('startup_instructions'):
            print("\n🚀 Para iniciar Docker:")
            for instruction in platform_info['startup_instructions']:
                print(f"   {instruction}")

        return False

    # Verificar Docker Compose
    compose_available, compose_cmd, compose_msg = check_docker_compose_available()
    if not compose_available:
        print(f"❌ {compose_msg}")
        print("Instale Docker Compose: https://docs.docker.com/compose/install/")
        return False

    if verbose:
        print(f"✅ {docker_msg}")
        print(f"✅ {compose_msg}")

    return True


def verify_project_configuration(project_path: str, verbose: bool) -> bool:
    """
    Verifica que la configuración del proyecto sea válida.

    Args:
        project_path: Ruta del proyecto
        verbose: Mostrar información detallada

    Returns:
        bool: True si la configuración es válida
    """
    config_files = find_docker_config_files(project_path)
    if not config_files:
        print("❌ No se encontró docker-compose.yml en el proyecto")
        print("Ubicaciones buscadas:")
        print("  - ./docker-compose.yml")
        print("  - ./docker/docker-compose.yml")
        print("  - ./setup/docker-compose.yml")
        return False

    if verbose:
        print(f"📁 Configuración Docker encontrada:")
        for env_name, file_path in config_files.items():
            print(f"  - {env_name}: {file_path}")

    return True


def setup_environment_variables(project_path: str, env: str, verbose: bool) -> None:
    """
    Configura las variables de entorno para el entorno especificado.

    Args:
        project_path: Ruta del proyecto
        env: Entorno objetivo
        verbose: Mostrar información detallada
    """
    env_files = find_env_files(project_path)
    if env in env_files:
        if verbose:
            print(f"📄 Variables de entorno: {env_files[env]}")
        set_env_for_compose(env_files[env])
    elif verbose:
        print(f"⚠️  No se encontró archivo .env para entorno {env}")


def check_port_conflicts(services_list: list, verbose: bool) -> None:
    """
    Verifica conflictos de puertos para los servicios solicitados.

    Args:
        services_list: Lista de servicios
        verbose: Mostrar información detallada
    """
    conflicting_ports = check_required_ports(services_list, verbose)
    if conflicting_ports:
        print("⚠️  Puertos en conflicto detectados:")
        for port in conflicting_ports:
            print(f"   - Puerto {port} está en uso")
        print("Los servicios pueden fallar al iniciar. Use --action=\"clean\" si es necesario.")


def execute_action(action: str, cmd_parts: list, compose_services: list,
                  project_path: str, flags: Dict[str, Any],
                  temp_dockerfiles: list) -> int:
    """
    Ejecuta la acción solicitada delegando a módulos especializados.

    Args:
        action: Acción a ejecutar
        cmd_parts: Comando base Docker Compose
        compose_services: Servicios Docker Compose
        project_path: Ruta del proyecto
        flags: Flags procesadas
        temp_dockerfiles: Lista de Dockerfiles temporales

    Returns:
        int: Código de salida
    """
    if action == 'up':
        return execute_up_action(cmd_parts, compose_services, project_path, flags, temp_dockerfiles)
    elif action == 'down':
        return execute_down_action(cmd_parts, project_path, flags)
    elif action == 'restart':
        return execute_restart_action(cmd_parts, compose_services, project_path, flags)
    elif action == 'status':
        return execute_status_action(cmd_parts, project_path, flags)
    elif action == 'logs':
        return execute_logs_action(cmd_parts, compose_services, project_path, flags)
    elif action == 'clean':
        return execute_clean_action(cmd_parts, project_path, flags)
    else:
        print(f"❌ Acción no reconocida: {action}")
        return 1