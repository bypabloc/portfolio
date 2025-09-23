"""
Gestión de Dockerfiles temporales para funciones Lambda.
"""

import yaml
from typing import List, Dict, Any
from pathlib import Path


def find_lambda_api_gateway_configs(project_path: str, verbose: bool = False) -> Dict[str, Dict[str, Any]]:
    """
    Detecta y parsea archivos config.yml en funciones lambda.

    Args:
        project_path: Ruta raíz del proyecto
        verbose: Mostrar información detallada

    Returns:
        Dict con nombre de lambda y su configuración completa
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
            config_file = lambda_dir / "setup" / "config.yml"

            if config_file.exists():
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config = yaml.safe_load(f)
                        configs[lambda_dir.name] = config
                except yaml.YAMLError as e:
                    if verbose:
                        print(f"❌ Error parseando {config_file}: {e}")
                except Exception as e:
                    if verbose:
                        print(f"❌ Error leyendo {config_file}: {e}")
            elif verbose:
                print(f"⚠️  No se encontró config.yml en {lambda_dir.name}/setup/")

    return configs


def generate_temp_dockerfile(lambda_name: str, config: Dict[str, Any], project_path: str, verbose: bool = False) -> str:
    """
    Genera un Dockerfile temporal para una función lambda usando LambdaDockerfileGenerator.

    Args:
        lambda_name: Nombre de la función lambda
        config: Configuración de la lambda desde config.yml
        project_path: Ruta raíz del proyecto
        verbose: Mostrar información detallada

    Returns:
        str: Ruta del Dockerfile temporal generado
    """
    try:
        # Import directo del dockerfile_generator
        import sys
        import os
        import importlib.util

        dockerfile_generator_path = os.path.join(
            os.path.dirname(__file__), '..', '..', 'dockerfile_generator.py'
        )
        spec = importlib.util.spec_from_file_location("dockerfile_generator", dockerfile_generator_path)
        dockerfile_generator_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(dockerfile_generator_module)
        LambdaDockerfileGenerator = dockerfile_generator_module.LambdaDockerfileGenerator

        # Crear generador de Dockerfiles
        generator = LambdaDockerfileGenerator(project_path)

        # Extraer configuración del lambda
        lambda_config = config.get('lambda_function', {})
        environment = 'dev'  # Para desarrollo local

        # Generar Dockerfile temporal con herramientas habilitadas
        dockerfile_path = generator.create_dockerfile(
            service_name=lambda_name,
            environment=environment,
            include_tools=True,  # ✅ Habilitar instalación de herramientas
            extra_packages=[]  # Usar solo paquetes base compatibles con AWS Lambda
        )

        # No mostrar paths individuales para salida más limpia
        return str(dockerfile_path)

    except Exception as e:
        if verbose:
            print(f"❌ Error generando Dockerfile para {lambda_name}: {e}")
        return ""


def generate_temp_dockerfiles(project_path: str, verbose: bool = False) -> List[str]:
    """
    Genera Dockerfiles temporales para todas las funciones lambda.

    Args:
        project_path: Ruta raíz del proyecto
        verbose: Mostrar información detallada

    Returns:
        List[str]: Lista de rutas de Dockerfiles temporales generados
    """
    print("🐳 Generando Dockerfiles temporales para funciones Lambda...")

    temp_files = []

    # Obtener configuraciones de todas las lambdas
    lambda_configs = find_lambda_api_gateway_configs(project_path, False)  # Sin verbose detallado

    if not lambda_configs:
        print("⚠️  No se encontraron configuraciones de lambda")
        return temp_files

    # Generar Dockerfile para cada lambda (sin mostrar cada archivo)
    for lambda_name, config in lambda_configs.items():
        dockerfile_path = generate_temp_dockerfile(lambda_name, config, project_path, False)
        if dockerfile_path:
            temp_files.append(dockerfile_path)

    print(f"✅ Generados {len(temp_files)} Dockerfiles temporales")

    return temp_files


def cleanup_temp_dockerfiles(temp_files: List[str], verbose: bool = False) -> None:
    """
    Limpia los Dockerfiles temporales usando LambdaDockerfileGenerator.

    Args:
        temp_files: Lista de rutas de archivos temporales
        verbose: Mostrar información detallada
    """
    if not temp_files:
        return

    # Limpieza silenciosa - no mostrar detalles al usuario

    # Determinar project_path desde el primer archivo temporal
    if temp_files:
        first_file = Path(temp_files[0])
        # Navegar desde server/lambda/service/Dockerfile.dev hacia la raíz
        project_path = first_file.parents[3]  # service → lambda → server → proyecto

        try:
            # Import directo del dockerfile_generator
            import sys
            import os
            import importlib.util

            dockerfile_generator_path = os.path.join(
                os.path.dirname(__file__), '..', '..', 'dockerfile_generator.py'
            )
            spec = importlib.util.spec_from_file_location("dockerfile_generator", dockerfile_generator_path)
            dockerfile_generator_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(dockerfile_generator_module)
            LambdaDockerfileGenerator = dockerfile_generator_module.LambdaDockerfileGenerator

            # Crear generador para limpieza
            generator = LambdaDockerfileGenerator(str(project_path))

            # Limpiar todos los Dockerfiles del entorno dev
            cleaned_count = generator.cleanup_all_dockerfiles(environment='dev')

            # Limpieza completada silenciosamente
            pass

        except Exception as e:
            if verbose:
                print(f"⚠️  Error usando LambdaDockerfileGenerator: {e}")

            # Fallback al método manual si no funciona el generador
            _manual_cleanup_dockerfiles(temp_files, verbose)
    else:
        # Fallback al método manual si no hay archivos
        _manual_cleanup_dockerfiles(temp_files, verbose)


def _manual_cleanup_dockerfiles(temp_files: List[str], verbose: bool = False) -> None:
    """
    Limpieza manual de Dockerfiles como fallback.

    Args:
        temp_files: Lista de rutas de archivos temporales
        verbose: Mostrar información detallada
    """
    for file_path in temp_files:
        try:
            Path(file_path).unlink(missing_ok=True)
        except Exception as e:
            # Silencioso: no mostrar errores de limpieza al usuario
            pass

    # Limpieza completada silenciosamente