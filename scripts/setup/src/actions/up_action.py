"""
Lógica para la acción 'up' - Levantar servicios Docker.
"""

import sys
import os
import subprocess
from typing import Dict, List, Any, Tuple

# Añadir src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from docker.compose_utils import execute_docker_compose_command, wait_for_services_health, follow_services_logs
from display.status_display import show_services_status
from display.url_display import show_available_urls
from localstack.localstack_manager import setup_localstack_api_gateway


def execute_up_action(cmd_parts: List[str], compose_services: List[str],
                     project_path: str, flags: Dict[str, Any],
                     temp_dockerfiles: List[str]) -> int:
    """
    Ejecuta la acción 'up' para levantar servicios.

    Args:
        cmd_parts: Comando base docker-compose
        compose_services: Servicios específicos de Docker Compose
        project_path: Ruta del proyecto
        flags: Flags procesadas
        temp_dockerfiles: Lista de Dockerfiles temporales generados

    Returns:
        int: Código de salida (0 = éxito)
    """

    verbose = flags.get('verbose', False)
    build = flags.get('build', False)
    detach = flags.get('detach', True)
    follow_logs = flags.get('follow_logs', False)
    services_list = flags.get('services_list', ['all'])

    additional_args = []
    if build:
        additional_args.append('--build')
    if detach:
        additional_args.append('-d')

    if verbose:
        print(f"🚀 Levantando servicios...")

    exit_code, stdout, stderr = execute_docker_compose_command(
        cmd_parts, 'up', compose_services, project_path, verbose, additional_args
    )

    if exit_code == 0:
        print("✅ Servicios levantados exitosamente")

        if detach:
            # Esperar a que servicios estén healthy
            if wait_for_services_health(cmd_parts, compose_services, project_path, 60, verbose):
                print("🎉 Todos los servicios están operativos")

                # Configurar LocalStack API Gateway solo si está realmente corriendo
                localstack_running = _check_localstack_running()

                if localstack_running and (_is_localstack_service_requested(compose_services, services_list)):
                    if verbose:
                        print("\n🌐 Configurando LocalStack API Gateway...")

                    if setup_localstack_api_gateway(project_path, verbose):
                        print("✅ LocalStack API Gateway configurado exitosamente")
                    else:
                        print("⚠️  LocalStack API Gateway no pudo ser configurado completamente")
                elif verbose and 'all' in services_list:
                    print("ℹ️  LocalStack no está habilitado - saltando configuración")
            else:
                print("⚠️  Algunos servicios pueden no estar completamente listos")

            # Mostrar estado
            show_services_status(cmd_parts, project_path, verbose)

            # Mostrar URLs disponibles del sistema
            show_available_urls(verbose)

            # Seguir logs si se solicitó
            if follow_logs:
                follow_services_logs(cmd_parts, compose_services, project_path, verbose)
    else:
        print("❌ Error levantando servicios")
        if verbose:
            print(f"stdout: {stdout}")
            print(f"stderr: {stderr}")
        return exit_code

    return 0


def _check_localstack_running() -> bool:
    """
    Verifica si LocalStack está corriendo.

    Returns:
        bool: True si LocalStack está corriendo
    """
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}", "--filter", "name=localstack"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return "localstack" in result.stdout
    except:
        return False


def _is_localstack_service_requested(compose_services: List[str], services_list: List[str]) -> bool:
    """
    Verifica si LocalStack fue solicitado en los servicios.

    Args:
        compose_services: Servicios de Docker Compose
        services_list: Lista de servicios solicitados

    Returns:
        bool: True si LocalStack fue solicitado
    """
    return ('localstack' in [s.lower() for s in compose_services] or 'all' in services_list)