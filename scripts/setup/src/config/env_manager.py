"""
Gestión de variables de entorno y archivos .env por ambiente.
"""

import os
from typing import Dict, List, Optional
from pathlib import Path


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
        'release': ['.env.release', '.env.staging'],
        'prod': ['.env.prod', '.env.production']
    }

    for env, possible_names in env_file_names.items():
        for name in possible_names:
            env_file_path = project_dir / name
            if env_file_path.exists():
                env_files[env] = str(env_file_path)
                break

    return env_files


def load_env_file(env_file_path: str) -> Dict[str, str]:
    """
    Carga variables de entorno desde un archivo .env.

    Args:
        env_file_path: Ruta del archivo .env

    Returns:
        Dict[str, str]: Variables de entorno cargadas
    """
    env_vars = {}

    try:
        with open(env_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                # Ignorar líneas vacías y comentarios
                if not line or line.startswith('#'):
                    continue

                # Buscar formato KEY=VALUE
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    # Remover comillas si están presentes
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]

                    env_vars[key] = value

    except Exception as e:
        print(f"⚠️  Error leyendo archivo .env {env_file_path}: {e}")

    return env_vars


def set_env_for_compose(env_file_path: str) -> None:
    """
    Configura la variable de entorno para Docker Compose.

    Args:
        env_file_path: Ruta del archivo .env
    """
    os.environ['COMPOSE_ENV_FILE'] = env_file_path


def get_default_env_template(environment: str) -> Dict[str, str]:
    """
    Obtiene un template de variables de entorno por defecto para un ambiente.

    Args:
        environment: Nombre del ambiente (local, test, dev, prod)

    Returns:
        Dict[str, str]: Template de variables de entorno
    """
    common_vars = {
        'NODE_ENV': environment if environment != 'local' else 'development',
        'COMPOSE_PROJECT_NAME': 'portfolio',
        'DOCKER_BUILDKIT': '1',
        'COMPOSE_DOCKER_CLI_BUILD': '1'
    }

    if environment == 'local':
        return {
            **common_vars,
            'NODE_ENV': 'development',
            'ASTRO_PORT': '4321',
            'API_GATEWAY_URL': 'http://localhost:8090',
            'PERSONAL_INFO_API_URL': 'http://localhost:8001',
            'SKILLS_API_URL': 'http://localhost:8002',
            'EXPERIENCE_API_URL': 'http://localhost:8003',
            'PROJECTS_API_URL': 'http://localhost:8004',
            'DATABASE_URL': 'postgresql://postgres:portfolio_password@localhost:5432/portfolio_local',
            'NEON_BRANCH': 'local',
            'HOT_RELOAD': 'true',
            'DEBUG_MODE': 'true',
            'LOG_LEVEL': 'debug'
        }
    elif environment == 'test':
        return {
            **common_vars,
            'NODE_ENV': 'test',
            'ASTRO_PORT': '4321',
            'API_GATEWAY_URL': 'http://localhost:8090',
            'DATABASE_URL': 'postgresql://postgres:portfolio_password@localhost:5432/portfolio_test',
            'NEON_BRANCH': 'test',
            'HOT_RELOAD': 'false',
            'DEBUG_MODE': 'false',
            'LOG_LEVEL': 'error'
        }
    elif environment == 'dev':
        return {
            **common_vars,
            'NODE_ENV': 'development',
            'ASTRO_PORT': '4321',
            'API_GATEWAY_URL': 'http://localhost:8090',
            'DATABASE_URL': 'postgresql://postgres:portfolio_password@localhost:5432/portfolio_dev',
            'NEON_BRANCH': 'dev',
            'HOT_RELOAD': 'true',
            'DEBUG_MODE': 'true',
            'LOG_LEVEL': 'info'
        }
    elif environment == 'release':
        return {
            **common_vars,
            'NODE_ENV': 'production',
            'ASTRO_PORT': '4321',
            'API_GATEWAY_URL': 'http://localhost:8090',
            'DATABASE_URL': 'postgresql://postgres:portfolio_password@localhost:5432/portfolio_release',
            'NEON_BRANCH': 'staging',
            'HOT_RELOAD': 'false',
            'DEBUG_MODE': 'false',
            'LOG_LEVEL': 'warn',
            'MONITORING_ENABLED': 'true'
        }
    elif environment == 'prod':
        return {
            **common_vars,
            'NODE_ENV': 'production',
            'ASTRO_PORT': '4321',
            'API_GATEWAY_URL': 'http://localhost:8090',
            'DATABASE_URL': 'postgresql://postgres:portfolio_password@localhost:5432/portfolio_prod',
            'NEON_BRANCH': 'main',
            'HOT_RELOAD': 'false',
            'DEBUG_MODE': 'false',
            'LOG_LEVEL': 'warn',
            'MONITORING_ENABLED': 'true'
        }
    else:
        return common_vars


def validate_env_configuration(env_vars: Dict[str, str], environment: str) -> Dict[str, List[str]]:
    """
    Valida la configuración de variables de entorno.

    Args:
        env_vars: Variables de entorno a validar
        environment: Ambiente objetivo

    Returns:
        Dict[str, List[str]]: Resultados de validación (warnings, errors, recommendations)
    """
    validation = {
        'errors': [],
        'warnings': [],
        'recommendations': []
    }

    required_vars = ['NODE_ENV', 'DATABASE_URL', 'ASTRO_PORT']
    optional_but_recommended = ['API_GATEWAY_URL', 'LOG_LEVEL', 'NEON_BRANCH']

    # Verificar variables requeridas
    for var in required_vars:
        if var not in env_vars:
            validation['errors'].append(f"Variable requerida faltante: {var}")

    # Verificar variables recomendadas
    for var in optional_but_recommended:
        if var not in env_vars:
            validation['warnings'].append(f"Variable recomendada faltante: {var}")

    # Validaciones específicas por ambiente
    if environment == 'prod':
        if env_vars.get('DEBUG_MODE', '').lower() == 'true':
            validation['warnings'].append("DEBUG_MODE está habilitado en producción")

        if env_vars.get('HOT_RELOAD', '').lower() == 'true':
            validation['warnings'].append("HOT_RELOAD está habilitado en producción")

    if environment in ['local', 'dev']:
        if env_vars.get('HOT_RELOAD', '').lower() != 'true':
            validation['recommendations'].append("Considerar habilitar HOT_RELOAD para desarrollo")

    # Validar formato de DATABASE_URL
    database_url = env_vars.get('DATABASE_URL', '')
    if database_url and not database_url.startswith('postgresql://'):
        validation['errors'].append("DATABASE_URL debe comenzar con 'postgresql://'")

    return validation


def create_env_file_if_missing(project_path: str, environment: str) -> Optional[str]:
    """
    Crea un archivo .env si no existe, usando el template por defecto.

    Args:
        project_path: Ruta del proyecto
        environment: Ambiente objetivo

    Returns:
        Optional[str]: Ruta del archivo .env creado, o None si ya existía
    """
    env_files = find_env_files(project_path)

    if environment in env_files:
        return None  # Ya existe

    # Crear archivo .env con template
    env_filename = f".env.{environment}"
    env_file_path = Path(project_path) / env_filename

    template_vars = get_default_env_template(environment)

    try:
        with open(env_file_path, 'w', encoding='utf-8') as f:
            f.write(f"# Variables de entorno para {environment.upper()}\n")
            f.write(f"# Generado automáticamente\n\n")

            for key, value in template_vars.items():
                f.write(f"{key}={value}\n")

        return str(env_file_path)

    except Exception as e:
        print(f"❌ Error creando archivo .env: {e}")
        return None