"""
Utilidades para mostrar configuración de flags del sistema setup.
"""

from typing import Dict, Any, List


def show_flag_configuration(flags_dict: Dict[str, Any]) -> None:
    """
    Muestra la configuración de flags de forma organizada.

    Args:
        flags_dict: Diccionario con todas las flags procesadas
    """
    # Solo mostrar si no es modo silencioso o si verbose está activado
    if not flags_dict.get('_invoked_from') == 'cli' or flags_dict.get('verbose'):
        print("🐳 Configuración docker_env:")
        print(f"  🌍 Entorno: {flags_dict['env']}")
        print(f"  ⚡ Acción: {flags_dict['action']}")

        _show_services_configuration(flags_dict)
        _show_build_configuration(flags_dict)
        _show_execution_mode(flags_dict)
        _show_logs_configuration(flags_dict)
        _show_verbose_mode(flags_dict)

        print()


def _show_services_configuration(flags_dict: Dict[str, Any]) -> None:
    """
    Muestra la configuración de servicios.

    Args:
        flags_dict: Diccionario de flags
    """
    services_list = flags_dict.get('services_list', [])

    if 'all' in services_list:
        print(f"  🏗️  Servicios: Todos (website, server, db, gateway)")
    else:
        print(f"  🏗️  Servicios: {', '.join(services_list)}")

    # Mostrar configuración de microservicios server si corresponde
    if 'server' in services_list:
        if flags_dict['server_services'] == 'all':
            print(f"  🔧 Server: Todos los microservicios")
        else:
            server_services_list = flags_dict.get('server_services_list', [])
            print(f"  🔧 Server: {', '.join(server_services_list)}")


def _show_build_configuration(flags_dict: Dict[str, Any]) -> None:
    """
    Muestra la configuración de build.

    Args:
        flags_dict: Diccionario de flags
    """
    if flags_dict.get('build'):
        print(f"  🔨 Rebuild: Habilitado")


def _show_execution_mode(flags_dict: Dict[str, Any]) -> None:
    """
    Muestra el modo de ejecución.

    Args:
        flags_dict: Diccionario de flags
    """
    if flags_dict['action'] == 'up':
        if flags_dict.get('detach'):
            print(f"  🔄 Modo: Background (detached)")
        else:
            print(f"  🔄 Modo: Foreground (attached)")


def _show_logs_configuration(flags_dict: Dict[str, Any]) -> None:
    """
    Muestra la configuración de logs.

    Args:
        flags_dict: Diccionario de flags
    """
    if flags_dict.get('follow_logs'):
        print(f"  📊 Logs: Seguimiento en tiempo real")


def _show_verbose_mode(flags_dict: Dict[str, Any]) -> None:
    """
    Muestra si el modo verbose está activado.

    Args:
        flags_dict: Diccionario de flags
    """
    if flags_dict.get('verbose'):
        print(f"  🔍 Modo verbose: Habilitado")


def show_simplified_configuration(flags_dict: Dict[str, Any]) -> None:
    """
    Muestra una configuración simplificada para uso en modo silencioso.

    Args:
        flags_dict: Diccionario de flags
    """
    action = flags_dict.get('action', 'up')
    env = flags_dict.get('env', 'local')
    services = flags_dict.get('services', 'all')

    print(f"🚀 Ejecutando: {action} en {env} para {services}")