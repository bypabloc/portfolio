"""
Gestión y verificación de puertos para servicios Docker.
"""

import sys
import os
import subprocess
from typing import List, Dict, Set, Optional

# Añadir src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def check_required_ports(services_list: List[str], verbose: bool = False) -> List[int]:
    """
    Verifica qué puertos están en uso que podrían causar conflictos.

    Args:
        services_list: Lista de servicios a verificar
        verbose: Mostrar información detallada

    Returns:
        List[int]: Lista de puertos en conflicto
    """
    from services.service_manager import get_required_ports_for_services

    ports_to_check = get_required_ports_for_services(services_list)
    conflicting_ports = []

    for port in ports_to_check:
        if is_port_in_use(port):
            conflicting_ports.append(port)
            if verbose:
                show_port_usage(port)

    return conflicting_ports


def is_port_in_use(port: int) -> bool:
    """
    Verifica si un puerto específico está en uso.

    Args:
        port: Puerto a verificar

    Returns:
        bool: True si el puerto está en uso
    """
    try:
        # Intentar con lsof primero (más preciso)
        result = subprocess.run(['lsof', f'-i:{port}'], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            return True
    except FileNotFoundError:
        # lsof no disponible, usar método alternativo
        pass

    try:
        # Intentar con netstat como fallback
        result = subprocess.run(['netstat', '-tulpn'], capture_output=True, text=True)
        if f":{port}" in result.stdout:
            return True
    except FileNotFoundError:
        # netstat no disponible, usar ss como último recurso
        pass

    try:
        # Intentar con ss (más moderno que netstat)
        result = subprocess.run(['ss', '-tulpn'], capture_output=True, text=True)
        if f":{port}" in result.stdout:
            return True
    except FileNotFoundError:
        pass

    return False


def show_port_usage(port: int) -> None:
    """
    Muestra información detallada sobre qué está usando un puerto.

    Args:
        port: Puerto a investigar
    """
    # No mostrar mensaje inicial duplicado, solo los detalles
    try:
        result = subprocess.run(['lsof', f'-i:{port}'], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            for line in lines[:3]:  # Show max 3 processes
                print(f"     {line}")
        else:
            # Fallback con netstat
            result = subprocess.run(['netstat', '-tulpn'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            for line in lines:
                if f":{port}" in line:
                    print(f"     {line.strip()}")
                    break
    except FileNotFoundError:
        print(f"     No se puede determinar qué proceso usa el puerto {port}")


def get_available_port_range(start_port: int, count: int = 10) -> List[int]:
    """
    Encuentra un rango de puertos disponibles consecutivos.

    Args:
        start_port: Puerto inicial para buscar
        count: Número de puertos consecutivos necesarios

    Returns:
        List[int]: Lista de puertos disponibles consecutivos
    """
    available_ports = []
    current_port = start_port

    while len(available_ports) < count:
        if not is_port_in_use(current_port):
            available_ports.append(current_port)
        else:
            # Si encontramos un puerto en uso, reiniciar la búsqueda
            available_ports = []

        current_port += 1

        # Evitar búsquedas infinitas
        if current_port > start_port + 1000:
            break

    return available_ports[:count] if len(available_ports) >= count else []


def suggest_alternative_ports(conflicting_ports: List[int]) -> Dict[int, int]:
    """
    Sugiere puertos alternativos para puertos en conflicto.

    Args:
        conflicting_ports: Lista de puertos en conflicto

    Returns:
        Dict[int, int]: Mapeo de puerto_conflictivo -> puerto_alternativo
    """
    suggestions = {}

    for port in conflicting_ports:
        # Buscar puerto alternativo en rangos cercanos
        alternative_ranges = [
            range(port + 100, port + 200),  # Mismo rango + 100
            range(port + 1000, port + 1100),  # Mismo rango + 1000
            range(port - 100, port) if port > 100 else range(port + 200, port + 300)
        ]

        for port_range in alternative_ranges:
            for alt_port in port_range:
                if not is_port_in_use(alt_port) and alt_port not in suggestions.values():
                    suggestions[port] = alt_port
                    break
            if port in suggestions:
                break

    return suggestions


def validate_port_configuration(services_config: Dict[str, Dict]) -> Dict[str, List[str]]:
    """
    Valida la configuración de puertos para detectar conflictos.

    Args:
        services_config: Configuración de servicios con puertos

    Returns:
        Dict[str, List[str]]: Resultados de validación
    """
    validation = {
        'errors': [],
        'warnings': [],
        'recommendations': []
    }

    used_ports = set()
    port_to_service = {}

    for service_name, config in services_config.items():
        port = config.get('port')
        if port:
            if port in used_ports:
                existing_service = port_to_service[port]
                validation['errors'].append(
                    f"Conflicto de puerto {port}: usado por {existing_service} y {service_name}"
                )
            else:
                used_ports.add(port)
                port_to_service[port] = service_name

            # Verificar si el puerto está en uso externamente
            if is_port_in_use(port):
                validation['warnings'].append(
                    f"Puerto {port} ({service_name}) está en uso por otro proceso"
                )

    # Recomendaciones generales
    if len(used_ports) > 0:
        min_port = min(used_ports)
        max_port = max(used_ports)

        if max_port - min_port > 1000:
            validation['recommendations'].append(
                "Los puertos están muy dispersos. Considerar agruparlos en un rango más compacto."
            )

        # Verificar si están en rangos apropiados
        privileged_ports = [p for p in used_ports if p < 1024]
        if privileged_ports:
            validation['warnings'].append(
                f"Puertos privilegiados en uso: {privileged_ports}. "
                "Pueden requerir permisos de administrador."
            )

    return validation


def generate_port_configuration_template() -> Dict[str, Dict[str, int]]:
    """
    Genera una configuración de puertos template para los servicios.

    Returns:
        Dict[str, Dict[str, int]]: Template de configuración de puertos
    """
    return {
        'website': {
            'port': 4321,
            'description': 'Astro v5 development server'
        },
        'api-gateway': {
            'port': 8090,
            'description': 'Nginx API Gateway (cambiado de 8080 para evitar conflictos)'
        },
        'personal-info-lambda': {
            'port': 8001,
            'description': 'Personal Info microservice'
        },
        'skills-lambda': {
            'port': 8002,
            'description': 'Skills microservice'
        },
        'experience-lambda': {
            'port': 8003,
            'description': 'Experience microservice'
        },
        'projects-lambda': {
            'port': 8004,
            'description': 'Projects microservice'
        },
        'postgres': {
            'port': 5432,
            'description': 'PostgreSQL database'
        }
    }


def check_system_port_limits() -> Dict[str, int]:
    """
    Verifica los límites de puertos del sistema.

    Returns:
        Dict[str, int]: Información sobre límites de puertos
    """
    limits = {
        'max_user_ports': 65535,
        'recommended_min': 1024,
        'recommended_max': 49151,
        'ephemeral_start': 32768
    }

    try:
        # Intentar obtener límites específicos del sistema
        with open('/proc/sys/net/ipv4/ip_local_port_range', 'r') as f:
            port_range = f.read().strip().split()
            if len(port_range) == 2:
                limits['ephemeral_start'] = int(port_range[0])
                limits['ephemeral_end'] = int(port_range[1])
    except:
        pass

    return limits