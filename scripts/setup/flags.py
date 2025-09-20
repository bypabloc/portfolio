import sys
import os

# Añadir utils al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.flags_to_dict import validate_allowed_flags, validate_required_flags, set_default_values


def flag(flags_dict):
    """
    Procesa y valida las flags del script docker_env.

    Args:
        flags_dict (dict): Diccionario de flags ya procesado por run.py

    Returns:
        dict: Diccionario validado con valores por defecto
    """

    # Definir flags permitidas
    allowed_flags = [
        'env',                   # local|test|dev|prod
        'services',              # frontend|backend|db|gateway|all
        'action',                # up|down|restart|status|logs|clean
        'build',                 # forzar rebuild de imágenes
        'detach',                # ejecutar en background
        'project_path',          # path del proyecto
        'verbose',               # información detallada
        'follow_logs',           # seguir logs en tiempo real
        'backend_services',      # microservicios backend específicos
        'help'                   # sistema de ayuda
    ]

    # Definir valores por defecto
    defaults = {
        'env': 'local',                    # entorno por defecto
        'services': 'all',                 # todos los servicios por defecto
        'action': 'up',                    # levantar servicios por defecto
        'build': False,                    # no rebuild por defecto
        'detach': True,                    # ejecutar en background por defecto
        'project_path': '',                # auto-detect del proyecto
        'verbose': False,                  # sin información detallada por defecto
        'follow_logs': False,              # no seguir logs por defecto
        'backend_services': 'all',         # todos los microservicios backend
    }

    # Validar flags permitidas
    validate_allowed_flags(flags_dict, allowed_flags)

    # Aplicar valores por defecto
    flags_dict = set_default_values(flags_dict, defaults)

    # Validar valores específicos
    valid_envs = ['local', 'test', 'dev', 'release', 'prod']
    if flags_dict['env'] not in valid_envs:
        raise ValueError(
            f"Entorno inválido: {flags_dict['env']}. "
            f"Valores válidos: {', '.join(valid_envs)}"
        )

    valid_services = ['frontend', 'backend', 'db', 'gateway', 'all']
    services_list = [s.strip() for s in flags_dict['services'].split(',') if s.strip()]
    for service in services_list:
        if service not in valid_services:
            raise ValueError(
                f"Servicio inválido: {service}. "
                f"Valores válidos: {', '.join(valid_services)}"
            )

    valid_actions = ['up', 'down', 'restart', 'status', 'logs', 'clean']
    if flags_dict['action'] not in valid_actions:
        raise ValueError(
            f"Acción inválida: {flags_dict['action']}. "
            f"Valores válidas: {', '.join(valid_actions)}"
        )

    # Procesar backend_services si se especificó (AWS Lambda functions)
    backend_services_list = ['personal-info', 'skills', 'all']
    if flags_dict['backend_services'] != 'all':
        specified_services = [s.strip() for s in flags_dict['backend_services'].split(',') if s.strip()]
        for service in specified_services:
            if service not in backend_services_list:
                raise ValueError(
                    f"Lambda function inválida: {service}. "
                    f"Valores válidos: {', '.join(backend_services_list)}"
                )
        flags_dict['backend_services_list'] = specified_services
    else:
        flags_dict['backend_services_list'] = ['personal-info', 'skills']


    # Procesar services como lista
    flags_dict['services_list'] = services_list

    # Validaciones específicas de compatibilidad
    if flags_dict['action'] == 'logs' and not flags_dict['follow_logs']:
        # Para logs, activar follow_logs por defecto
        flags_dict['follow_logs'] = True

    if flags_dict['action'] in ['status', 'clean'] and flags_dict['follow_logs']:
        # follow_logs no tiene sentido para status o clean
        flags_dict['follow_logs'] = False

    # Si services incluye 'backend', validar backend_services
    if 'backend' in services_list and flags_dict['backend_services'] != 'all':
        if not flags_dict['backend_services_list']:
            raise ValueError(
                "Si especifica --services=\"backend\", debe especificar "
                "--backend-services con al menos un microservicio válido"
            )


    # Mostrar configuración si no es modo silencioso
    if not flags_dict.get('_invoked_from') == 'cli' or flags_dict.get('verbose'):
        print("🐳 Configuración docker_env:")
        print(f"  🌍 Entorno: {flags_dict['env']}")
        print(f"  ⚡ Acción: {flags_dict['action']}")

        if 'all' in services_list:
            print(f"  🏗️  Servicios: Todos (frontend, backend, db, gateway)")
        else:
            print(f"  🏗️  Servicios: {', '.join(services_list)}")

        if 'backend' in services_list:
            if flags_dict['backend_services'] == 'all':
                print(f"  🔧 Backend: Todos los microservicios")
            else:
                print(f"  🔧 Backend: {', '.join(flags_dict['backend_services_list'])}")


        if flags_dict.get('build'):
            print(f"  🔨 Rebuild: Habilitado")

        if flags_dict['action'] == 'up':
            if flags_dict.get('detach'):
                print(f"  🔄 Modo: Background (detached)")
            else:
                print(f"  🔄 Modo: Foreground (attached)")

        if flags_dict.get('follow_logs'):
            print(f"  📊 Logs: Seguimiento en tiempo real")

        if flags_dict.get('verbose'):
            print(f"  🔍 Modo verbose: Habilitado")

        print()

    return flags_dict