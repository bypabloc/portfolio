import sys
import os

# Añadir utils y src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from utils.flags_to_dict import validate_allowed_flags, set_default_values
from config.flag_processor import (
    process_all_flags,
    get_allowed_flags,
    get_default_values
)
from display.flag_display import show_flag_configuration


def flag(flags_dict):
    """
    Procesa y valida las flags del script setup con arquitectura modular.

    Args:
        flags_dict (dict): Diccionario de flags ya procesado por run.py

    Returns:
        dict: Diccionario completamente validado y procesado
    """
    # Obtener configuración básica desde módulos especializados
    allowed_flags = get_allowed_flags()
    defaults = get_default_values()

    # Validaciones básicas
    validate_allowed_flags(flags_dict, allowed_flags)
    flags_dict = set_default_values(flags_dict, defaults)

    # Procesamiento complejo delegado a módulo especializado
    flags_dict = process_all_flags(flags_dict)

    # Mostrar configuración usando módulo de display
    show_flag_configuration(flags_dict)

    return flags_dict