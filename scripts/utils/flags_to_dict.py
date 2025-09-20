from typing import Any, Dict, List, Union


def flags_to_dict(args_list: List[str]) -> Dict[str, Union[str, List[str], bool]]:
    """
    Convierte una lista de argumentos de línea de comandos a un diccionario de Python.

    Parsea argumentos estilo --flag y --flag=value, manejando valores booleanos,
    strings y listas separadas por pipes. Convierte guiones a guiones bajos
    para compatibilidad con Python.

    Parameters
    ----------
    args_list : list
        Lista de argumentos de línea de comandos

    Returns
    -------
    dict
        Diccionario con las flags parseadas con nombres normalizados

    Examples
    --------
    >>> flags_to_dict(['--only-folders-root'])
    {'only_folders_root': True}
    >>> flags_to_dict(['--excludes-extension="json|csv"'])
    {'excludes_extension': ['json', 'csv']}
    >>> flags_to_dict(['--excludes-files-ignored', '--only-folders-root'])
    {'excludes_files_ignored': True, 'only_folders_root': True}

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    flags_dict = {}

    for arg in args_list:
        if not arg.startswith('--'):
            continue

        # Remover el prefijo --
        arg = arg[2:]

        # Verificar si tiene un valor asignado con =
        if '=' in arg:
            flag_name, flag_value = arg.split('=', 1)

            # Remover comillas si están presentes
            if (
                (flag_value.startswith('"') and flag_value.endswith('"'))
                or (flag_value.startswith("'") and flag_value.endswith("'"))
            ):
                flag_value = flag_value[1:-1]

            # Convertir guiones a guiones bajos
            flag_name = flag_name.replace('-', '_')

            # Si contiene separadores "|", convertir a lista
            if '|' in flag_value:
                flag_value = flag_value.split('|')

            flags_dict[flag_name] = flag_value
        else:
            # Flag booleana (solo presence/absence)
            flag_name = arg.replace('-', '_')
            flags_dict[flag_name] = True

    return flags_dict


def validate_required_flags(flags_dict: Dict[str, Any], required_flags: List[str]) -> None:
    """
    Valida que todas las flags requeridas estén presentes.

    Verifica que el diccionario de flags contenga todas las flags
    marcadas como obligatorias para la ejecución del script.

    Parameters
    ----------
    flags_dict : dict
        Diccionario de flags a validar
    required_flags : list
        Lista de nombres de flags que son obligatorias

    Raises
    ------
    ValueError
        Si falta alguna flag requerida en el diccionario

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    missing_flags = []

    for flag in required_flags:
        if flag not in flags_dict:
            missing_flags.append(flag)

    if missing_flags:
        raise ValueError(f'Flags requeridas faltantes: {", ".join(missing_flags)}')


def validate_allowed_flags(flags_dict: Dict[str, Any], allowed_flags: List[str]) -> None:
    """
    Valida que solo se usen flags permitidas.

    Verifica que todas las flags en el diccionario estén en la lista
    de flags permitidas, rechazando flags no reconocidas para evitar errores.

    Parameters
    ----------
    flags_dict : dict
        Diccionario de flags a validar
    allowed_flags : list
        Lista de nombres de flags que están permitidas

    Raises
    ------
    ValueError
        Si hay flags no permitidas en el diccionario

    Note
    ----
    Las flags del sistema (como '_invoked_from') son siempre válidas

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    # Flags del sistema que son siempre válidas
    system_flags = ['_invoked_from']

    invalid_flags = []

    for flag in flags_dict:
        if flag not in allowed_flags and flag not in system_flags:
            invalid_flags.append(flag)

    if invalid_flags:
        raise ValueError(f'Flags no permitidas: {", ".join(invalid_flags)}')


def set_default_values(flags_dict: Dict[str, Any], defaults: Dict[str, Any]) -> Dict[str, Any]:
    """
    Establece valores por defecto para flags no especificadas.

    Añade valores por defecto al diccionario de flags para aquellas
    flags que no fueron especificadas por el usuario.

    Parameters
    ----------
    flags_dict : dict
        Diccionario de flags existente
    defaults : dict
        Diccionario con valores por defecto para flags

    Returns
    -------
    dict
        Diccionario actualizado con valores por defecto aplicados

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    for flag, default_value in defaults.items():
        if flag not in flags_dict:
            flags_dict[flag] = default_value

    return flags_dict
