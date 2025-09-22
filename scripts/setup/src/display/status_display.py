"""
Visualización del estado de servicios Docker y información del sistema.
"""

import sys
import os
import subprocess
from typing import List, Dict, Any

# Añadir src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def show_services_status(cmd_parts: List[str], project_path: str, verbose: bool) -> None:
    """
    Muestra el estado actual de los servicios.

    Args:
        cmd_parts: Comando base docker-compose
        project_path: Ruta del proyecto
        verbose: Mostrar información detallada
    """
    print("📊 Estado de servicios Docker:")
    print("-" * 50)

    # Obtener estado de servicios
    cmd = cmd_parts + ['ps', '--format', 'table']
    result = subprocess.run(cmd, cwd=project_path, capture_output=True, text=True)

    if result.returncode == 0:
        print(result.stdout)
    else:
        print("❌ Error obteniendo estado de servicios")
        if verbose:
            print(f"Error: {result.stderr}")

    # Mostrar uso de puertos si verbose
    if verbose:
        show_port_mappings(cmd_parts, project_path)


def show_port_mappings(cmd_parts: List[str], project_path: str) -> None:
    """
    Muestra los mapeos de puertos de los servicios.

    Args:
        cmd_parts: Comando base docker-compose
        project_path: Ruta del proyecto
    """
    from docker.compose_utils import get_compose_port_mappings

    print("\n🔌 Puertos expuestos:")
    port_mappings = get_compose_port_mappings(cmd_parts, project_path)

    if port_mappings:
        for service, ports in port_mappings.items():
            print(f"  {service}:")
            for port in ports:
                print(f"    - {port}")
    else:
        print("No hay puertos expuestos o servicios no están corriendo")


def show_services_summary(services_status: Dict[str, Dict[str, Any]]) -> None:
    """
    Muestra un resumen del estado de servicios.

    Args:
        services_status: Estado de servicios obtenido de Docker Compose
    """
    if not services_status:
        print("❌ No se detectaron servicios")
        return

    print(f"\n📈 Resumen de servicios ({len(services_status)} servicios):")
    print("-" * 40)

    # Contar servicios por estado
    states = {}
    health_status = {}

    for service_name, info in services_status.items():
        state = info.get('state', 'unknown')
        health = info.get('health', '')

        states[state] = states.get(state, 0) + 1

        if health:
            health_status[health] = health_status.get(health, 0) + 1

    # Mostrar conteo por estado
    for state, count in states.items():
        icon = get_state_icon(state)
        print(f"  {icon} {state.title()}: {count} servicios")

    # Mostrar conteo por health status si hay información
    if health_status:
        print("\n🏥 Health Status:")
        for health, count in health_status.items():
            icon = get_health_icon(health)
            print(f"  {icon} {health.title()}: {count} servicios")


def show_detailed_service_info(service_name: str, service_info: Dict[str, Any]) -> None:
    """
    Muestra información detallada de un servicio específico.

    Args:
        service_name: Nombre del servicio
        service_info: Información del servicio
    """
    state = service_info.get('state', 'unknown')
    health = service_info.get('health', '')
    image = service_info.get('image', '')
    ports = service_info.get('ports', [])

    state_icon = get_state_icon(state)
    health_icon = get_health_icon(health) if health else ""

    print(f"\n{state_icon} {service_name}")
    print(f"  Estado: {state} {health_icon}")

    if image:
        print(f"  Imagen: {image}")

    if ports:
        print(f"  Puertos: {', '.join(str(p) for p in ports)}")


def get_state_icon(state: str) -> str:
    """
    Obtiene el icono apropiado para un estado de servicio.

    Args:
        state: Estado del servicio

    Returns:
        str: Icono del estado
    """
    icons = {
        'running': '✅',
        'exited': '❌',
        'created': '🔵',
        'restarting': '🔄',
        'removing': '🗑️',
        'paused': '⏸️',
        'dead': '💀'
    }

    return icons.get(state.lower(), '❓')


def get_health_icon(health: str) -> str:
    """
    Obtiene el icono apropiado para un estado de salud.

    Args:
        health: Estado de salud del servicio

    Returns:
        str: Icono del estado de salud
    """
    icons = {
        'healthy': '💚',
        'unhealthy': '❤️',
        'starting': '🟡',
        'none': ''
    }

    return icons.get(health.lower(), '❓')


def show_system_resources() -> None:
    """
    Muestra información sobre recursos del sistema Docker.
    """
    print("\n💻 Recursos del sistema:")
    print("-" * 30)

    try:
        # Obtener información del sistema Docker
        result = subprocess.run(['docker', 'system', 'df'], capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("❌ No se pudo obtener información de recursos")

    except FileNotFoundError:
        print("❌ Docker no está disponible")


def show_docker_info_summary() -> None:
    """
    Muestra un resumen de la información de Docker.
    """
    try:
        result = subprocess.run(['docker', 'info', '--format', '{{json .}}'],
                              capture_output=True, text=True)

        if result.returncode == 0:
            import json
            docker_info = json.loads(result.stdout)

            print("\n🐳 Información de Docker:")
            print("-" * 25)
            print(f"  Versión: {docker_info.get('ServerVersion', 'Desconocida')}")
            print(f"  Contenedores: {docker_info.get('Containers', 0)}")
            print(f"  Imágenes: {docker_info.get('Images', 0)}")

            # Información de memoria si está disponible
            mem_total = docker_info.get('MemTotal', 0)
            if mem_total:
                mem_gb = round(mem_total / (1024**3), 1)
                print(f"  Memoria total: {mem_gb} GB")

    except (FileNotFoundError, json.JSONDecodeError):
        print("❌ No se pudo obtener información de Docker")


def show_troubleshooting_hints(services_status: Dict[str, Dict[str, Any]]) -> None:
    """
    Muestra hints de troubleshooting basados en el estado de servicios.

    Args:
        services_status: Estado actual de servicios
    """
    issues = []

    for service_name, info in services_status.items():
        state = info.get('state', 'unknown')
        health = info.get('health', '')

        if state == 'exited':
            issues.append(f"🔧 {service_name} se detuvo - revisar logs: docker-compose logs {service_name}")

        if health == 'unhealthy':
            issues.append(f"🏥 {service_name} no está healthy - verificar configuración de health check")

        if state == 'restarting':
            issues.append(f"🔄 {service_name} está reiniciando constantemente - posible problema de configuración")

    if issues:
        print("\n🔧 Sugerencias de troubleshooting:")
        print("-" * 35)
        for issue in issues:
            print(f"  {issue}")
    else:
        print("\n✅ Todos los servicios parecen estar funcionando correctamente")