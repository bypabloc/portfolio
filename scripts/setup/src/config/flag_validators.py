"""
Validadores específicos para flags del sistema de setup.
"""

from typing import Dict, Any, List


def validate_environment(env: str) -> None:
    """
    Valida que el entorno sea válido.

    Args:
        env: Entorno a validar

    Raises:
        ValueError: Si el entorno no es válido
    """
    valid_envs = ['local', 'test', 'dev', 'release', 'prod']
    if env not in valid_envs:
        raise ValueError(
            f"Entorno inválido: {env}. "
            f"Valores válidos: {', '.join(valid_envs)}"
        )


def validate_services(services: str) -> List[str]:
    """
    Valida y procesa la lista de servicios.

    Args:
        services: String con servicios separados por comas

    Returns:
        List[str]: Lista de servicios validados

    Raises:
        ValueError: Si algún servicio no es válido
    """
    valid_services = ['website', 'server', 'db', 'gateway', 'all']
    services_list = [s.strip() for s in services.split(',') if s.strip()]

    for service in services_list:
        if service not in valid_services:
            raise ValueError(
                f"Servicio inválido: {service}. "
                f"Valores válidos: {', '.join(valid_services)}"
            )

    return services_list


def validate_action(action: str) -> None:
    """
    Valida que la acción sea válida.

    Args:
        action: Acción a validar

    Raises:
        ValueError: Si la acción no es válida
    """
    valid_actions = ['up', 'down', 'restart', 'status', 'logs', 'clean']
    if action not in valid_actions:
        raise ValueError(
            f"Acción inválida: {action}. "
            f"Valores válidas: {', '.join(valid_actions)}"
        )


def validate_and_process_server_services(server_services: str) -> List[str]:
    """
    Valida y procesa los microservicios del servidor.

    Args:
        server_services: String con microservicios separados por comas o 'all'

    Returns:
        List[str]: Lista de microservicios validados

    Raises:
        ValueError: Si algún microservicio no es válido
    """
    server_services_list = ['personal-info', 'skills', 'experience', 'projects', 'all']

    if server_services == 'all':
        return ['personal-info', 'skills', 'experience', 'projects']

    specified_services = [s.strip() for s in server_services.split(',') if s.strip()]
    for service in specified_services:
        if service not in server_services_list:
            raise ValueError(
                f"Lambda function inválida: {service}. "
                f"Valores válidos: {', '.join(server_services_list)}"
            )

    return specified_services


def apply_compatibility_rules(flags_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Aplica reglas de compatibilidad entre flags.

    Args:
        flags_dict: Diccionario de flags

    Returns:
        Dict[str, Any]: Diccionario con reglas aplicadas
    """
    # Para logs, activar follow_logs por defecto
    if flags_dict['action'] == 'logs' and not flags_dict['follow_logs']:
        flags_dict['follow_logs'] = True

    # follow_logs no tiene sentido para status o clean
    if flags_dict['action'] in ['status', 'clean'] and flags_dict['follow_logs']:
        flags_dict['follow_logs'] = False

    return flags_dict


def validate_service_dependencies(flags_dict: Dict[str, Any]) -> None:
    """
    Valida dependencias entre servicios.

    Args:
        flags_dict: Diccionario de flags

    Raises:
        ValueError: Si hay dependencias no satisfechas
    """
    services_list = flags_dict.get('services_list', [])

    # Si services incluye 'server', validar server_services
    if 'server' in services_list and flags_dict['server_services'] != 'all':
        if not flags_dict.get('server_services_list'):
            raise ValueError(
                "Si especifica --services=\"server\", debe especificar "
                "--server-services con al menos un microservicio válido"
            )