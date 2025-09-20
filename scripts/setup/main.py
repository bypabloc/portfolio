#!/usr/bin/env python3

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Añadir utils al path para usar las utilidades
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.flags_to_dict import flags_to_dict


def detect_project_root(start_path: str = None) -> str:
    """
    Detecta la raíz del proyecto buscando docker-compose.yml o .git.

    Args:
        start_path: Ruta desde donde empezar la búsqueda

    Returns:
        str: Ruta de la raíz del proyecto
    """
    if start_path is None:
        start_path = os.getcwd()

    current_path = Path(start_path).resolve()

    # Buscar hacia arriba hasta encontrar docker-compose.yml, package.json o .git
    for parent in [current_path] + list(current_path.parents):
        docker_compose_paths = [
            parent / 'docker-compose.yml',
            parent / 'docker' / 'docker-compose.yml'
        ]

        for docker_path in docker_compose_paths:
            if docker_path.exists():
                return str(parent)

        if (parent / 'package.json').exists() or (parent / '.git').exists():
            return str(parent)

    # Si no se encuentra, usar directorio actual
    return str(current_path)


def check_docker_available() -> Tuple[bool, str]:
    """
    Verifica si Docker está disponible y corriendo.

    Returns:
        Tuple[bool, str]: (disponible, mensaje)
    """
    try:
        # Verificar que docker comando existe
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            return False, "Docker no está instalado"

        # Verificar que docker daemon está corriendo
        result = subprocess.run(['docker', 'info'], capture_output=True, text=True)
        if result.returncode != 0:
            return False, "Docker daemon no está corriendo"

        return True, "Docker disponible"

    except FileNotFoundError:
        return False, "Docker no está instalado"
    except Exception as e:
        return False, f"Error verificando Docker: {e}"


def check_docker_compose_available() -> Tuple[bool, str, str]:
    """
    Verifica si Docker Compose está disponible.

    Returns:
        Tuple[bool, str, str]: (disponible, comando, mensaje)
    """
    # Intentar docker compose (v2) primero
    try:
        result = subprocess.run(['docker', 'compose', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            return True, 'docker compose', "Docker Compose v2 disponible"
    except:
        pass

    # Intentar docker-compose (v1) como fallback
    try:
        result = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            return True, 'docker-compose', "Docker Compose v1 disponible"
    except:
        pass

    return False, '', "Docker Compose no está disponible"


def find_docker_config_files(project_path: str) -> Dict[str, str]:
    """
    Busca archivos de configuración Docker en el proyecto.

    Args:
        project_path: Ruta del proyecto

    Returns:
        Dict[str, str]: Mapping de archivos encontrados
    """
    config_files = {}

    # Buscar docker-compose.yml en diferentes ubicaciones
    compose_locations = [
        Path(project_path) / 'docker-compose.yml',
        Path(project_path) / 'docker' / 'docker-compose.yml'
    ]

    for location in compose_locations:
        if location.exists():
            config_files['base'] = str(location)
            docker_dir = location.parent
            break
    else:
        return {}  # No se encontró docker-compose.yml

    # Buscar archivos de override por entorno
    docker_dir = Path(config_files['base']).parent
    env_overrides = {
        'local': docker_dir / 'docker-compose.local.yml',
        'test': docker_dir / 'docker-compose.test.yml',
        'dev': docker_dir / 'docker-compose.dev.yml',
        'prod': docker_dir / 'docker-compose.prod.yml'
    }

    for env, override_path in env_overrides.items():
        if override_path.exists():
            config_files[env] = str(override_path)

    return config_files


def find_env_files(project_path: str) -> Dict[str, str]:
    """
    Busca archivos .env por entorno.

    Args:
        project_path: Ruta del proyecto

    Returns:
        Dict[str, str]: Mapping de archivos .env encontrados
    """
    env_files = {}
    project_dir = Path(project_path)

    env_file_names = {
        'local': ['.env.local', '.env.development'],
        'test': ['.env.test', '.env.testing'],
        'dev': ['.env.dev', '.env.development'],
        'prod': ['.env.prod', '.env.production']
    }

    for env, possible_names in env_file_names.items():
        for name in possible_names:
            env_file_path = project_dir / name
            if env_file_path.exists():
                env_files[env] = str(env_file_path)
                break

    return env_files


def check_required_ports(services_list: List[str], verbose: bool = False) -> List[int]:
    """
    Verifica qué puertos están en uso que podrían causar conflictos.

    Args:
        services_list: Lista de servicios a verificar
        verbose: Mostrar información detallada

    Returns:
        List[int]: Lista de puertos en conflicto
    """
    # Mapeo de servicios a puertos
    service_ports = {
        'frontend': [4321],
        'backend': [8001, 8002, 8003, 8004],
        'gateway': [8080],
        'db': [5432]
    }

    ports_to_check = set()

    if 'all' in services_list:
        for service_ports_list in service_ports.values():
            ports_to_check.update(service_ports_list)
    else:
        for service in services_list:
            if service in service_ports:
                ports_to_check.update(service_ports[service])

    conflicting_ports = []

    for port in ports_to_check:
        try:
            result = subprocess.run(['lsof', f'-i:{port}'], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                conflicting_ports.append(port)
                if verbose:
                    print(f"⚠️  Puerto {port} está en uso:")
                    lines = result.stdout.strip().split('\n')[1:]  # Skip header
                    for line in lines[:3]:  # Show max 3 processes
                        print(f"     {line}")
        except FileNotFoundError:
            # lsof no disponible, usar método alternativo
            try:
                result = subprocess.run(['netstat', '-tulpn'], capture_output=True, text=True)
                if f":{port}" in result.stdout:
                    conflicting_ports.append(port)
            except:
                pass  # No podemos verificar puertos

    return conflicting_ports


def build_docker_compose_command(config_files: Dict[str, str], env: str,
                                compose_cmd: str) -> List[str]:
    """
    Construye el comando docker-compose con archivos de configuración.

    Args:
        config_files: Archivos de configuración encontrados
        env: Entorno objetivo
        compose_cmd: Comando docker-compose a usar

    Returns:
        List[str]: Comando completo como lista
    """
    cmd_parts = compose_cmd.split()

    # Agregar archivo base
    if 'base' in config_files:
        cmd_parts.extend(['-f', config_files['base']])

    # Agregar override del entorno si existe
    if env in config_files:
        cmd_parts.extend(['-f', config_files[env]])

    return cmd_parts


def get_service_names_for_compose(services_list: List[str],
                                 backend_services_list: List[str]) -> List[str]:
    """
    Convierte la lista de servicios lógicos a nombres de servicios Docker Compose.

    Args:
        services_list: Lista de servicios lógicos
        backend_services_list: Lista de microservicios backend

    Returns:
        List[str]: Nombres de servicios para Docker Compose
    """
    compose_services = []

    for service in services_list:
        if service == 'all':
            return []  # Docker Compose levantará todos por defecto
        elif service == 'frontend':
            compose_services.append('portfolio-frontend')
        elif service == 'backend':
            for backend_service in backend_services_list:
                compose_services.append(backend_service)
        elif service == 'db':
            compose_services.append('portfolio-db')
        elif service == 'gateway':
            compose_services.append('portfolio-gateway')

    return compose_services


def execute_docker_compose_command(cmd_parts: List[str], action: str, services: List[str],
                                  project_path: str, verbose: bool,
                                  additional_args: List[str] = None) -> Tuple[int, str, str]:
    """
    Ejecuta comando docker-compose.

    Args:
        cmd_parts: Partes base del comando
        action: Acción a ejecutar
        services: Servicios específicos
        project_path: Ruta del proyecto
        verbose: Mostrar información detallada
        additional_args: Argumentos adicionales

    Returns:
        Tuple[int, str, str]: (exit_code, stdout, stderr)
    """
    # Construir comando completo
    full_cmd = cmd_parts + [action]

    if additional_args:
        full_cmd.extend(additional_args)

    if services:
        full_cmd.extend(services)

    if verbose:
        print(f"🐳 Ejecutando: {' '.join(full_cmd)}")

    try:
        result = subprocess.run(full_cmd, cwd=project_path, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)


def wait_for_services_health(cmd_parts: List[str], services: List[str],
                           project_path: str, max_wait: int = 60,
                           verbose: bool = False) -> bool:
    """
    Espera a que los servicios estén healthy.

    Args:
        cmd_parts: Comando base docker-compose
        services: Servicios a verificar
        project_path: Ruta del proyecto
        max_wait: Tiempo máximo de espera en segundos
        verbose: Mostrar información detallada

    Returns:
        bool: True si todos los servicios están healthy
    """
    start_time = time.time()

    if verbose:
        print(f"⏳ Esperando que los servicios estén healthy (max {max_wait}s)...")

    while time.time() - start_time < max_wait:
        # Verificar estado de servicios
        cmd = cmd_parts + ['ps', '--format', 'json']
        result = subprocess.run(cmd, cwd=project_path, capture_output=True, text=True)

        if result.returncode == 0:
            try:
                # Parsear JSON output de docker-compose ps
                lines = [line for line in result.stdout.strip().split('\n') if line.strip()]
                all_healthy = True

                for line in lines:
                    try:
                        service_info = json.loads(line)
                        service_name = service_info.get('Service', '')
                        state = service_info.get('State', '')
                        health = service_info.get('Health', '')

                        # Si no hay services específicos, verificar todos
                        if not services or service_name in services:
                            if state != 'running':
                                all_healthy = False
                                if verbose:
                                    print(f"   ⏳ {service_name}: {state}")
                            elif health and health != 'healthy':
                                all_healthy = False
                                if verbose:
                                    print(f"   🔄 {service_name}: {health}")
                            elif verbose:
                                print(f"   ✅ {service_name}: healthy")
                    except json.JSONDecodeError:
                        continue

                if all_healthy:
                    if verbose:
                        print("✅ Todos los servicios están healthy")
                    return True

            except Exception as e:
                if verbose:
                    print(f"⚠️  Error verificando salud de servicios: {e}")

        time.sleep(2)

    if verbose:
        print(f"⚠️  Timeout esperando servicios healthy después de {max_wait}s")
    return False


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
        print("\n🔌 Puertos expuestos:")
        cmd = cmd_parts + ['port']
        result = subprocess.run(cmd, cwd=project_path, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            print(result.stdout)
        else:
            print("No hay puertos expuestos o servicios no están corriendo")


def follow_services_logs(cmd_parts: List[str], services: List[str],
                        project_path: str, verbose: bool) -> None:
    """
    Sigue los logs de los servicios en tiempo real.

    Args:
        cmd_parts: Comando base docker-compose
        services: Servicios específicos
        project_path: Ruta del proyecto
        verbose: Mostrar información detallada
    """
    print("📊 Siguiendo logs de servicios (Ctrl+C para salir)...")
    print("-" * 50)

    cmd = cmd_parts + ['logs', '-f', '--timestamps']
    if services:
        cmd.extend(services)

    try:
        subprocess.run(cmd, cwd=project_path)
    except KeyboardInterrupt:
        print("\n📊 Deteniendo seguimiento de logs")


def clean_docker_resources(project_path: str, verbose: bool) -> None:
    """
    Limpia recursos Docker del proyecto.

    Args:
        project_path: Ruta del proyecto
        verbose: Mostrar información detallada
    """
    if verbose:
        print("🧹 Limpiando recursos Docker...")

    commands = [
        (['docker', 'system', 'prune', '-f'], "Limpiando recursos no utilizados"),
        (['docker', 'volume', 'prune', '-f'], "Limpiando volúmenes no utilizados"),
        (['docker', 'network', 'prune', '-f'], "Limpiando redes no utilizadas")
    ]

    for cmd, description in commands:
        if verbose:
            print(f"   {description}...")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if verbose and result.stdout.strip():
                print(f"   {result.stdout.strip()}")
        except Exception as e:
            if verbose:
                print(f"   ⚠️  Error: {e}")

    print("✅ Limpieza completada")


def main(flags: Dict[str, Any]) -> None:
    """
    Función principal del script docker_env.

    Args:
        flags: Diccionario con las flags procesadas y validadas
    """
    verbose = flags.get('verbose', False)
    project_path = flags.get('project_path') or detect_project_root()
    env = flags.get('env', 'local')
    action = flags.get('action', 'up')
    services_list = flags.get('services_list', ['all'])
    backend_services_list = flags.get('backend_services_list', [])
    build = flags.get('build', False)
    detach = flags.get('detach', True)
    follow_logs = flags.get('follow_logs', False)

    if verbose:
        print(f"🏗️  Proyecto detectado en: {project_path}")
        print(f"🌍 Entorno: {env}")
        print(f"⚡ Acción: {action}")

    # Verificar Docker
    docker_available, docker_msg = check_docker_available()
    if not docker_available:
        print(f"❌ {docker_msg}")
        sys.exit(2)

    compose_available, compose_cmd, compose_msg = check_docker_compose_available()
    if not compose_available:
        print(f"❌ {compose_msg}")
        print("Instale Docker Compose: https://docs.docker.com/compose/install/")
        sys.exit(2)

    if verbose:
        print(f"✅ {docker_msg}")
        print(f"✅ {compose_msg}")

    # Buscar archivos de configuración
    config_files = find_docker_config_files(project_path)
    if not config_files:
        print("❌ No se encontró docker-compose.yml en el proyecto")
        print("Ubicaciones buscadas:")
        print("  - ./docker-compose.yml")
        print("  - ./docker/docker-compose.yml")
        sys.exit(1)

    if verbose:
        print(f"📁 Configuración Docker encontrada:")
        for env_name, file_path in config_files.items():
            print(f"  - {env_name}: {file_path}")

    # Buscar archivos .env
    env_files = find_env_files(project_path)
    if env in env_files:
        if verbose:
            print(f"📄 Variables de entorno: {env_files[env]}")
        # Cargar variables de entorno
        os.environ['COMPOSE_ENV_FILE'] = env_files[env]
    elif verbose:
        print(f"⚠️  No se encontró archivo .env para entorno {env}")

    # Construir comando docker-compose
    cmd_parts = build_docker_compose_command(config_files, env, compose_cmd)

    # Obtener nombres de servicios para docker-compose
    compose_services = get_service_names_for_compose(services_list, backend_services_list)

    # Verificar puertos si estamos levantando servicios
    if action == 'up':
        conflicting_ports = check_required_ports(services_list, verbose)
        if conflicting_ports:
            print("⚠️  Puertos en conflicto detectados:")
            for port in conflicting_ports:
                print(f"   - Puerto {port} está en uso")
            print("Los servicios pueden fallar al iniciar. Use --action=\"clean\" si es necesario.")

    # Ejecutar acción
    if action == 'up':
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
                else:
                    print("⚠️  Algunos servicios pueden no estar completamente listos")

                # Mostrar estado
                show_services_status(cmd_parts, project_path, verbose)

                # Seguir logs si se solicitó
                if follow_logs:
                    follow_services_logs(cmd_parts, compose_services, project_path, verbose)
        else:
            print("❌ Error levantando servicios")
            if verbose:
                print(f"stdout: {stdout}")
                print(f"stderr: {stderr}")
            sys.exit(exit_code)

    elif action == 'down':
        if verbose:
            print(f"⬇️  Bajando servicios...")

        exit_code, stdout, stderr = execute_docker_compose_command(
            cmd_parts, 'down', [], project_path, verbose, ['--remove-orphans']
        )

        if exit_code == 0:
            print("✅ Servicios bajados exitosamente")
        else:
            print("❌ Error bajando servicios")
            if verbose:
                print(f"stderr: {stderr}")
            sys.exit(exit_code)

    elif action == 'restart':
        if verbose:
            print(f"🔄 Reiniciando servicios...")

        exit_code, stdout, stderr = execute_docker_compose_command(
            cmd_parts, 'restart', compose_services, project_path, verbose
        )

        if exit_code == 0:
            print("✅ Servicios reiniciados exitosamente")
            show_services_status(cmd_parts, project_path, verbose)
        else:
            print("❌ Error reiniciando servicios")
            if verbose:
                print(f"stderr: {stderr}")
            sys.exit(exit_code)

    elif action == 'status':
        show_services_status(cmd_parts, project_path, verbose)

    elif action == 'logs':
        follow_services_logs(cmd_parts, compose_services, project_path, verbose)

    elif action == 'clean':
        # Primero bajar servicios
        print("🛑 Bajando servicios antes de limpiar...")
        execute_docker_compose_command(cmd_parts, 'down', [], project_path, verbose,
                                     ['--remove-orphans', '--volumes'])

        # Limpiar recursos Docker
        clean_docker_resources(project_path, verbose)

    if verbose:
        print(f"\n🎯 Operación '{action}' completada")