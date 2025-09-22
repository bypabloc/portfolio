"""
Configuración específica de API Gateway en LocalStack.
"""

import subprocess
import json
from typing import Dict, Any, bool
from pathlib import Path


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
        if not create_api_resource(api_id, root_resource_id, resource_path, verbose):
            return False

        # Obtener ID del recurso creado
        resource_id = get_resource_id(api_id, resource_path, verbose)
        if not resource_id:
            return False

        # Configurar métodos HTTP
        success_count = 0
        for method_config in methods_config:
            if configure_api_method(api_id, resource_id, lambda_name, method_config, verbose):
                success_count += 1

        return success_count > 0

    except Exception as e:
        if verbose:
            print(f"❌ Error configurando {lambda_name}: {e}")
        return False


def create_api_resource(api_id: str, parent_id: str, path: str, verbose: bool = False) -> bool:
    """
    Crea un recurso en API Gateway.

    Args:
        api_id: ID de la API
        parent_id: ID del recurso padre
        path: Path del recurso
        verbose: Mostrar información detallada

    Returns:
        bool: True si fue exitoso
    """
    create_resource_cmd = [
        "awslocal", "apigateway", "create-resource",
        "--rest-api-id", api_id,
        "--parent-id", parent_id,
        "--path-part", path
    ]

    resource_result = subprocess.run(
        ["docker", "exec", "portfolio-localstack"] + create_resource_cmd,
        capture_output=True,
        text=True
    )

    if resource_result.returncode == 0:
        if verbose:
            resource_data = json.loads(resource_result.stdout)
            resource_id = resource_data["id"]
            print(f"✅ Recurso creado: /{path} (ID: {resource_id})")
        return True
    else:
        if verbose:
            print(f"❌ Error creando recurso {path}: {resource_result.stderr}")
        return False


def get_resource_id(api_id: str, path: str, verbose: bool = False) -> str:
    """
    Obtiene el ID de un recurso por su path.

    Args:
        api_id: ID de la API
        path: Path del recurso
        verbose: Mostrar información detallada

    Returns:
        str: ID del recurso o cadena vacía si no se encuentra
    """
    try:
        get_resources_cmd = [
            "awslocal", "apigateway", "get-resources",
            "--rest-api-id", api_id
        ]

        result = subprocess.run(
            ["docker", "exec", "portfolio-localstack"] + get_resources_cmd,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            resources_data = json.loads(result.stdout)
            for resource in resources_data.get("items", []):
                if resource.get("pathPart") == path:
                    return resource["id"]

    except Exception as e:
        if verbose:
            print(f"❌ Error obteniendo ID de recurso {path}: {e}")

    return ""


def configure_api_method(api_id: str, resource_id: str, lambda_name: str,
                        method_config: Dict[str, Any], verbose: bool = False) -> bool:
    """
    Configura un método HTTP para un recurso.

    Args:
        api_id: ID de la API
        resource_id: ID del recurso
        lambda_name: Nombre de la función Lambda
        method_config: Configuración del método
        verbose: Mostrar información detallada

    Returns:
        bool: True si fue exitoso
    """
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
        return True
    elif verbose:
        print(f"⚠️  Error configurando integración: {integration_result.stderr}")

    return False


def deploy_api_gateway(verbose: bool = False) -> bool:
    """
    Despliega el API Gateway en LocalStack.

    Args:
        verbose: Mostrar información detallada

    Returns:
        bool: True si el despliegue fue exitoso
    """
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
                "--description", "Portfolio API deployment"
            ]

            deploy_result = subprocess.run(
                ["docker", "exec", "portfolio-localstack"] + deploy_cmd,
                capture_output=True,
                text=True
            )

            if deploy_result.returncode == 0:
                if verbose:
                    print(f"🚀 API Gateway desplegado")
                    print(f"🌐 URL de la API: http://localhost:4566/restapis/{api_id}/{stage_name}/_user_request_")
                return True
            elif verbose:
                print(f"⚠️  Error desplegando API: {deploy_result.stderr}")

    except Exception as e:
        if verbose:
            print(f"❌ Error desplegando API Gateway: {e}")

    return False


def get_api_gateway_info(verbose: bool = False) -> Dict[str, Any]:
    """
    Obtiene información del API Gateway configurado.

    Args:
        verbose: Mostrar información detallada

    Returns:
        Dict[str, Any]: Información del API Gateway
    """
    info = {
        'configured': False,
        'api_id': '',
        'stage_name': '',
        'resources': [],
        'url': ''
    }

    try:
        get_api_result = subprocess.run(
            ["docker", "exec", "portfolio-localstack", "cat", "/tmp/localstack-config.json"],
            capture_output=True,
            text=True
        )

        if get_api_result.returncode == 0:
            config = json.loads(get_api_result.stdout)
            info['configured'] = True
            info['api_id'] = config.get('api_id', '')
            info['stage_name'] = config.get('stage_name', '')
            info['url'] = f"http://localhost:4566/restapis/{info['api_id']}/{info['stage_name']}/_user_request_"

            if verbose:
                print("📊 Información API Gateway:")
                print(f"  API ID: {info['api_id']}")
                print(f"  Stage: {info['stage_name']}")
                print(f"  URL: {info['url']}")

    except Exception as e:
        if verbose:
            print(f"❌ Error obteniendo información API Gateway: {e}")

    return info


def validate_api_gateway_configuration(verbose: bool = False) -> Dict[str, bool]:
    """
    Valida la configuración del API Gateway.

    Args:
        verbose: Mostrar información detallada

    Returns:
        Dict[str, bool]: Resultados de validación
    """
    validation = {
        'api_exists': False,
        'resources_configured': False,
        'deployment_exists': False,
        'accessible': False
    }

    try:
        # Verificar si la API existe
        get_apis_result = subprocess.run(
            ["docker", "exec", "portfolio-localstack", "awslocal", "apigateway", "get-rest-apis"],
            capture_output=True,
            text=True
        )

        if get_apis_result.returncode == 0:
            apis_data = json.loads(get_apis_result.stdout)
            if apis_data.get("items"):
                validation['api_exists'] = True

        # Verificar información específica si está configurado
        info = get_api_gateway_info(verbose=False)
        if info['configured']:
            validation['resources_configured'] = True

            # Verificar accesibilidad (esto es una aproximación)
            validation['accessible'] = bool(info['url'])

    except Exception as e:
        if verbose:
            print(f"❌ Error validando configuración API Gateway: {e}")

    return validation