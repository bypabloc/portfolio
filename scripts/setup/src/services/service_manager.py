"""
Gestión general de servicios - Coordinador principal para todos los servicios.
"""

from typing import Dict, List, Any


def get_service_names_for_compose(services_list: List[str],
                                 server_services_list: List[str]) -> List[str]:
    """
    Convierte la lista de servicios lógicos a nombres de servicios Docker Compose.

    Args:
        services_list: Lista de servicios lógicos
        server_services_list: Lista de microservicios server

    Returns:
        List[str]: Nombres de servicios para Docker Compose
    """
    compose_services = []

    for service in services_list:
        if service == 'all':
            return []  # Docker Compose levantará todos por defecto
        elif service == 'app' or service == 'website':
            compose_services.append('portfolio-app')
        elif service == 'server':
            for server_service in server_services_list:
                compose_services.append(f'{server_service}-lambda')
        elif service == 'db':
            compose_services.append('portfolio-db')
        elif service == 'gateway':
            compose_services.append('api-gateway')

    return compose_services


def validate_services_configuration(services_list: List[str], server_services_list: List[str]) -> None:
    """
    Valida la configuración de servicios para detectar problemas antes de ejecutar.

    Args:
        services_list: Lista de servicios lógicos
        server_services_list: Lista de microservicios server

    Raises:
        ValueError: Si hay problemas en la configuración
    """
    # Si services incluye 'server', validar server_services
    if 'server' in services_list:
        if not server_services_list:
            raise ValueError(
                "Si especifica --services=\"server\", debe especificar "
                "--server-services con al menos un microservicio válido"
            )


def get_service_ports_mapping() -> Dict[str, List[int]]:
    """
    Obtiene el mapeo de servicios a puertos.

    Returns:
        Dict[str, List[int]]: Mapeo de servicios a puertos
    """
    return {
        'app': [4321],
        'website': [4321],
        'server': [8001, 8002, 8003, 8004],
        'gateway': [8080],
        'db': [5432]
    }


def get_required_ports_for_services(services_list: List[str]) -> List[int]:
    """
    Obtiene los puertos requeridos para una lista de servicios.

    Args:
        services_list: Lista de servicios

    Returns:
        List[int]: Lista de puertos requeridos
    """
    service_ports = get_service_ports_mapping()
    ports_to_check = set()

    if 'all' in services_list:
        for service_ports_list in service_ports.values():
            ports_to_check.update(service_ports_list)
    else:
        for service in services_list:
            if service in service_ports:
                ports_to_check.update(service_ports[service])

    return list(ports_to_check)