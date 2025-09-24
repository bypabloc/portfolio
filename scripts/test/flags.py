import sys
import os

# Añadir utils al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.flags_to_dict import validate_allowed_flags, set_default_values

def flag(flags_dict):
    """
    Procesa y valida las flags del script de testing de base de datos.

    Args:
        flags_dict (dict): Diccionario de flags ya procesado por run.py

    Returns:
        dict: Diccionario validado con valores por defecto
    """
    # Definir flags permitidas
    allowed_flags = [
        'endpoint',         # Endpoint específico a probar
        'query',           # Query SQL personalizada
        'verbose',         # Mostrar información detallada
        'timeout',         # Timeout para requests
        'url',             # URL base del API Gateway
        'user',            # Usuario de autenticación
        'password',        # Password de autenticación
        'help'             # Ayuda
    ]

    # Definir valores por defecto
    defaults = {
        'endpoint': 'test-all',                    # Test completo por defecto
        'query': '',                               # Sin query por defecto
        'verbose': False,                          # Sin verbose por defecto
        'timeout': 30,                            # 30 segundos de timeout
        'url': 'http://localhost:4321',           # URL del API Gateway
        'user': 'admin',                          # Usuario por defecto
        'password': 'portfolio_admin'             # Password por defecto
    }

    # Validar flags permitidas
    validate_allowed_flags(flags_dict, allowed_flags)

    # Aplicar valores por defecto
    flags_dict = set_default_values(flags_dict, defaults)

    # Validación específica de endpoint
    valid_endpoints = ['health', 'info', 'tables', 'query', 'test-all']
    if flags_dict['endpoint'] not in valid_endpoints:
        raise ValueError(f"Endpoint '{flags_dict['endpoint']}' no válido. Opciones: {', '.join(valid_endpoints)}")

    # Validación de query cuando endpoint es 'query'
    if flags_dict['endpoint'] == 'query' and not flags_dict['query']:
        raise ValueError("Flag --query es requerida cuando --endpoint='query'")

    # Convertir timeout a int si es string
    if isinstance(flags_dict['timeout'], str):
        try:
            flags_dict['timeout'] = int(flags_dict['timeout'])
        except ValueError:
            raise ValueError(f"Timeout debe ser un número, recibido: {flags_dict['timeout']}")

    # Mostrar configuración si verbose está habilitado
    if flags_dict.get('verbose'):
        print("🔧 Configuración de database testing:")
        print(f"  🎯 Endpoint: {flags_dict['endpoint']}")
        print(f"  🌐 URL: {flags_dict['url']}")
        print(f"  👤 Usuario: {flags_dict['user']}")
        print(f"  ⏱️  Timeout: {flags_dict['timeout']}s")
        if flags_dict['query']:
            print(f"  📝 Query: {flags_dict['query']}")
        print()

    return flags_dict