"""
Visualización de URLs disponibles y comandos de testing dinámicos.
"""

import subprocess
import json
from typing import Dict, List, Any, Tuple


def show_available_urls(verbose: bool = False):
    """
    Muestra las URLs principales del sistema de forma concisa.

    Args:
        verbose: Mostrar información detallada (para debug)
    """
    from .service_info import get_running_services

    print("\n" + "="*60)
    print("🌐 SISTEMA PORTFOLIO")
    print("="*60)

    # Obtener servicios corriendo dinámicamente
    services = get_running_services()

    if not services:
        print("\n❌ No se detectaron servicios corriendo")
        return

    # URLs principales
    print(f"\n🎨 Website:     http://localhost:4321")
    print(f"🚪 API Gateway: http://localhost:4321/api")

    # Información de base de datos
    db_service = None
    for name, info in services.items():
        if info.get('type') == 'database' or 'db' in name.lower() or 'postgres' in name.lower():
            db_service = info
            break

    if db_service:
        db_status = "✅" if db_service.get('healthy', False) else "🔄"
        db_port = db_service.get('port', 5432)
        print(f"🗄️  Database:    localhost:{db_port} {db_status}")
        if db_service.get('healthy', False):
            print(f"    └── Conexión: psql -h localhost -p {db_port} -U postgres -d portfolio_local")

    # Contar servicios operativos
    healthy_services = sum(1 for _, info in services.items() if info.get('healthy', False))
    total_services = len(services)

    print(f"\n✅ {healthy_services}/{total_services} servicios operativos")

    if verbose:
        print(f"\n📋 Servicios disponibles:")
        for name, info in services.items():
            status = "✅" if info.get('healthy', False) else "🔄"
            service_type = info.get('type', 'unknown')
            print(f"   {status} {name} ({service_type})")

    print("="*60)


def show_service_urls(service_info: Dict[str, Any], verbose: bool = False):
    """
    Muestra las URLs de un servicio específico.

    Args:
        service_info: Información del servicio
        verbose: Mostrar información detallada
    """
    icon = service_info['icon']
    name = service_info['name']
    port = service_info['port']
    healthy_status = "✅" if service_info['healthy'] else "⚠️"

    # Determinar base URL
    if service_info['type'] == 'database':
        base_url = f"localhost:{port}"
    else:
        base_url = f"http://localhost:{port}"

    print(f"\n{icon} {name} (Puerto {port}) {healthy_status}")
    print(f"└── {base_url}")

    # Mostrar endpoints
    for i, (method, endpoint, description) in enumerate(service_info['endpoints']):
        is_last = (i == len(service_info['endpoints']) - 1)
        prefix = "└──" if is_last else "├──"

        if service_info['type'] == 'database':
            print(f"    {prefix} {method:<8} {endpoint:<30} # {description}")
        else:
            full_endpoint = endpoint if endpoint.startswith('http') else endpoint
            print(f"    {prefix} {method:<6} {full_endpoint:<25} # {description}")

    # Mostrar puertos adicionales si hay
    if len(service_info['all_ports']) > 1:
        additional_ports = [p for p in service_info['all_ports'] if p != port]
        if additional_ports:
            print(f"    └── Puertos adicionales: {', '.join(map(str, additional_ports))}")


def show_dynamic_testing_commands(services: Dict[str, Dict[str, Any]]):
    """
    Muestra comandos de testing basados en servicios corriendo.

    Args:
        services: Diccionario de servicios activos
    """
    print(f"\n🧪 COMANDOS DE TESTING DINÁMICOS")

    # Health checks
    health_commands = []
    for name, info in services.items():
        if info['type'] in ['website', 'gateway', 'lambda']:
            if info['type'] == 'website':
                health_commands.append(f"curl http://localhost:{info['port']}")
            else:
                health_commands.append(f"curl http://localhost:{info['port']}/health")

    if health_commands:
        print("# Health checks rápidos")
        for cmd in health_commands:
            print(cmd)
        print()

    # FastAPI docs
    docs_commands = []
    for name, info in services.items():
        if info['type'] == 'lambda':
            docs_commands.append(f"http://localhost:{info['port']}/docs         # {info['name']} Swagger")

    if docs_commands:
        print("# FastAPI documentación interactiva")
        for cmd in docs_commands:
            print(cmd)


def show_consolidated_urls(services: Dict[str, Dict[str, Any]]):
    """
    Muestra URLs consolidadas del API Gateway si está disponible.

    Args:
        services: Diccionario de servicios activos
    """
    # Buscar API Gateway
    gateway_service = None
    for name, info in services.items():
        if info['type'] == 'gateway':
            gateway_service = info
            break

    if not gateway_service:
        return

    print(f"\n🌐 URLs CONSOLIDADAS (API Gateway - Puerto {gateway_service['port']})")
    print("-" * 60)

    gateway_port = gateway_service['port']
    consolidated_urls = {
        'health': f"http://localhost:{gateway_port}/health",
        'personal-info': f"http://localhost:{gateway_port}/api/personal-info",
        'skills': f"http://localhost:{gateway_port}/api/skills",
        'experience': f"http://localhost:{gateway_port}/api/experience",
        'projects': f"http://localhost:{gateway_port}/api/projects"
    }

    for service, url in consolidated_urls.items():
        print(f"  {service.title()}: {url}")


def detect_tech_stack(services: Dict[str, Dict[str, Any]]) -> List[str]:
    """
    Detecta tecnologías en uso basándose en servicios corriendo.

    Args:
        services: Diccionario de servicios activos

    Returns:
        List: Lista de strings describiendo el tech stack
    """
    tech_stack = []

    # Contar servicios por tipo
    website_count = sum(1 for s in services.values() if s['type'] == 'website')
    lambda_count = sum(1 for s in services.values() if s['type'] == 'lambda')
    gateway_count = sum(1 for s in services.values() if s['type'] == 'gateway')
    db_count = sum(1 for s in services.values() if s['type'] == 'database')

    if website_count > 0:
        tech_stack.append("🚀 Website: Astro v5 + TypeScript + Tailwind CSS")

    if lambda_count > 0:
        tech_stack.append(f"⚡ Server: {lambda_count} microservicios FastAPI + SQLModel")

    if db_count > 0:
        tech_stack.append("🗄️ Database: PostgreSQL 17 con branching")

    if gateway_count > 0:
        tech_stack.append("🌐 Gateway: Nginx reverse proxy consolidado")

    return tech_stack


def show_quick_access_commands(services: Dict[str, Dict[str, Any]]):
    """
    Muestra comandos de acceso rápido para servicios.

    Args:
        services: Diccionario de servicios activos
    """
    print(f"\n⚡ COMANDOS DE ACCESO RÁPIDO")
    print("-" * 30)

    quick_commands = []

    for name, info in services.items():
        if info['type'] == 'website':
            quick_commands.append(f"# Abrir website")
            quick_commands.append(f"open http://localhost:{info['port']}")

        elif info['type'] == 'gateway':
            quick_commands.append(f"# Health check del gateway")
            quick_commands.append(f"curl http://localhost:{info['port']}/health")

        elif info['type'] == 'lambda':
            service_name = name.replace('-lambda', '').replace('-', '_')
            quick_commands.append(f"# API {service_name}")
            quick_commands.append(f"curl http://localhost:{info['port']}/docs")

    # Mostrar solo los más importantes para no saturar
    for cmd in quick_commands[:8]:  # Limitar a 8 comandos
        print(cmd)


def show_service_discovery_info(services: Dict[str, Dict[str, Any]]):
    """
    Muestra información de service discovery para desarrollo.

    Args:
        services: Diccionario de servicios activos
    """
    print(f"\n🔍 SERVICE DISCOVERY")
    print("-" * 20)

    # Información para conectar servicios entre sí
    service_map = {}

    for name, info in services.items():
        if info['type'] in ['lambda', 'gateway', 'database']:
            service_map[info['type']] = {
                'name': name,
                'port': info['port'],
                'internal_url': f"http://{name}:{info['port']}" if info['type'] != 'database' else f"{name}:{info['port']}"
            }

    if service_map:
        print("# Para desarrollo interno (entre contenedores):")
        for service_type, info in service_map.items():
            print(f"  {service_type}: {info['internal_url']}")

        print("\n# Para desarrollo externo (desde host):")
        for service_type, info in service_map.items():
            external_url = f"http://localhost:{info['port']}" if service_type != 'database' else f"localhost:{info['port']}"
            print(f"  {service_type}: {external_url}")


def show_performance_urls(services: Dict[str, Dict[str, Any]]):
    """
    Muestra URLs específicas para testing de performance.

    Args:
        services: Diccionario de servicios activos
    """
    perf_urls = []

    for name, info in services.items():
        if info['type'] == 'lambda':
            # URLs de health check para performance testing
            perf_urls.append(f"http://localhost:{info['port']}/health")

        elif info['type'] == 'gateway':
            # URLs consolidadas para load testing
            perf_urls.extend([
                f"http://localhost:{info['port']}/api/personal-info",
                f"http://localhost:{info['port']}/api/skills",
                f"http://localhost:{info['port']}/api/experience",
                f"http://localhost:{info['port']}/api/projects"
            ])

    if perf_urls:
        print(f"\n⚡ URLs PARA PERFORMANCE TESTING")
        print("-" * 35)
        print("# Para usar con wrk, ab, o similares:")
        for url in perf_urls[:6]:  # Limitar para no saturar
            print(f"  {url}")

        print(f"\n# Ejemplo con curl para latencia:")
        print(f"  curl -w '@-' -o /dev/null -s {perf_urls[0]} <<< 'time_total: %{{time_total}}\\n'")


def show_logs_access_info(services: Dict[str, Dict[str, Any]]):
    """
    Muestra información sobre cómo acceder a logs de servicios.

    Args:
        services: Diccionario de servicios activos
    """
    print(f"\n📊 ACCESO A LOGS")
    print("-" * 15)

    log_commands = []

    for name, info in services.items():
        container_name = info.get('container_name', name)
        log_commands.append(f"docker logs {container_name}")
        log_commands.append(f"docker logs -f {container_name}  # Seguir en tiempo real")

    if log_commands:
        print("# Logs individuales:")
        for cmd in log_commands[:6]:  # Mostrar solo algunos ejemplos
            print(f"  {cmd}")

        print("\n# Logs consolidados:")
        print("  python scripts/run.py setup --action=logs --follow-logs")