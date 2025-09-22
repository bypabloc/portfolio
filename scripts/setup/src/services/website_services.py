"""
Gestión específica de servicios website/app (Frontend Astro v5).
"""

from typing import List, Dict, Any


def get_website_service_info() -> Dict[str, Any]:
    """
    Obtiene información del servicio website.

    Returns:
        Dict[str, Any]: Información del servicio website
    """
    return {
        'compose_name': 'portfolio-app',
        'port': 4321,
        'type': 'website',
        'icon': '🎨',
        'name': 'Website (Astro v5)',
        'technology': 'Astro v5 + TypeScript + Tailwind CSS'
    }


def get_website_endpoints() -> List[tuple]:
    """
    Obtiene los endpoints típicos del website.

    Returns:
        List[tuple]: Lista de (método, endpoint, descripción)
    """
    return [
        ("GET", "/", "Página principal del portfolio"),
        ("GET", "/about", "Página de información personal"),
        ("GET", "/experience", "Página de experiencia profesional"),
        ("GET", "/projects", "Página de portfolio de proyectos"),
        ("GET", "/skills", "Página de habilidades técnicas"),
        ("GET", "/contact", "Página de contacto"),
        ("GET", "/favicon.svg", "Favicon del sitio"),
        ("GET", "/*", "Todas las páginas estáticas")
    ]


def validate_website_configuration(project_path: str) -> Dict[str, bool]:
    """
    Valida que la configuración del website sea correcta.

    Args:
        project_path: Ruta del proyecto

    Returns:
        Dict[str, bool]: Resultados de validación
    """
    from pathlib import Path

    results = {}
    frontend_path = Path(project_path) / "frontend"
    website_path = Path(project_path) / "website"

    # Verificar si existe directorio frontend o website
    results['frontend_dir_exists'] = frontend_path.exists()
    results['website_dir_exists'] = website_path.exists()
    results['has_astro_project'] = (
        (frontend_path / "astro.config.ts").exists() or
        (website_path / "astro.config.ts").exists()
    )

    return results


def get_website_health_check_url(port: int = 4321) -> str:
    """
    Obtiene la URL de health check del website.

    Args:
        port: Puerto del website

    Returns:
        str: URL de health check
    """
    return f"http://localhost:{port}"