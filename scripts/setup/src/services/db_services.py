"""
Gestión específica de servicios de base de datos (PostgreSQL).
"""

from typing import List, Dict, Any


def get_db_service_info() -> Dict[str, Any]:
    """
    Obtiene información del servicio de base de datos.

    Returns:
        Dict[str, Any]: Información del servicio de base de datos
    """
    return {
        'compose_name': 'portfolio-db',
        'port': 5432,
        'type': 'database',
        'icon': '🗄️',
        'name': 'PostgreSQL Database',
        'technology': 'PostgreSQL 17 con branching'
    }


def get_db_connection_info(port: int = 5432, environment: str = 'local') -> Dict[str, str]:
    """
    Obtiene información de conexión a la base de datos.

    Args:
        port: Puerto de la base de datos
        environment: Entorno (local, dev, test, prod)

    Returns:
        Dict[str, str]: Información de conexión
    """
    db_name = f"portfolio_{environment}"

    return {
        'host': 'localhost',
        'port': str(port),
        'database': db_name,
        'username': 'postgres',
        'password': 'portfolio_password',
        'connection_url': f"postgresql://postgres:portfolio_password@localhost:{port}/{db_name}",
        'environment': environment
    }


def get_db_endpoints(port: int = 5432) -> List[tuple]:
    """
    Obtiene los endpoints/comandos de conexión a la base de datos.

    Args:
        port: Puerto de la base de datos

    Returns:
        List[tuple]: Lista de (tipo, comando/url, descripción)
    """
    return [
        ("CONNECT", f"postgresql://postgres:portfolio_password@localhost:{port}/portfolio_local", "Conexión directa"),
        ("CLI", f"psql -h localhost -p {port} -U postgres -d portfolio_local", "Cliente de línea de comandos"),
        ("GUI", "Adminer/pgAdmin", "Interfaz gráfica"),
        ("DOCKER", "docker exec -it portfolio-db psql -U postgres -d portfolio_local", "Conexión via Docker")
    ]


def get_db_health_check_command(port: int = 5432) -> str:
    """
    Obtiene el comando de health check para la base de datos.

    Args:
        port: Puerto de la base de datos

    Returns:
        str: Comando de health check
    """
    return f"pg_isready -h localhost -p {port} -U postgres"


def validate_db_configuration(project_path: str) -> Dict[str, bool]:
    """
    Valida que la configuración de la base de datos sea correcta.

    Args:
        project_path: Ruta del proyecto

    Returns:
        Dict[str, bool]: Resultados de validación
    """
    from pathlib import Path

    results = {}
    db_path = Path(project_path) / "db"
    setup_db_path = Path(project_path) / "setup" / "postgres"
    docker_db_path = Path(project_path) / "docker" / "postgres"

    # Verificar si existen archivos de configuración DB
    results['db_dir_exists'] = db_path.exists()
    results['setup_postgres_exists'] = setup_db_path.exists()
    results['docker_postgres_exists'] = docker_db_path.exists()
    results['has_init_sql'] = (
        (setup_db_path / "init.sql").exists() or
        (docker_db_path / "init.sql").exists() or
        (db_path / "init.sql").exists()
    )

    return results


def get_db_environment_variables(environment: str = 'local') -> Dict[str, str]:
    """
    Obtiene las variables de entorno para la base de datos.

    Args:
        environment: Entorno (local, dev, test, prod)

    Returns:
        Dict[str, str]: Variables de entorno
    """
    db_name = f"portfolio_{environment}"

    return {
        'POSTGRES_DB': db_name,
        'POSTGRES_USER': 'postgres',
        'POSTGRES_PASSWORD': 'portfolio_password',
        'PGDATA': '/var/lib/postgresql/data',
        'DATABASE_URL': f"postgresql://postgres:portfolio_password@localhost:5432/{db_name}"
    }