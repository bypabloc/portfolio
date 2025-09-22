"""
Gestión específica de servicios server (microservicios Lambda).
"""

from typing import List, Dict, Any
from pathlib import Path


def get_available_server_services() -> List[str]:
    """
    Obtiene la lista de microservicios server disponibles.

    Returns:
        List[str]: Lista de nombres de microservicios
    """
    return ['personal-info', 'skills', 'experience', 'projects']


def validate_server_services(server_services_list: List[str]) -> None:
    """
    Valida que los microservicios server especificados sean válidos.

    Args:
        server_services_list: Lista de microservicios server

    Raises:
        ValueError: Si algún microservicio no es válido
    """
    available_services = get_available_server_services()

    for service in server_services_list:
        if service not in available_services:
            raise ValueError(
                f"Lambda function inválida: {service}. "
                f"Valores válidos: {', '.join(available_services)}"
            )


def get_server_service_compose_names(server_services_list: List[str]) -> List[str]:
    """
    Convierte nombres de microservicios a nombres de servicios Docker Compose.

    Args:
        server_services_list: Lista de microservicios server

    Returns:
        List[str]: Lista de nombres de servicios Docker Compose
    """
    return [f'{service}-lambda' for service in server_services_list]


def get_server_service_ports() -> Dict[str, int]:
    """
    Obtiene el mapeo de microservicios a puertos.

    Returns:
        Dict[str, int]: Mapeo de microservicio a puerto
    """
    return {
        'personal-info': 8001,
        'skills': 8002,
        'experience': 8003,
        'projects': 8004
    }


def check_server_services_exist(project_path: str, server_services_list: List[str]) -> Dict[str, bool]:
    """
    Verifica que los directorios de microservicios existan en el proyecto.

    Args:
        project_path: Ruta del proyecto
        server_services_list: Lista de microservicios server

    Returns:
        Dict[str, bool]: Mapeo de microservicio a existencia
    """
    results = {}
    server_lambda_path = Path(project_path) / "server" / "lambda"

    for service in server_services_list:
        service_path = server_lambda_path / service
        results[service] = service_path.exists()

    return results


def get_server_service_endpoints(service_name: str) -> List[tuple]:
    """
    Obtiene los endpoints estándar para un microservicio específico.

    Args:
        service_name: Nombre del microservicio

    Returns:
        List[tuple]: Lista de (método, endpoint, descripción)
    """
    resource = service_name.replace('-', '_')

    endpoints = [
        ("GET", "/health", "Health check"),
        ("GET", "/docs", "FastAPI Swagger docs"),
        ("GET", "/redoc", "FastAPI ReDoc"),
        ("GET", f"/{resource}", f"Obtener {service_name}"),
        ("POST", f"/{resource}", f"Crear {service_name}"),
        ("GET", f"/{resource}/{{id}}", f"Obtener {service_name} específico"),
        ("PUT", f"/{resource}/{{id}}", f"Actualizar {service_name}"),
        ("DELETE", f"/{resource}/{{id}}", f"Eliminar {service_name}")
    ]

    return endpoints