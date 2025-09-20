import os
from pathlib import Path
import sys
from typing import Any, Dict

# Añadir utils al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.flags_to_dict import set_default_values
from utils.flags_to_dict import validate_allowed_flags


def flag(flags_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Procesa y valida las flags del script code_conformance.

    Valida las configuraciones de entrada para el análisis de conformance
    de código, asegurando que se usen flags válidas y valores apropiados.

    Parameters
    ----------
    flags_dict : dict
        Diccionario de flags ya procesado por run.py

    Returns
    -------
    dict
        Diccionario validado con valores por defecto

    Raises
    ------
    ValueError
        Si las flags no son válidas o tienen valores incorrectos

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    # Definir flags permitidas
    allowed_flags = [
        'mode',                    # Modo de archivos a verificar (opcional)
        'files',                   # Lista de archivos específicos a verificar (opcional, mutuamente excluyente con mode)
        'languages',               # Lenguajes a analizar: js,ts,py,md,json,yml (NEW)
        'verbose',                 # Mostrar información detallada
        'project_path',            # Ruta del proyecto (auto-detect si no se especifica)
        'output_format',           # Formato de salida (console, json, html)
        'output_location',         # Ubicación del archivo de salida (ruta relativa o absoluta)
        'target_folder',           # Carpeta específica a analizar (relativa o absoluta)
        'exclude_paths',           # Paths/directorios a excluir del análisis
        'help',                     # Siempre incluir help
    ]

    # Definir valores por defecto con tipos apropiados
    defaults = {
        'languages': [],           # Auto-detect por defecto (detecta de archivos)
        'verbose': False,          # Sin verbose por defecto
        'project_path': '',        # Auto-detect por defecto
        'output_format': 'console', # Por defecto mostrar en consola
        'output_location': '',     # Sin archivo de salida por defecto
        'target_folder': '',       # Sin carpeta específica por defecto
        'exclude_paths': '',       # Sin exclusiones por defecto
    }

    # Validar flags permitidas
    validate_allowed_flags(flags_dict, allowed_flags)

    # Aplicar valores por defecto
    flags_dict = set_default_values(flags_dict, defaults)

    # Validación: Debe tener o 'mode' o 'files', pero no ambos
    has_mode = 'mode' in flags_dict and flags_dict.get('mode')
    has_files = 'files' in flags_dict and flags_dict.get('files')

    if not has_mode and not has_files:
        raise ValueError(
            "Debe especificar o '--mode' o '--files', pero no ninguna de las dos.\n"
            "   📋 Opciones válidas:\n"
            "   📁 --mode=\"changed\" para archivos modificados\n"
            "   📄 --files=\"path/file1.py path/file2.py\" para archivos específicos\n"
            "   💡 Ejemplo: --mode=\"staged\" o --files=\"easy_pay/models.py\""
        )

    if has_mode and has_files:
        raise ValueError(
            "No puede usar '--mode' y '--files' al mismo tiempo.\n"
            "   ❌ Son opciones mutuamente excluyentes\n"
            "   📋 Use:\n"
            "   📁 --mode=\"changed\" para archivos por modo git, O\n"
            "   📄 --files=\"archivo1.py archivo2.py\" para archivos específicos\n"
            "   💡 Elija una de las dos opciones"
        )

    # Validar modo específico si se proporciona
    if has_mode:
        valid_modes = ['all', 'changed', 'staged', 'unstaged', 'stash', 'unmerged']
        if flags_dict['mode'] not in valid_modes:
            raise ValueError(
                f"El modo '{flags_dict['mode']}' no existe.\n"
                f"   📋 Modos disponibles: {', '.join(valid_modes)}\n"
                f"   💡 Ejemplo: --mode=\"changed\" para archivos modificados",
            )

    # Validar archivos específicos si se proporcionan
    if has_files:
        files_list = flags_dict['files']

        # Si 'files' es un string, convertir a lista separando por espacios
        if isinstance(files_list, str):
            files_list = [f.strip() for f in files_list.split() if f.strip()]
            flags_dict['files'] = files_list

        if not files_list:
            raise ValueError(
                "La flag '--files' no puede estar vacía.\n"
                "   📄 Debe especificar uno o más archivos de código\n"
                "   💡 Ejemplo: --files=\"src/main.py src/utils.js styles.css\""
            )

        # Validar que cada archivo existe y es de tipo soportado
        project_path = Path(flags_dict.get('project_path', '.'))
        invalid_files = []
        unsupported_files = []

        # Mapeo de extensiones a lenguajes
        extension_to_language = {
            '.py': 'py', '.pyi': 'py', '.pyx': 'py',
            '.js': 'js', '.mjs': 'js', '.cjs': 'js',
            '.ts': 'ts', '.tsx': 'tsx', '.jsx': 'jsx',
            '.md': 'md', '.markdown': 'md',
            '.json': 'json', '.json5': 'json',
            '.yml': 'yml', '.yaml': 'yaml',
            '.html': 'html', '.htm': 'html',
            '.css': 'css', '.scss': 'scss', '.sass': 'scss',
            '.vue': 'vue'
        }

        for file_path in files_list:
            file_full_path = project_path / file_path

            if not file_full_path.exists():
                invalid_files.append(file_path)
            elif not file_full_path.is_file():
                invalid_files.append(f"{file_path} (es una carpeta, no un archivo)")
            else:
                # Verificar si la extensión está soportada
                file_extension = Path(file_path).suffix.lower()
                if file_extension not in extension_to_language:
                    unsupported_files.append(file_path)

        if invalid_files:
            raise ValueError(
                "Archivos no encontrados o inválidos:\n"
                + "\n".join([f"   ❌ {f}" for f in invalid_files]) +
                "\n   💡 Verifique que los paths sean correctos desde la raíz del proyecto"
            )

        if unsupported_files:
            supported_extensions = ', '.join(sorted(extension_to_language.keys()))
            raise ValueError(
                "Archivos con extensiones no soportadas:\n"
                + "\n".join([f"   ⚠️  {f}" for f in unsupported_files]) +
                f"\n   📄 Extensiones soportadas: {supported_extensions}\n"
                "   💡 Use archivos con extensiones válidas"
            )

    # Validar project_path si se proporciona
    if flags_dict['project_path'] and not Path(flags_dict['project_path']).exists():
        raise ValueError(f"La ruta del proyecto '{flags_dict['project_path']}' no existe")

    # Validar formato de salida específico
    valid_formats = ['console', 'json', 'html']
    if flags_dict['output_format'] not in valid_formats:
        raise ValueError(
            f"El formato '{flags_dict['output_format']}' no es válido.\n"
            f"   📋 Formatos disponibles: {', '.join(valid_formats)}\n"
            f"   💡 Ejemplo: --output-format=\"json\" para archivo JSON",
        )

    # Validar output_location si se proporciona
    if flags_dict['output_location']:
        output_path = Path(flags_dict['output_location'])
        # Si es ruta relativa, no validar existencia del directorio padre
        # Si es ruta absoluta, validar que el directorio padre exista
        if output_path.is_absolute() and not output_path.parent.exists():
            raise ValueError(f"El directorio padre '{output_path.parent}' no existe para output_location")

    # Validar que output_location se especifique cuando el formato es HTML (JSON puede ir a stdout)
    if flags_dict['output_format'] == 'html' and not flags_dict['output_location']:
        raise ValueError(
            "El formato HTML requiere especificar dónde guardar el archivo.\n"
            "   📁 Usa --output-location=\"ruta/al/archivo.html\"\n"
            "   💡 Ejemplo: --output-location=\"reports/conformance.html\"",
        )

    # Si output_location se especifica pero el formato es console, cambiar formato a json
    if flags_dict['output_location'] and flags_dict['output_format'] == 'console':
        flags_dict['output_format'] = 'json'
        if flags_dict.get('verbose'):
            print("INFO: Cambiando formato a 'json' porque se especificó output-location")

    # Validar target_folder si se proporciona
    if flags_dict['target_folder']:
        target_path = Path(flags_dict['target_folder'])
        # Si es ruta relativa, convertir a absoluta basada en project_path
        if not target_path.is_absolute():
            project_path = Path(flags_dict.get('project_path', '.'))
            target_path = project_path / target_path

        if not target_path.exists():
            raise ValueError(
                f"La carpeta objetivo '{flags_dict['target_folder']}' no existe.\n"
                f"   📁 Ruta completa: {target_path}\n"
                f"   💡 Verifica que la carpeta exista o usa una ruta correcta",
            )

        if not target_path.is_dir():
            raise ValueError(
                f"La ruta '{flags_dict['target_folder']}' no es una carpeta.\n"
                f"   📁 Es un archivo: {target_path}\n"
                f"   💡 Especifica una carpeta, no un archivo",
            )

    # Validar exclude_paths si se proporciona
    if flags_dict['exclude_paths']:
        exclude_paths_list = flags_dict['exclude_paths']

        # Si es un string, convertir a lista separando por comas o espacios
        if isinstance(exclude_paths_list, str):
            # Separar por comas primero, luego por espacios
            exclude_paths_list = [p.strip() for p in exclude_paths_list.replace(',', ' ').split() if p.strip()]
            flags_dict['exclude_paths'] = exclude_paths_list

        if not exclude_paths_list:
            raise ValueError(
                "La flag '--exclude-paths' no puede estar vacía.\n"
                "   📁 Debe especificar uno o más paths/directorios a excluir\n"
                "   💡 Ejemplo: --exclude-paths=\"tests migrations\" o --exclude-paths=\"tests,migrations\""
            )

    # Validar languages si se proporciona
    if flags_dict['languages']:
        languages_list = flags_dict['languages']

        # Si es un string, convertir a lista separando por comas
        if isinstance(languages_list, str):
            languages_list = [lang.strip().lower() for lang in languages_list.split(',') if lang.strip()]
            flags_dict['languages'] = languages_list

        # Lista de lenguajes soportados
        supported_languages = ['js', 'ts', 'py', 'md', 'json', 'yml', 'yaml', 'html', 'css', 'scss', 'vue', 'jsx', 'tsx']

        # Validar que todos los lenguajes estén soportados
        invalid_languages = [lang for lang in languages_list if lang not in supported_languages]
        if invalid_languages:
            raise ValueError(
                f"Lenguajes no soportados: {', '.join(invalid_languages)}\n"
                f"   📋 Lenguajes disponibles: {', '.join(supported_languages)}\n"
                f"   💡 Ejemplo: --languages=\"js,ts\" o --languages=\"py,md,json\""
            )

        if flags_dict.get('verbose'):
            print(f"🔧 Lenguajes especificados: {', '.join(languages_list)}")

    # Mostrar flags procesadas para debug (opcional)
    if flags_dict.get('verbose'):
        print("Flags procesadas:")
        for flag_name, flag_value in flags_dict.items():
            if flag_value and flag_name != 'help':
                display_name = flag_name.replace('_', '-')
                if flag_name == 'files' and isinstance(flag_value, list):
                    print(f"  --{display_name}: {len(flag_value)} archivo(s) -> {', '.join(flag_value[:3])}")
                    if len(flag_value) > 3:
                        print(f"                        ... y {len(flag_value) - 3} más")
                else:
                    print(f"  --{display_name}: {flag_value}")

    return flags_dict
