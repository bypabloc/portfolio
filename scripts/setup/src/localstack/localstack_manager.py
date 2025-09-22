"""
Gestión principal de LocalStack y configuración de servicios.
"""

import sys
import os
import subprocess
import json
import time
from typing import Dict, Any, List
from pathlib import Path

# Añadir src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def check_localstack_ready(max_attempts: int = 30, verbose: bool = False) -> bool:
    """
    Verifica si LocalStack está listo para recibir comandos.

    Args:
        max_attempts: Número máximo de intentos
        verbose: Mostrar información detallada

    Returns:
        bool: True si LocalStack está listo
    """
    if verbose:
        print("🔍 Verificando estado de LocalStack...")

    for attempt in range(max_attempts):
        try:
            result = subprocess.run(
                ["docker", "exec", "portfolio-localstack", "awslocal", "sts", "get-caller-identity"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                if verbose:
                    print("✅ LocalStack está listo")
                return True

        except subprocess.TimeoutExpired:
            if verbose:
                print(f"⏳ Intento {attempt + 1}/{max_attempts} - LocalStack aún no responde...")
        except Exception as e:
            if verbose:
                print(f"⏳ Intento {attempt + 1}/{max_attempts} - Error: {e}")

        if attempt < max_attempts - 1:
            time.sleep(5)

    return False


def setup_localstack_api_gateway(project_path: str, verbose: bool = False) -> bool:
    """
    Setup completo de LocalStack API Gateway basado en configuraciones de lambdas.

    Args:
        project_path: Ruta raíz del proyecto
        verbose: Mostrar información detallada

    Returns:
        bool: True si el setup fue exitoso
    """
    from .api_gateway_setup import (
        initialize_localstack_api_gateway,
        configure_lambda_api_gateway,
        deploy_api_gateway
    )
    from docker.dockerfile_manager import find_lambda_api_gateway_configs

    if verbose:
        print("🌐 Configurando LocalStack API Gateway...")

    # 1. Verificar que LocalStack esté corriendo
    if not check_localstack_ready(max_attempts=30, verbose=verbose):
        if verbose:
            print("❌ LocalStack no está disponible")
        return False

    # 2. Inicializar LocalStack API Gateway
    if not initialize_localstack_api_gateway(project_path, verbose):
        if verbose:
            print("❌ Error inicializando LocalStack")
        return False

    # 3. Detectar configuraciones de lambdas
    lambda_configs = find_lambda_api_gateway_configs(project_path, verbose)

    if not lambda_configs:
        if verbose:
            print("⚠️  No se encontraron configuraciones de API Gateway")
        return True

    # 4. Configurar cada lambda
    success_count = 0
    for lambda_name, config in lambda_configs.items():
        if configure_lambda_api_gateway(lambda_name, config, verbose):
            success_count += 1

    # 5. Redesplegar API Gateway
    if deploy_api_gateway(verbose):
        if verbose:
            print(f"🚀 API Gateway desplegado con {success_count} lambdas")
        return True

    return success_count > 0


def check_localstack_services_status(verbose: bool = False) -> Dict[str, bool]:
    """
    Verifica el estado de servicios LocalStack.

    Args:
        verbose: Mostrar información detallada

    Returns:
        Dict[str, bool]: Estado de servicios LocalStack
    """
    services_status = {
        'apigateway': False,
        'lambda': False,
        'sts': False,
        'logs': False
    }

    if not verbose:
        return services_status

    try:
        # Verificar servicios disponibles
        result = subprocess.run(
            ["docker", "exec", "portfolio-localstack", "awslocal", "apigateway", "get-rest-apis"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            services_status['apigateway'] = True

        # Verificar Lambda
        result = subprocess.run(
            ["docker", "exec", "portfolio-localstack", "awslocal", "lambda", "list-functions"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            services_status['lambda'] = True

        # Verificar STS
        result = subprocess.run(
            ["docker", "exec", "portfolio-localstack", "awslocal", "sts", "get-caller-identity"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            services_status['sts'] = True

    except Exception as e:
        if verbose:
            print(f"⚠️  Error verificando servicios LocalStack: {e}")

    return services_status


def get_localstack_endpoints(verbose: bool = False) -> Dict[str, str]:
    """
    Obtiene los endpoints disponibles de LocalStack.

    Args:
        verbose: Mostrar información detallada

    Returns:
        Dict[str, str]: Endpoints de LocalStack
    """
    endpoints = {
        'base': 'http://localhost:4566',
        'apigateway': 'http://localhost:4566/restapis',
        'lambda': 'http://localhost:4566/2015-03-31/functions',
        'logs': 'http://localhost:4566/logs',
        'health': 'http://localhost:4566/_localstack/health'
    }

    if verbose:
        print("🌐 Endpoints LocalStack disponibles:")
        for service, endpoint in endpoints.items():
            print(f"  {service}: {endpoint}")

    return endpoints


def cleanup_localstack_resources(verbose: bool = False) -> bool:
    """
    Limpia recursos de LocalStack.

    Args:
        verbose: Mostrar información detallada

    Returns:
        bool: True si la limpieza fue exitosa
    """
    cleanup_commands = [
        ["awslocal", "apigateway", "get-rest-apis"],
        ["awslocal", "lambda", "list-functions"]
    ]

    if verbose:
        print("🧹 Limpiando recursos LocalStack...")

    try:
        for cmd in cleanup_commands:
            result = subprocess.run(
                ["docker", "exec", "portfolio-localstack"] + cmd,
                capture_output=True,
                text=True,
                timeout=10
            )

            if verbose and result.returncode == 0:
                print(f"✅ Comando ejecutado: {' '.join(cmd)}")

        return True

    except Exception as e:
        if verbose:
            print(f"❌ Error limpiando LocalStack: {e}")
        return False


def get_localstack_configuration_summary(verbose: bool = False) -> Dict[str, Any]:
    """
    Obtiene un resumen de la configuración de LocalStack.

    Args:
        verbose: Mostrar información detallada

    Returns:
        Dict[str, Any]: Resumen de configuración
    """
    summary = {
        'running': False,
        'services': {},
        'apis': [],
        'functions': [],
        'endpoints': {}
    }

    try:
        # Verificar si LocalStack está corriendo
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=localstack", "--format", "{{.Names}}"],
            capture_output=True,
            text=True
        )

        if "localstack" in result.stdout:
            summary['running'] = True

            # Obtener información de servicios
            summary['services'] = check_localstack_services_status(verbose)

            # Obtener endpoints
            summary['endpoints'] = get_localstack_endpoints(verbose=False)

            if verbose:
                print("📊 Resumen LocalStack:")
                print(f"  Estado: {'✅ Corriendo' if summary['running'] else '❌ Detenido'}")
                print(f"  Servicios disponibles: {sum(summary['services'].values())}/{len(summary['services'])}")

    except Exception as e:
        if verbose:
            print(f"❌ Error obteniendo configuración LocalStack: {e}")

    return summary


def validate_localstack_setup(project_path: str, verbose: bool = False) -> Dict[str, List[str]]:
    """
    Valida la configuración de LocalStack.

    Args:
        project_path: Ruta del proyecto
        verbose: Mostrar información detallada

    Returns:
        Dict[str, List[str]]: Resultados de validación
    """
    validation = {
        'errors': [],
        'warnings': [],
        'recommendations': []
    }

    # Verificar si LocalStack está configurado
    summary = get_localstack_configuration_summary(verbose=False)

    if not summary['running']:
        validation['errors'].append("LocalStack no está corriendo")
    else:
        # Verificar servicios
        services = summary['services']
        inactive_services = [name for name, status in services.items() if not status]

        if inactive_services:
            validation['warnings'].append(f"Servicios LocalStack inactivos: {', '.join(inactive_services)}")

        if services.get('apigateway') and services.get('lambda'):
            validation['recommendations'].append("LocalStack configurado correctamente para API Gateway + Lambda")

    # Verificar archivos de configuración
    from docker.dockerfile_manager import find_lambda_api_gateway_configs
    lambda_configs = find_lambda_api_gateway_configs(project_path, verbose=False)

    if not lambda_configs:
        validation['warnings'].append("No se encontraron configuraciones de Lambda para LocalStack")

    return validation