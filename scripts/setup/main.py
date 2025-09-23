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

# Imports de generación dinámica
from config_generator import ConfigGenerator
from docker_cleanup import DockerCleanupManager


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
        # Mostrar path relativo en lugar de absoluto
        relative_path = project_path.replace(os.path.expanduser("~"), "~")
        print(f"🏗️  Proyecto detectado en: {relative_path}")
        print(f"🌍 Entorno: {env}")
        print(f"⚡ Acción: {action}")

    # 1.5. Generación dinámica de configuraciones
    unified_port = get_unified_port_from_env(project_path, env)
    if action in ['up', 'restart', 'build']:
        generate_dynamic_configurations(project_path, unified_port, env, verbose)

    # Configurar limpieza automática para todas las acciones
    setup_automatic_cleanup(project_path, env, verbose)

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
        # 9. Limpieza de recursos temporales (silenciosa)
        if temp_dockerfiles:
            cleanup_temp_dockerfiles(temp_dockerfiles, False)  # Siempre silenciosa


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

    print(f"✅ 🐳 Docker disponible y funcionando")
    print(f"✅ Docker Compose v2 disponible")

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

    # Solo mostrar la configuración que se está usando con path relativo
    base_path = config_files.get('base', '')
    if project_path in base_path:
        relative_base_path = base_path.replace(project_path, '.')
    else:
        relative_base_path = base_path
    print(f"📁 Configuración Docker: {relative_base_path}")

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
            # Mostrar path relativo
            relative_env_path = env_files[env].replace(project_path, '.')
            print(f"📄 Variables de entorno: {relative_env_path}")
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


def get_unified_port_from_env(project_path: str, env: str) -> int:
    """
    Obtiene el puerto unificado desde el archivo .env correspondiente.

    Args:
        project_path: Ruta del proyecto
        env: Entorno (local, dev, test, etc.)

    Returns:
        int: Puerto unificado (default 4321)
    """
    env_files = find_env_files(project_path)
    unified_port = 4321  # Default

    if env in env_files:
        env_file = env_files[env]
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('UNIFIED_PORT='):
                        unified_port = int(line.split('=')[1].strip())
                        break
        except (FileNotFoundError, ValueError):
            pass

    return unified_port


def generate_dynamic_configurations(project_path: str, unified_port: int, env: str, verbose: bool):
    """
    Genera configuraciones dinámicas basadas en config.yml de servicios.

    Args:
        project_path: Ruta del proyecto
        unified_port: Puerto unificado
        env: Entorno
        verbose: Mostrar información detallada
    """
    if verbose:
        print(f"🔧 Generando configuraciones dinámicas para puerto {unified_port}...")

    try:
        # Inicializar generador de configuración
        generator = ConfigGenerator(project_path, unified_port)

        # Descubrir servicios
        services = generator.discover_services()
        if verbose:
            print(f"🔍 Servicios descubiertos: {len(services)}")

        # Generar configuraciones
        output_dir = os.path.join(project_path, "setup", "generated")
        files = generator.save_configurations(output_dir)

        if verbose:
            print(f"✅ Configuraciones generadas")

    except Exception as e:
        print(f"⚠️ Error generando configuraciones dinámicas: {e}")
        if verbose:
            import traceback
            traceback.print_exc()


def setup_automatic_cleanup(project_path: str, env: str, verbose: bool):
    """
    Configura limpieza automática de Docker al finalizar.

    Args:
        project_path: Ruta del proyecto
        env: Entorno
        verbose: Mostrar información detallada
    """
    try:
        cleanup_manager = DockerCleanupManager(project_path)
        cleanup_manager.register_exit_handler(env)

        if verbose:
            print(f"🔧 Limpieza automática configurada para entorno: {env}")

    except Exception as e:
        if verbose:
            print(f"⚠️ No se pudo configurar limpieza automática: {e}")