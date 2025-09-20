import os
import sys
from typing import Any, Dict, List

from utils.flags_to_dict import set_default_values
from utils.flags_to_dict import validate_allowed_flags

# Añadir el directorio padre al path para poder importar utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def get_valid_git_modes() -> List[str]:
    """
    Obtiene lista de modos git válidos.

    Devuelve los modos git soportados para filtrado de archivos
    por diferentes estados en el repositorio.

    Returns
    -------
    List[str]
        Lista de modos git válidos como 'changed', 'staged', 'unstaged', etc.

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    return ['changed', 'staged', 'unstaged', 'stash', 'unmerged', 'all']


def flag(flags_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Procesa y valida las flags para el script structure_folder_n_files.

    Valida y procesa las configuraciones para la visualización de estructura
    de archivos y carpetas del proyecto, incluyendo filtros y modos git.

    Flags soportadas incluyen filtros de extensiones, modos git, exclusiones
    de archivos vacíos, patrones regex y opciones de formato de salida.

    Parameters
    ----------
    flags_dict : dict
        Diccionario de flags ya procesado por run.py

    Returns
    -------
    dict
        Diccionario con las flags procesadas y validadas con valores por defecto

    Raises
    ------
    ValueError
        Si se usan flags no permitidas o valores inválidos

    Examples
    --------
    >>> flag({'include_ignored': True, 'only_extension': 'py'})
    >>> flag({'git_mode': 'unmerged', 'exclude_empty': True})

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    # Definir flags permitidas
    allowed_flags = [
        'include_ignored',
        'excludes_extension',
        'only_extension',
        'only_folders_root',
        'only_list',
        'include_deleted',
        'exclude_empty',
        'ignore_patterns',
        'git_mode',
        'help',  # Agregar help como flag permitida,
        # Nota: '_invoked_from' es una flag del sistema, automáticamente válida
    ]

    # Definir valores por defecto - por defecto EXCLUIR archivos ignorados
    defaults = {
        'include_ignored': False,  # Por defecto NO incluir ignorados
        'excludes_extension': [],
        'only_extension': [],
        'only_folders_root': False,
        'only_list': False,  # Por defecto formato visual
        'include_deleted': False,  # Por defecto NO incluir archivos eliminados
        'exclude_empty': False,  # Por defecto NO excluir archivos vacíos
        'ignore_patterns': [],  # Por defecto NO ignorar patrones específicos
        'git_mode': None,  # Por defecto NO usar modo git específico
        '_invoked_from': 'python',  # Por defecto asume invocación desde Python
    }

    # Validar flags permitidas
    validate_allowed_flags(flags_dict, allowed_flags)

    # Establecer valores por defecto
    flags_dict = set_default_values(flags_dict, defaults)

    # Validar git_mode si se especifica
    if flags_dict.get('git_mode'):
        valid_git_modes = ['changed', 'staged', 'unstaged', 'stash', 'unmerged', 'all']
        if flags_dict['git_mode'] not in valid_git_modes:
            raise ValueError(
                f'git_mode debe ser uno de: {", ".join(valid_git_modes)}. Recibido: {flags_dict["git_mode"]}',
            )

    # Validaciones adicionales específicas
    if flags_dict.get('excludes_extension'):
        # Asegurar que excludes_extension sea siempre una lista
        if isinstance(flags_dict['excludes_extension'], str):
            flags_dict['excludes_extension'] = [flags_dict['excludes_extension']]

        # Validar que las extensiones no empiecen con punto
        cleaned_extensions = []
        for ext in flags_dict['excludes_extension']:
            # Remover punto inicial si existe
            if ext.startswith('.'):
                ext = ext[1:]
            cleaned_extensions.append(ext.lower())
        flags_dict['excludes_extension'] = cleaned_extensions

    if flags_dict.get('only_extension'):
        # Asegurar que only_extension sea siempre una lista
        if isinstance(flags_dict['only_extension'], str):
            flags_dict['only_extension'] = [flags_dict['only_extension']]

        # Validar que las extensiones no empiecen con punto
        cleaned_extensions = []
        for ext in flags_dict['only_extension']:
            # Remover punto inicial si existe
            if ext.startswith('.'):
                ext = ext[1:]
            cleaned_extensions.append(ext.lower())
        flags_dict['only_extension'] = cleaned_extensions

        # Validación: no se puede usar only_extension junto con excludes_extension
        if flags_dict.get('excludes_extension'):
            raise ValueError('No se puede usar --only-extension junto con --excludes-extension. Use una u otra.')

    # Validar ignore_patterns si se especifica
    if flags_dict.get('ignore_patterns'):
        # Asegurar que ignore_patterns sea siempre una lista
        if isinstance(flags_dict['ignore_patterns'], str):
            # Si es string, dividir por | para obtener múltiples patrones
            flags_dict['ignore_patterns'] = [
                pattern.strip() for pattern in flags_dict['ignore_patterns'].split('|') if pattern.strip()
            ]

        # Validar que los patrones no estén vacíos
        valid_patterns = []
        for pattern in flags_dict['ignore_patterns']:
            if pattern and pattern.strip():
                valid_patterns.append(pattern.strip())

        flags_dict['ignore_patterns'] = valid_patterns

    # Mostrar información de las flags procesadas solo si NO es modo lista
    if not flags_dict.get('only_list', False):
        print('Flags procesadas:')
        for flag_name, flag_value in flags_dict.items():
            if flag_value and flag_name != 'help':  # Solo mostrar flags activas o con valores
                if isinstance(flag_value, list) and flag_value:
                    print(f'  --{flag_name.replace("_", "-")}: {", ".join(flag_value)}')
                elif flag_value is True:
                    print(f'  --{flag_name.replace("_", "-")}')
                elif flag_value:  # Para strings y otros valores no vacíos
                    print(f'  --{flag_name.replace("_", "-")}: {flag_value}')

    return flags_dict
