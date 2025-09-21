#!/usr/bin/env python3

import json
import os
import subprocess
import sys
import time
import yaml
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


def detect_platform() -> str:
    """
    Detecta la plataforma del sistema.

    Returns:
        str: 'wsl2', 'linux', 'macos', 'windows'
    """
    import platform

    system = platform.system().lower()

    # Detectar WSL2
    if system == 'linux':
        try:
            with open('/proc/version', 'r') as f:
                version_info = f.read().lower()
                if 'microsoft' in version_info or 'wsl' in version_info:
                    return 'wsl2'
        except:
            pass
        return 'linux'
    elif system == 'darwin':
        return 'macos'
    elif system == 'windows':
        return 'windows'
    else:
        return 'linux'  # Default fallback


def check_docker_available() -> Tuple[bool, str, Dict[str, Any]]:
    """
    Verifica si Docker está disponible y corriendo, con detección avanzada por plataforma.

    Returns:
        Tuple[bool, str, Dict]: (disponible, mensaje, info_detallada)
    """
    platform = detect_platform()
    info = {
        'platform': platform,
        'docker_installed': False,
        'docker_running': False,
        'docker_command': None,
        'installation_instructions': [],
        'startup_instructions': []
    }

    # Lista de comandos Docker a probar según plataforma
    docker_commands = ['docker']

    if platform == 'wsl2':
        # En WSL2, también probar docker.exe desde Windows
        docker_commands.extend([
            '/mnt/c/Program Files/Docker/Docker/resources/bin/docker.exe',
            'docker.exe'
        ])

    # Verificar instalación de Docker
    docker_found = False
    working_command = None

    for cmd in docker_commands:
        try:
            result = subprocess.run([cmd, '--version'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                docker_found = True
                working_command = cmd
                info['docker_installed'] = True
                info['docker_command'] = cmd
                break
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
        except Exception:
            continue

    if not docker_found:
        info['installation_instructions'] = get_docker_installation_instructions(platform)
        return False, f"🐳 Docker no está instalado en {platform.upper()}", info

    # Verificar que Docker daemon está corriendo
    try:
        result = subprocess.run([working_command, 'info'], capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            info['docker_running'] = True
            return True, "🐳 Docker disponible y funcionando", info
        else:
            # Docker instalado pero daemon no corriendo
            info['startup_instructions'] = get_docker_startup_instructions(platform)
            return False, f"🐳 Docker instalado pero no está corriendo en {platform.upper()}", info

    except subprocess.TimeoutExpired:
        info['startup_instructions'] = get_docker_startup_instructions(platform)
        return False, f"🐳 Docker daemon no responde en {platform.upper()}", info
    except Exception as e:
        return False, f"🐳 Error verificando Docker daemon: {e}", info


def get_docker_installation_instructions(platform: str) -> List[str]:
    """
    Obtiene instrucciones de instalación de Docker según la plataforma.

    Args:
        platform: Plataforma detectada

    Returns:
        List[str]: Lista de instrucciones de instalación
    """
    if platform == 'wsl2':
        return [
            "📥 INSTALACIÓN DOCKER EN WSL2:",
            "",
            "1️⃣ Instalar Docker Desktop en Windows:",
            "   • Descargar desde: https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe",
            "   • Ejecutar el instalador como administrador",
            "   • Reiniciar Windows después de la instalación",
            "",
            "2️⃣ Configurar WSL2 Integration:",
            "   • Abrir Docker Desktop",
            "   • Ir a Settings → Resources → WSL Integration",
            "   • Habilitar 'Enable integration with my default WSL distro'",
            "   • Seleccionar tu distribución WSL2",
            "   • Aplicar cambios y reiniciar Docker Desktop",
            "",
            "3️⃣ Verificar en WSL2:",
            "   wsl --update",
            "   wsl --shutdown",
            "   # Reiniciar tu terminal WSL2",
            "",
            "4️⃣ Probar instalación:",
            "   docker --version",
            "   docker run hello-world"
        ]
    elif platform == 'linux':
        return [
            "📥 INSTALACIÓN DOCKER EN LINUX:",
            "",
            "🐧 Ubuntu/Debian:",
            "   sudo apt update",
            "   sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release",
            "   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg",
            "   echo \"deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null",
            "   sudo apt update",
            "   sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin",
            "",
            "🎩 CentOS/RHEL/Fedora:",
            "   sudo dnf install -y dnf-plugins-core",
            "   sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo",
            "   sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin",
            "",
            "🔧 Post-instalación:",
            "   sudo systemctl enable docker",
            "   sudo systemctl start docker",
            "   sudo usermod -aG docker $USER",
            "   # Cerrar sesión y volver a entrar",
            "",
            "🧪 Probar:",
            "   docker --version",
            "   docker run hello-world"
        ]
    elif platform == 'macos':
        return [
            "📥 INSTALACIÓN DOCKER EN MACOS:",
            "",
            "🍎 Opción 1 - Docker Desktop (Recomendado):",
            "   • Descargar desde: https://desktop.docker.com/mac/main/amd64/Docker.dmg",
            "   • Arrastrar Docker.app a Applications",
            "   • Ejecutar Docker Desktop desde Applications",
            "   • Seguir el setup inicial",
            "",
            "🍺 Opción 2 - Homebrew:",
            "   brew install --cask docker",
            "   # Ejecutar Docker Desktop desde Applications",
            "",
            "🔧 Configuración:",
            "   • Docker Desktop debe estar corriendo en la barra de menú",
            "   • Configurar recursos en Preferences si es necesario",
            "",
            "🧪 Probar:",
            "   docker --version",
            "   docker run hello-world"
        ]
    elif platform == 'windows':
        return [
            "📥 INSTALACIÓN DOCKER EN WINDOWS:",
            "",
            "🪟 Docker Desktop:",
            "   • Descargar desde: https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe",
            "   • Ejecutar como administrador",
            "   • Habilitar WSL2 backend durante instalación",
            "   • Reiniciar Windows",
            "",
            "🔧 Requisitos previos:",
            "   • Windows 10 versión 2004+ o Windows 11",
            "   • WSL2 instalado y configurado",
            "   • Virtualización habilitada en BIOS",
            "",
            "⚙️ Configurar WSL2:",
            "   wsl --install",
            "   wsl --set-default-version 2",
            "",
            "🧪 Probar:",
            "   docker --version",
            "   docker run hello-world"
        ]
    else:
        return [
            "📥 INSTALACIÓN DOCKER:",
            "   Visita https://docs.docker.com/get-docker/ para instrucciones específicas de tu sistema."
        ]


def get_docker_startup_instructions(platform: str) -> List[str]:
    """
    Obtiene instrucciones para iniciar Docker según la plataforma.

    Args:
        platform: Plataforma detectada

    Returns:
        List[str]: Lista de instrucciones para iniciar Docker
    """
    if platform == 'wsl2':
        return [
            "🚀 INICIAR DOCKER EN WSL2:",
            "",
            "1️⃣ Verificar Docker Desktop en Windows:",
            "   • Buscar 'Docker Desktop' en el menú inicio",
            "   • Ejecutar Docker Desktop",
            "   • Esperar a que aparezca 'Docker Desktop is running' en la barra de tareas",
            "",
            "2️⃣ Si Docker Desktop no inicia:",
            "   • Reiniciar Docker Desktop desde la barra de tareas",
            "   • Verificar que WSL2 Integration esté habilitado en Settings",
            "   • Reiniciar Windows si es necesario",
            "",
            "3️⃣ En WSL2, probar:",
            "   docker --version",
            "   docker info"
        ]
    elif platform == 'linux':
        return [
            "🚀 INICIAR DOCKER EN LINUX:",
            "",
            "🔧 Iniciar servicio Docker:",
            "   sudo systemctl start docker",
            "   sudo systemctl enable docker  # Para inicio automático",
            "",
            "👤 Si no estás en el grupo docker:",
            "   sudo usermod -aG docker $USER",
            "   # Cerrar sesión y volver a entrar, o:",
            "   newgrp docker",
            "",
            "🧪 Verificar:",
            "   systemctl status docker",
            "   docker --version",
            "   docker info"
        ]
    elif platform == 'macos':
        return [
            "🚀 INICIAR DOCKER EN MACOS:",
            "",
            "🖱️ Iniciar Docker Desktop:",
            "   • Abrir Applications → Docker",
            "   • O buscar 'Docker' en Spotlight (Cmd+Space)",
            "   • Esperar a que aparezca el ícono de Docker en la barra de menú",
            "   • El ícono debe estar en estado 'running' (ballena)",
            "",
            "⚙️ Si Docker no inicia:",
            "   • Reiniciar Docker desde el menú de la barra",
            "   • Verificar recursos en Docker → Preferences → Resources",
            "   • Reiniciar macOS si es necesario",
            "",
            "🧪 Verificar:",
            "   docker --version",
            "   docker info"
        ]
    elif platform == 'windows':
        return [
            "🚀 INICIAR DOCKER EN WINDOWS:",
            "",
            "🖱️ Iniciar Docker Desktop:",
            "   • Buscar 'Docker Desktop' en el menú inicio",
            "   • Ejecutar como administrador si es necesario",
            "   • Esperar a que aparezca en la barra de tareas",
            "",
            "⚙️ Si Docker no inicia:",
            "   • Verificar que WSL2 esté corriendo: wsl --list --verbose",
            "   • Reiniciar Docker desde la barra de tareas",
            "   • Verificar virtualización en BIOS",
            "   • Reiniciar Windows si es necesario",
            "",
            "🧪 Verificar:",
            "   docker --version",
            "   docker info"
        ]
    else:
        return [
            "🚀 INICIAR DOCKER:",
            "   Consulta la documentación específica de tu sistema en https://docs.docker.com/"
        ]


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
        Path(project_path) / 'docker' / 'docker-compose.yml',
        Path(project_path) / 'setup' / 'docker-compose.yml'
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
        'app': [4321],
        'server': [8001, 8002, 8003, 8004],
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
        elif service == 'app':
            compose_services.append('portfolio-app')
        elif service == 'server':
            for server_service in server_services_list:
                compose_services.append(f'{server_service}-lambda')
        elif service == 'db':
            compose_services.append('portfolio-db')
        elif service == 'gateway':
            compose_services.append('api-gateway')

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
    server_services_list = flags.get('server_services_list', [])
    build = flags.get('build', False)
    detach = flags.get('detach', True)
    follow_logs = flags.get('follow_logs', False)

    if verbose:
        print(f"🏗️  Proyecto detectado en: {project_path}")
        print(f"🌍 Entorno: {env}")
        print(f"⚡ Acción: {action}")

    # Verificar Docker
    docker_available, docker_msg, platform_info = check_docker_available()
    if not docker_available:
        print(f"❌ {docker_msg}")

        # Mostrar instrucciones específicas por plataforma
        if platform_info.get('installation_instructions'):
            print("\n📋 Instrucciones de instalación:")
            for instruction in platform_info['installation_instructions']:
                print(f"   {instruction}")

        if platform_info.get('startup_instructions'):
            print("\n🚀 Para iniciar Docker:")
            for instruction in platform_info['startup_instructions']:
                print(f"   {instruction}")

        if platform_info.get('notes'):
            print(f"\n💡 Nota: {platform_info['notes']}")

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
        print("  - ./setup/docker-compose.yml")
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

    # Determinar profiles necesarios basado en servicios
    profiles = []

    # Construir comando docker-compose
    cmd_parts = build_docker_compose_command(config_files, env, compose_cmd, profiles)

    # Obtener nombres de servicios para docker-compose
    compose_services = get_service_names_for_compose(services_list, server_services_list)

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

                    # Configurar LocalStack API Gateway si está presente
                    if 'localstack' in [s.lower() for s in compose_services] or 'all' in services_list:
                        if verbose:
                            print("\n🌐 Configurando LocalStack API Gateway...")

                        if setup_localstack_api_gateway(project_path, verbose):
                            print("✅ LocalStack API Gateway configurado exitosamente")
                        else:
                            print("⚠️  LocalStack API Gateway no pudo ser configurado completamente")
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


def find_lambda_api_gateway_configs(project_path: str, verbose: bool = False) -> Dict[str, Dict[str, Any]]:
    """
    Detecta y parsea archivos api-gateway.yml en funciones lambda.

    Args:
        project_path: Ruta raíz del proyecto
        verbose: Mostrar información detallada

    Returns:
        Dict con nombre de lambda y su configuración API Gateway
    """
    configs = {}
    lambda_base_path = Path(project_path) / "server" / "lambda"

    if not lambda_base_path.exists():
        if verbose:
            print("⚠️  No se encontró directorio server/lambda")
        return configs

    # Buscar directorios de lambdas
    for lambda_dir in lambda_base_path.iterdir():
        if lambda_dir.is_dir() and not lambda_dir.name.startswith('.'):
            api_gateway_file = lambda_dir / "setup" / "api-gateway.yml"

            if api_gateway_file.exists():
                try:
                    with open(api_gateway_file, 'r', encoding='utf-8') as f:
                        config = yaml.safe_load(f)
                        configs[lambda_dir.name] = config
                        if verbose:
                            print(f"✅ Configuración API Gateway encontrada: {lambda_dir.name}")
                except yaml.YAMLError as e:
                    if verbose:
                        print(f"❌ Error parseando {api_gateway_file}: {e}")
                except Exception as e:
                    if verbose:
                        print(f"❌ Error leyendo {api_gateway_file}: {e}")
            elif verbose:
                print(f"⚠️  No se encontró api-gateway.yml en {lambda_dir.name}/setup/")

    return configs


def check_localstack_ready(max_attempts: int = 30, verbose: bool = False) -> bool:
    """
    Verifica si LocalStack está listo para recibir comandos.

    Args:
        max_attempts: Número máximo de intentos
        verbose: Mostrar información detallada

    Returns:
        bool: True si LocalStack está listo
    """
    if verbose:
        print("🔍 Verificando estado de LocalStack...")

    for attempt in range(max_attempts):
        try:
            result = subprocess.run(
                ["docker", "exec", "portfolio-localstack", "awslocal", "sts", "get-caller-identity"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                if verbose:
                    print("✅ LocalStack está listo")
                return True

        except subprocess.TimeoutExpired:
            if verbose:
                print(f"⏳ Intento {attempt + 1}/{max_attempts} - LocalStack aún no responde...")
        except Exception as e:
            if verbose:
                print(f"⏳ Intento {attempt + 1}/{max_attempts} - Error: {e}")

        if attempt < max_attempts - 1:
            time.sleep(5)

    return False


def initialize_localstack_api_gateway(project_path: str, verbose: bool = False) -> bool:
    """
    Inicializa LocalStack y ejecuta el script de configuración API Gateway.

    Args:
        project_path: Ruta raíz del proyecto
        verbose: Mostrar información detallada

    Returns:
        bool: True si la inicialización fue exitosa
    """
    localstack_script = Path(project_path) / "scripts" / "setup" / "localstack" / "init-api-gateway.sh"

    if not localstack_script.exists():
        if verbose:
            print(f"❌ Script de LocalStack no encontrado: {localstack_script}")
        return False

    try:
        if verbose:
            print("🚀 Inicializando LocalStack API Gateway...")

        # Hacer el script ejecutable
        subprocess.run(["chmod", "+x", str(localstack_script)], check=True)

        # Copiar y ejecutar script de inicialización usando docker cp
        temp_script = "/tmp/localstack-init.sh"

        # Copiar script al contenedor
        copy_result = subprocess.run(
            ["docker", "cp", str(localstack_script), f"portfolio-localstack:{temp_script}"],
            capture_output=True,
            text=True
        )

        if copy_result.returncode != 0:
            if verbose:
                print(f"❌ Error copiando script: {copy_result.stderr}")
            return False

        # Hacer ejecutable y ejecutar
        result = subprocess.run(
            ["docker", "exec", "portfolio-localstack", "bash", "-c", f"chmod +x {temp_script} && {temp_script}"],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            if verbose:
                print("✅ LocalStack API Gateway inicializado correctamente")
                print(result.stdout)
            return True
        else:
            if verbose:
                print("❌ Error inicializando LocalStack API Gateway")
                print(f"stderr: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        if verbose:
            print("❌ Timeout inicializando LocalStack")
        return False
    except Exception as e:
        if verbose:
            print(f"❌ Error ejecutando script de LocalStack: {e}")
        return False


def configure_lambda_api_gateway(lambda_name: str, config: Dict[str, Any], verbose: bool = False) -> bool:
    """
    Configura API Gateway para una función lambda específica usando awslocal.

    Args:
        lambda_name: Nombre de la función lambda
        config: Configuración API Gateway desde el archivo YAML
        verbose: Mostrar información detallada

    Returns:
        bool: True si la configuración fue exitosa
    """
    try:
        if verbose:
            print(f"🔧 Configurando API Gateway para {lambda_name}...")

        # Leer configuración existente de LocalStack
        get_api_result = subprocess.run(
            ["docker", "exec", "portfolio-localstack", "cat", "/tmp/localstack-config.json"],
            capture_output=True,
            text=True
        )

        if get_api_result.returncode != 0:
            if verbose:
                print("❌ No se pudo leer configuración de LocalStack")
            return False

        localstack_config = json.loads(get_api_result.stdout)
        api_id = localstack_config["api_id"]
        root_resource_id = localstack_config["root_resource_id"]

        # Extraer configuración de la lambda
        api_gateway_config = config.get("api_gateway", {})
        resource_config = api_gateway_config.get("resource", {})
        methods_config = api_gateway_config.get("methods", [])

        resource_path = resource_config.get("path", lambda_name)

        # Crear recurso para la lambda
        create_resource_cmd = [
            "awslocal", "apigateway", "create-resource",
            "--rest-api-id", api_id,
            "--parent-id", root_resource_id,
            "--path-part", resource_path
        ]

        resource_result = subprocess.run(
            ["docker", "exec", "portfolio-localstack"] + create_resource_cmd,
            capture_output=True,
            text=True
        )

        if resource_result.returncode != 0:
            if verbose:
                print(f"❌ Error creando recurso {resource_path}: {resource_result.stderr}")
            return False

        resource_data = json.loads(resource_result.stdout)
        resource_id = resource_data["id"]

        if verbose:
            print(f"✅ Recurso creado: /{resource_path} (ID: {resource_id})")

        # Configurar métodos HTTP
        for method_config in methods_config:
            http_method = method_config.get("http_method", "GET")

            # Crear método
            put_method_cmd = [
                "awslocal", "apigateway", "put-method",
                "--rest-api-id", api_id,
                "--resource-id", resource_id,
                "--http-method", http_method,
                "--authorization-type", "NONE"
            ]

            method_result = subprocess.run(
                ["docker", "exec", "portfolio-localstack"] + put_method_cmd,
                capture_output=True,
                text=True
            )

            if method_result.returncode != 0:
                if verbose:
                    print(f"⚠️  Método {http_method} ya existe o error: {method_result.stderr}")
            else:
                if verbose:
                    print(f"✅ Método {http_method} creado")

            # Crear integración con Lambda
            lambda_uri = f"arn:aws:lambda:us-east-1:000000000000:function:{lambda_name}"

            put_integration_cmd = [
                "awslocal", "apigateway", "put-integration",
                "--rest-api-id", api_id,
                "--resource-id", resource_id,
                "--http-method", http_method,
                "--type", "AWS_PROXY",
                "--integration-http-method", "POST",
                "--uri", f"arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_uri}/invocations"
            ]

            integration_result = subprocess.run(
                ["docker", "exec", "portfolio-localstack"] + put_integration_cmd,
                capture_output=True,
                text=True
            )

            if integration_result.returncode == 0:
                if verbose:
                    print(f"✅ Integración Lambda configurada para {http_method}")
            elif verbose:
                print(f"⚠️  Error configurando integración: {integration_result.stderr}")

        return True

    except Exception as e:
        if verbose:
            print(f"❌ Error configurando {lambda_name}: {e}")
        return False


def setup_localstack_api_gateway(project_path: str, verbose: bool = False) -> bool:
    """
    Setup completo de LocalStack API Gateway basado en configuraciones de lambdas.

    Args:
        project_path: Ruta raíz del proyecto
        verbose: Mostrar información detallada

    Returns:
        bool: True si el setup fue exitoso
    """
    if verbose:
        print("🌐 Configurando LocalStack API Gateway...")

    # 1. Verificar que LocalStack esté corriendo
    if not check_localstack_ready(max_attempts=30, verbose=verbose):
        if verbose:
            print("❌ LocalStack no está disponible")
        return False

    # 2. Inicializar LocalStack API Gateway
    if not initialize_localstack_api_gateway(project_path, verbose):
        if verbose:
            print("❌ Error inicializando LocalStack")
        return False

    # 3. Detectar configuraciones de lambdas
    lambda_configs = find_lambda_api_gateway_configs(project_path, verbose)

    if not lambda_configs:
        if verbose:
            print("⚠️  No se encontraron configuraciones de API Gateway")
        return True

    # 4. Configurar cada lambda
    success_count = 0
    for lambda_name, config in lambda_configs.items():
        if configure_lambda_api_gateway(lambda_name, config, verbose):
            success_count += 1

    # 5. Redesplegar API Gateway
    try:
        get_api_result = subprocess.run(
            ["docker", "exec", "portfolio-localstack", "cat", "/tmp/localstack-config.json"],
            capture_output=True,
            text=True
        )

        if get_api_result.returncode == 0:
            localstack_config = json.loads(get_api_result.stdout)
            api_id = localstack_config["api_id"]
            stage_name = localstack_config["stage_name"]

            deploy_cmd = [
                "awslocal", "apigateway", "create-deployment",
                "--rest-api-id", api_id,
                "--stage-name", stage_name,
                "--description", f"Portfolio API deployment with {success_count} lambdas"
            ]

            deploy_result = subprocess.run(
                ["docker", "exec", "portfolio-localstack"] + deploy_cmd,
                capture_output=True,
                text=True
            )

            if deploy_result.returncode == 0:
                if verbose:
                    print(f"🚀 API Gateway desplegado con {success_count} lambdas")
                    print(f"🌐 URL de la API: http://localhost:4566/restapis/{api_id}/{stage_name}/_user_request_")
                return True
            elif verbose:
                print(f"⚠️  Error desplegando API: {deploy_result.stderr}")

    except Exception as e:
        if verbose:
            print(f"❌ Error desplegando API Gateway: {e}")

    return success_count > 0