"""
Información y categorización dinámica de servicios corriendo.
"""

import subprocess
import json
import re
from typing import Dict, List, Any, Tuple


def get_running_services() -> Dict[str, Dict[str, Any]]:
    """
    Obtiene información dinámica de los servicios que están corriendo.

    Returns:
        Dict: Diccionario con información de servicios activos
    """
    services = {}

    try:
        # Obtener información de contenedores corriendo
        result = subprocess.run(
            ["docker", "ps", "--format", "json"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    try:
                        container = json.loads(line)
                        name = container.get('Names', '')
                        ports = container.get('Ports', '')
                        status = container.get('Status', '')

                        # Extraer información del puerto
                        port_info = extract_port_info(ports)

                        # Categorizar servicio
                        service_info = categorize_service(name, port_info, status)
                        if service_info:
                            services[name] = service_info

                    except json.JSONDecodeError:
                        continue

    except subprocess.TimeoutExpired:
        pass
    except Exception:
        pass

    return services


def extract_port_info(ports_str: str) -> Dict[str, List[int]]:
    """
    Extrae información de puertos de la cadena de puertos de Docker.

    Args:
        ports_str: String con información de puertos

    Returns:
        Dict: Información de puertos extraída
    """
    port_info = {'external_ports': [], 'internal_ports': []}

    if not ports_str:
        return port_info

    # Patrón para extraer puertos: 0.0.0.0:8001->8080/tcp
    pattern = r'0\.0\.0\.0:(\d+)->(\d+)/'
    matches = re.findall(pattern, ports_str)

    for external, internal in matches:
        port_info['external_ports'].append(int(external))
        port_info['internal_ports'].append(int(internal))

    return port_info


def categorize_service(name: str, port_info: Dict[str, List[int]], status: str) -> Dict[str, Any]:
    """
    Categoriza un servicio según su nombre y configuración.

    Args:
        name: Nombre del contenedor
        port_info: Información de puertos
        status: Status del contenedor

    Returns:
        Dict: Información categorizada del servicio
    """
    if not port_info['external_ports']:
        return None

    primary_port = port_info['external_ports'][0]
    is_healthy = 'healthy' in status.lower()

    # Detectar tipo de servicio por nombre
    service_type = None
    icon = "🔧"
    service_name = name
    endpoints = []

    if 'website' in name.lower() or 'app' in name.lower():
        service_type = 'website'
        icon = "🎨"
        service_name = "Website (Astro v5)"
        endpoints = get_website_endpoints()
    elif 'gateway' in name.lower() or 'proxy' in name.lower():
        service_type = 'gateway'
        icon = "🚪"
        service_name = "API Gateway (Nginx)"
        endpoints = get_gateway_endpoints()
    elif 'personal-info' in name.lower():
        service_type = 'lambda'
        icon = "👤"
        service_name = "Personal Info Service"
        endpoints = get_fastapi_endpoints('personal-info')
    elif 'skills' in name.lower():
        service_type = 'lambda'
        icon = "🎯"
        service_name = "Skills Service"
        endpoints = get_fastapi_endpoints('skills')
    elif 'experience' in name.lower():
        service_type = 'lambda'
        icon = "💼"
        service_name = "Experience Service"
        endpoints = get_fastapi_endpoints('experience')
    elif 'projects' in name.lower():
        service_type = 'lambda'
        icon = "📂"
        service_name = "Projects Service"
        endpoints = get_fastapi_endpoints('projects')
    elif 'db' in name.lower() or 'postgres' in name.lower():
        service_type = 'database'
        icon = "🗄️"
        service_name = "PostgreSQL Database"
        endpoints = get_database_endpoints(primary_port)
    else:
        service_type = 'other'
        icon = "⚙️"
        service_name = name.replace('-', ' ').title()
        endpoints = [("GET", "/health", "Health check")]

    return {
        'type': service_type,
        'icon': icon,
        'name': service_name,
        'port': primary_port,
        'all_ports': port_info['external_ports'],
        'healthy': is_healthy,
        'endpoints': endpoints,
        'container_name': name
    }


def get_website_endpoints() -> List[Tuple[str, str, str]]:
    """
    Genera endpoints para el servicio website.

    Returns:
        List: Lista de tuplas (method, endpoint, description)
    """
    return [
        ("GET", "/", "Página principal del portfolio"),
        ("GET", "/about", "Página de información personal"),
        ("GET", "/experience", "Página de experiencia profesional"),
        ("GET", "/projects", "Página de portfolio de proyectos"),
        ("GET", "/skills", "Página de habilidades técnicas"),
        ("GET", "/contact", "Página de contacto"),
        ("GET", "/favicon.svg", "Favicon del sitio"),
        ("GET", "/*", "Todas las páginas estáticas")
    ]


def get_gateway_endpoints() -> List[Tuple[str, str, str]]:
    """
    Genera endpoints para el servicio gateway.

    Returns:
        List: Lista de tuplas (method, endpoint, description)
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


def get_fastapi_endpoints(service_name: str) -> List[Tuple[str, str, str]]:
    """
    Genera endpoints estándar para servicios FastAPI.

    Args:
        service_name: Nombre del servicio

    Returns:
        List: Lista de tuplas (method, endpoint, description)
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


def get_database_endpoints(port: int) -> List[Tuple[str, str, str]]:
    """
    Genera endpoints/comandos para el servicio de base de datos.

    Args:
        port: Puerto del servicio de base de datos

    Returns:
        List: Lista de tuplas (method, command/url, description)
    """
    return [
        ("CONNECT", f"postgresql://postgres:portfolio_password@localhost:{port}/portfolio_local", "Conexión directa"),
        ("CLI", f"psql -h localhost -p {port} -U postgres -d portfolio_local", "Cliente de línea de comandos"),
        ("GUI", "psql CLI / third-party tools", "Interfaz gráfica"),
        ("DOCKER", "docker exec -it portfolio-db psql -U postgres -d portfolio_local", "Conexión via Docker")
    ]


def categorize_services_by_type(services: Dict[str, Dict[str, Any]]) -> Dict[str, List[Tuple[str, Dict[str, Any]]]]:
    """
    Agrupa servicios por tipo para mostrar organizadamente.

    Args:
        services: Diccionario de servicios

    Returns:
        Dict: Servicios agrupados por tipo
    """
    service_types = {
        'website': [],
        'gateway': [],
        'lambda': [],
        'database': [],
        'other': []
    }

    for name, info in services.items():
        service_types[info['type']].append((name, info))

    return service_types


def get_service_health_summary(services: Dict[str, Dict[str, Any]]) -> Dict[str, int]:
    """
    Obtiene un resumen del estado de salud de servicios.

    Args:
        services: Diccionario de servicios

    Returns:
        Dict: Conteo de servicios por estado de salud
    """
    health_summary = {
        'healthy': 0,
        'unhealthy': 0,
        'unknown': 0,
        'total': len(services)
    }

    for name, info in services.items():
        if info['healthy']:
            health_summary['healthy'] += 1
        else:
            health_summary['unhealthy'] += 1

    health_summary['unknown'] = health_summary['total'] - health_summary['healthy'] - health_summary['unhealthy']

    return health_summary


def get_service_by_type(services: Dict[str, Dict[str, Any]], service_type: str) -> List[Dict[str, Any]]:
    """
    Filtra servicios por tipo específico.

    Args:
        services: Diccionario de servicios
        service_type: Tipo de servicio a filtrar

    Returns:
        List: Lista de servicios del tipo especificado
    """
    return [info for info in services.values() if info['type'] == service_type]


def get_service_ports_summary(services: Dict[str, Dict[str, Any]]) -> Dict[int, str]:
    """
    Obtiene un resumen de puertos utilizados por servicios.

    Args:
        services: Diccionario de servicios

    Returns:
        Dict: Mapeo de puerto a nombre de servicio
    """
    ports_summary = {}

    for name, info in services.items():
        for port in info['all_ports']:
            ports_summary[port] = info['name']

    return ports_summary


def validate_service_configuration(services: Dict[str, Dict[str, Any]]) -> Dict[str, List[str]]:
    """
    Valida la configuración de servicios detectados.

    Args:
        services: Diccionario de servicios

    Returns:
        Dict: Resultados de validación
    """
    validation = {
        'warnings': [],
        'recommendations': [],
        'conflicts': []
    }

    # Verificar conflictos de puertos
    port_usage = {}
    for name, info in services.items():
        for port in info['all_ports']:
            if port in port_usage:
                validation['conflicts'].append(
                    f"Puerto {port} usado por múltiples servicios: {port_usage[port]} y {info['name']}"
                )
            else:
                port_usage[port] = info['name']

    # Verificar servicios no saludables
    unhealthy_services = [info['name'] for info in services.values() if not info['healthy']]
    if unhealthy_services:
        validation['warnings'].append(
            f"Servicios no saludables: {', '.join(unhealthy_services)}"
        )

    # Recomendaciones basadas en servicios detectados
    service_types = {info['type'] for info in services.values()}

    if 'lambda' in service_types and 'gateway' not in service_types:
        validation['recommendations'].append(
            "Considera usar un API Gateway para consolidar microservicios Lambda"
        )

    if 'website' in service_types and 'gateway' in service_types:
        validation['recommendations'].append(
            "Configuración completa detectada: Website + API Gateway + Microservicios"
        )

    return validation