"""
Utilidades específicas para Docker Compose - Comandos, health checks, logs.
"""

import subprocess
import json
import time
from typing import Dict, List, Any, Tuple


def build_docker_compose_command(config_files: Dict[str, str], env: str,
                                compose_cmd: str, profiles: List[str] = None) -> List[str]:
    """
    Construye el comando docker-compose con archivos de configuración.

    Args:
        config_files: Archivos de configuración encontrados
        env: Entorno objetivo
        compose_cmd: Comando docker-compose a usar
        profiles: Lista de profiles a activar

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

    # Agregar profiles si se especificaron
    if profiles:
        for profile in profiles:
            cmd_parts.extend(['--profile', profile])

    return cmd_parts


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
        # Convertir paths absolutos a relativos para mostrar
        display_cmd = []
        for part in full_cmd:
            if part.startswith('/home/') and 'projects' in part:
                # Convertir path absoluto a relativo
                relative_part = part.replace(project_path, '.')
                display_cmd.append(relative_part)
            else:
                display_cmd.append(part)
        print(f"🐳 Ejecutando: {' '.join(display_cmd)}")

    try:
        result = subprocess.run(full_cmd, cwd=project_path, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)


def wait_for_services_health(cmd_parts: List[str], services: List[str],
                           project_path: str, max_wait: int = 60,
                           verbose: bool = False) -> bool:
    """
    Espera a que los servicios estén healthy con loading indicators individuales.

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

    # Estado de servicios para el loading
    service_status = {}
    loading_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    loading_index = 0

    print("⏳ Verificando estado de servicios...")

    while time.time() - start_time < max_wait:
        # Verificar estado de servicios
        cmd = cmd_parts + ['ps', '--format', 'json']
        result = subprocess.run(cmd, cwd=project_path, capture_output=True, text=True)

        if result.returncode == 0:
            try:
                # Parsear JSON output de docker-compose ps
                lines = [line for line in result.stdout.strip().split('\n') if line.strip()]
                all_healthy = True
                current_services = {}

                for line in lines:
                    try:
                        service_info = json.loads(line)
                        service_name = service_info.get('Service', '')
                        state = service_info.get('State', '')
                        health = service_info.get('Health', '')

                        # Si no hay services específicos, verificar todos
                        if not services or service_name in services:
                            current_services[service_name] = {
                                'state': state,
                                'health': health,
                                'healthy': state == 'running' and (not health or health == 'healthy')
                            }

                            if not current_services[service_name]['healthy']:
                                all_healthy = False

                    except json.JSONDecodeError:
                        continue

                # Mostrar loading por servicio
                loading_char = loading_chars[loading_index % len(loading_chars)]
                loading_index += 1

                # Limpiar líneas anteriores y mostrar estado
                print('\r\033[K', end='')  # Limpiar línea
                for service_name, status in current_services.items():
                    if status['healthy']:
                        print(f"✅ {service_name}: healthy", end="  ")
                    else:
                        state_desc = f"{status['state']}"
                        if status['health'] and status['health'] != 'healthy':
                            state_desc += f" ({status['health']})"
                        print(f"{loading_char} {service_name}: {state_desc}", end="  ")
                print()  # Nueva línea al final

                if all_healthy:
                    print()  # Línea extra para separar del siguiente output
                    return True

            except Exception as e:
                if verbose:
                    print(f"⚠️  Error verificando salud de servicios: {e}")

        time.sleep(2)

    print(f"⚠️  Timeout esperando servicios healthy después de {max_wait}s")
    return False


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


def get_compose_services_status(cmd_parts: List[str], project_path: str) -> Dict[str, Dict[str, Any]]:
    """
    Obtiene el estado actual de todos los servicios Docker Compose.

    Args:
        cmd_parts: Comando base docker-compose
        project_path: Ruta del proyecto

    Returns:
        Dict[str, Dict[str, Any]]: Estado de servicios por nombre
    """
    services_status = {}

    try:
        # Obtener estado de servicios en formato JSON
        cmd = cmd_parts + ['ps', '--format', 'json']
        result = subprocess.run(cmd, cwd=project_path, capture_output=True, text=True)

        if result.returncode == 0:
            lines = [line for line in result.stdout.strip().split('\n') if line.strip()]

            for line in lines:
                try:
                    service_info = json.loads(line)
                    service_name = service_info.get('Service', '')

                    if service_name:
                        services_status[service_name] = {
                            'name': service_name,
                            'state': service_info.get('State', 'unknown'),
                            'health': service_info.get('Health', ''),
                            'ports': service_info.get('Publishers', []),
                            'image': service_info.get('Image', ''),
                            'command': service_info.get('Command', '')
                        }
                except json.JSONDecodeError:
                    continue

    except Exception:
        pass

    return services_status


def get_compose_port_mappings(cmd_parts: List[str], project_path: str) -> Dict[str, List[str]]:
    """
    Obtiene los mapeos de puertos de servicios Docker Compose.

    Args:
        cmd_parts: Comando base docker-compose
        project_path: Ruta del proyecto

    Returns:
        Dict[str, List[str]]: Mapeos de puertos por servicio
    """
    port_mappings = {}

    try:
        cmd = cmd_parts + ['ps', '--format', 'json']
        result = subprocess.run(cmd, cwd=project_path, capture_output=True, text=True)

        if result.returncode == 0 and result.stdout.strip():
            lines = [line for line in result.stdout.strip().split('\n') if line.strip()]

            for line in lines:
                try:
                    service_info = json.loads(line)
                    service_name = service_info.get('Service', '')
                    publishers = service_info.get('Publishers', [])

                    if service_name and publishers:
                        port_mappings[service_name] = []
                        for publisher in publishers:
                            if isinstance(publisher, dict):
                                published_port = publisher.get('PublishedPort')
                                target_port = publisher.get('TargetPort')
                                protocol = publisher.get('Protocol', 'tcp')
                                if published_port and target_port:
                                    port_mappings[service_name].append(
                                        f"{published_port}:{target_port}/{protocol}"
                                    )
                            elif isinstance(publisher, str) and ':' in publisher:
                                # Formato string directo (fallback)
                                port_mappings[service_name].append(publisher)

                except json.JSONDecodeError:
                    continue
                except Exception:
                    continue

    except Exception:
        pass

    return port_mappings