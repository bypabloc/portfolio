"""
Procesamiento y transformación de flags del sistema setup.
"""

from typing import Dict, Any, List
from .flag_validators import (
    validate_environment,
    validate_services,
    validate_action,
    validate_and_process_server_services,
    apply_compatibility_rules,
    validate_service_dependencies
)


def process_all_flags(flags_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Procesa y valida todas las flags del sistema setup.

    Args:
        flags_dict: Diccionario de flags básico

    Returns:
        Dict[str, Any]: Diccionario completamente procesado y validado

    Raises:
        ValueError: Si alguna validación falla
    """
    # Validar valores individuales
    validate_environment(flags_dict['env'])
    validate_action(flags_dict['action'])

    # Procesar y validar servicios
    services_list = validate_services(flags_dict['services'])
    flags_dict['services_list'] = services_list

    # Procesar microservicios del servidor
    server_services_list = validate_and_process_server_services(flags_dict['server_services'])
    flags_dict['server_services_list'] = server_services_list

    # Aplicar reglas de compatibilidad
    flags_dict = apply_compatibility_rules(flags_dict)

    # Validar dependencias entre servicios
    validate_service_dependencies(flags_dict)

    return flags_dict


def get_allowed_flags() -> List[str]:
    """
    Retorna la lista de flags permitidas para el sistema setup.

    Returns:
        List[str]: Lista de flags permitidas
    """
    return [
        'env',                   # local|test|dev|prod
        'services',              # website|server|db|gateway|all
        'action',                # up|down|restart|status|logs|clean
        'build',                 # forzar rebuild de imágenes
        'detach',                # ejecutar en background
        'project_path',          # path del proyecto
        'verbose',               # información detallada
        'follow_logs',           # seguir logs en tiempo real
        'server_services',       # microservicios server específicos
        'help'                   # sistema de ayuda
    ]


def get_default_values() -> Dict[str, Any]:
    """
    Retorna los valores por defecto para todas las flags.

    Returns:
        Dict[str, Any]: Diccionario con valores por defecto
    """
    return {
        'env': 'local',                    # entorno por defecto
        'services': 'all',                 # todos los servicios por defecto
        'action': 'up',                    # levantar servicios por defecto
        'build': False,                    # no rebuild por defecto
        'detach': True,                    # ejecutar en background por defecto
        'project_path': '',                # auto-detect del proyecto
        'verbose': False,                  # sin información detallada por defecto
        'follow_logs': False,              # no seguir logs por defecto
        'server_services': 'all',          # todos los microservicios server
    }


def extract_services_list(flags_dict: Dict[str, Any]) -> List[str]:
    """
    Extrae la lista de servicios procesada.

    Args:
        flags_dict: Diccionario de flags procesado

    Returns:
        List[str]: Lista de servicios
    """
    return flags_dict.get('services_list', [])


def extract_server_services_list(flags_dict: Dict[str, Any]) -> List[str]:
    """
    Extrae la lista de microservicios del servidor procesada.

    Args:
        flags_dict: Diccionario de flags procesado

    Returns:
        List[str]: Lista de microservicios del servidor
    """
    return flags_dict.get('server_services_list', [])