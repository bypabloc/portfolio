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
        cmd = cmd_parts + ['port']
        result = subprocess.run(cmd, cwd=project_path, capture_output=True, text=True)

        if result.returncode == 0 and result.stdout.strip():
            lines = result.stdout.strip().split('\n')
            current_service = None

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Las líneas de servicios no tienen ":"
                if ':' in line:
                    # Esta es una línea de puerto
                    if current_service:
                        if current_service not in port_mappings:
                            port_mappings[current_service] = []
                        port_mappings[current_service].append(line)
                else:
                    # Esta es una línea de servicio
                    current_service = line

    except Exception:
        pass

    return port_mappings