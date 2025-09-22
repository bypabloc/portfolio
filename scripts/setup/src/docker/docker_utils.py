"""
Utilidades generales de Docker - Verificación, instalación, platform detection.
"""

import subprocess
import platform
from typing import Tuple, Dict, Any, List
from pathlib import Path


def detect_platform() -> str:
    """
    Detecta la plataforma del sistema.

    Returns:
        str: 'wsl2', 'linux', 'macos', 'windows'
    """
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
    platform_name = detect_platform()
    info = {
        'platform': platform_name,
        'docker_installed': False,
        'docker_running': False,
        'docker_command': None,
        'installation_instructions': [],
        'startup_instructions': []
    }

    # Lista de comandos Docker a probar según plataforma
    docker_commands = ['docker']

    if platform_name == 'wsl2':
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
        info['installation_instructions'] = get_docker_installation_instructions(platform_name)
        return False, f"🐳 Docker no está instalado en {platform_name.upper()}", info

    # Verificar que Docker daemon está corriendo
    try:
        result = subprocess.run([working_command, 'info'], capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            info['docker_running'] = True
            return True, "🐳 Docker disponible y funcionando", info
        else:
            # Docker instalado pero daemon no corriendo
            info['startup_instructions'] = get_docker_startup_instructions(platform_name)
            return False, f"🐳 Docker instalado pero no está corriendo en {platform_name.upper()}", info

    except subprocess.TimeoutExpired:
        info['startup_instructions'] = get_docker_startup_instructions(platform_name)
        return False, f"🐳 Docker daemon no responde en {platform_name.upper()}", info
    except Exception as e:
        return False, f"🐳 Error verificando Docker daemon: {e}", info


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


def get_docker_installation_instructions(platform_name: str) -> List[str]:
    """
    Obtiene instrucciones de instalación de Docker según la plataforma.

    Args:
        platform_name: Plataforma detectada

    Returns:
        List[str]: Lista de instrucciones de instalación
    """
    if platform_name == 'wsl2':
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
    elif platform_name == 'linux':
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
    elif platform_name == 'macos':
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
    elif platform_name == 'windows':
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


def get_docker_startup_instructions(platform_name: str) -> List[str]:
    """
    Obtiene instrucciones para iniciar Docker según la plataforma.

    Args:
        platform_name: Plataforma detectada

    Returns:
        List[str]: Lista de instrucciones para iniciar Docker
    """
    if platform_name == 'wsl2':
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
    elif platform_name == 'linux':
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
    elif platform_name == 'macos':
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
    elif platform_name == 'windows':
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