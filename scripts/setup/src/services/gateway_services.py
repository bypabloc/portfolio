"""
Gestión específica de servicios gateway (API Gateway con Nginx).
"""

from typing import List, Dict, Any


def get_gateway_service_info() -> Dict[str, Any]:
    """
    Obtiene información del servicio gateway.

    Returns:
        Dict[str, Any]: Información del servicio gateway
    """
    return {
        'compose_name': 'api-gateway',
        'port': 8080,
        'type': 'gateway',
        'icon': '🚪',
        'name': 'API Gateway (Nginx)',
        'technology': 'Nginx reverse proxy consolidado'
    }


def get_gateway_endpoints() -> List[tuple]:
    """
    Obtiene los endpoints del API Gateway.

    Returns:
        List[tuple]: Lista de (método, endpoint, descripción)
    """
    return [
        ("GET", "/health", "Health check del gateway"),
        ("GET", "/api/personal-info", "Información personal (via gateway)"),
        ("GET", "/api/skills", "Habilidades técnicas (via gateway)"),
        ("GET", "/api/experience", "Experiencia profesional (via gateway)"),
        ("GET", "/api/projects", "Portfolio de proyectos (via gateway)"),
        ("POST", "/api/*", "Operaciones de escritura consolidadas"),
        ("PUT", "/api/*", "Operaciones de actualización consolidadas"),
        ("DELETE", "/api/*", "Operaciones de eliminación consolidadas")
    ]


def get_gateway_upstream_mapping() -> Dict[str, Dict[str, Any]]:
    """
    Obtiene el mapeo de upstreams para el gateway.

    Returns:
        Dict[str, Dict[str, Any]]: Mapeo de servicios a configuración upstream
    """
    return {
        'personal-info': {
            'service': 'personal-info-lambda',
            'port': 8080,
            'path': '/api/personal-info',
            'upstream_name': 'personal_info_server'
        },
        'skills': {
            'service': 'skills-lambda',
            'port': 8080,
            'path': '/api/skills',
            'upstream_name': 'skills_server'
        },
        'experience': {
            'service': 'experience-lambda',
            'port': 8080,
            'path': '/api/experience',
            'upstream_name': 'experience_server'
        },
        'projects': {
            'service': 'projects-lambda',
            'port': 8080,
            'path': '/api/projects',
            'upstream_name': 'projects_server'
        }
    }


def validate_gateway_configuration(project_path: str) -> Dict[str, bool]:
    """
    Valida que la configuración del gateway sea correcta.

    Args:
        project_path: Ruta del proyecto

    Returns:
        Dict[str, bool]: Resultados de validación
    """
    from pathlib import Path

    results = {}

    # Buscar archivos de configuración Nginx en diferentes ubicaciones
    nginx_locations = [
        Path(project_path) / "setup" / "nginx",
        Path(project_path) / "docker" / "nginx",
        Path(project_path) / "setup" / "proxy",
        Path(project_path) / "proxy"
    ]

    results['nginx_dir_found'] = False
    results['nginx_conf_found'] = False
    results['dockerfile_found'] = False

    for location in nginx_locations:
        if location.exists():
            results['nginx_dir_found'] = True

            # Buscar nginx.conf
            nginx_conf = location / "nginx.conf"
            if nginx_conf.exists():
                results['nginx_conf_found'] = True

            # Buscar Dockerfile
            dockerfile = location / "Dockerfile"
            if dockerfile.exists():
                results['dockerfile_found'] = True

            break

    return results


def get_gateway_health_check_url(port: int = 8080) -> str:
    """
    Obtiene la URL de health check del gateway.

    Args:
        port: Puerto del gateway

    Returns:
        str: URL de health check
    """
    return f"http://localhost:{port}/health"


def get_gateway_proxy_urls(port: int = 8080) -> Dict[str, str]:
    """
    Obtiene las URLs consolidadas del gateway para cada servicio.

    Args:
        port: Puerto del gateway

    Returns:
        Dict[str, str]: Mapeo de servicio a URL consolidada
    """
    base_url = f"http://localhost:{port}"

    return {
        'personal-info': f"{base_url}/api/personal-info",
        'skills': f"{base_url}/api/skills",
        'experience': f"{base_url}/api/experience",
        'projects': f"{base_url}/api/projects",
        'health': f"{base_url}/health"
    }