#!/usr/bin/env python3

import importlib.util
from pathlib import Path
import sys
import traceback
from typing import Any, Dict, List
from types import ModuleType

from utils.flags_to_dict import flags_to_dict

# Añadir utils al path para usar flags_to_dict
sys.path.append(str(Path(__file__).parent / 'utils'))


def load_module_from_path(module_name: str, file_path: str) -> ModuleType:
    """
    Carga un módulo desde una ruta específica.

    Utiliza importlib para cargar dinámicamente un módulo Python
    desde un path de archivo específico.

    Parameters
    ----------
    module_name : str
        Nombre del módulo a cargar
    file_path : str or Path
        Ruta al archivo .py del módulo

    Returns
    -------
    module
        Módulo cargado dinámicamente

    Raises
    ------
    ImportError
        Si no se puede cargar el módulo desde la ruta especificada

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(f'No se pudo cargar el módulo desde {file_path}')

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def discover_valid_scripts() -> List[str]:
    """
    Descubre todos los scripts válidos en el directorio scripts/.

    Escanea el directorio scripts/ para encontrar subdirectorios que contengan
    la estructura requerida (main.py, flags.py, README.md) con contenido válido.

    Returns
    -------
    List[str]
        Lista de nombres de scripts válidos encontrados, ordenados alfabéticamente

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    scripts_dir = Path(__file__).parent
    valid_scripts = []

    for item in scripts_dir.iterdir():
        if item.is_dir() and item.name != 'utils' and not item.name.startswith('.'):
            main_py = item / 'main.py'
            flags_py = item / 'flags.py'
            readme_md = item / 'README.md'

            # Verificar que tenga la estructura requerida
            if main_py.exists() and flags_py.exists() and readme_md.exists():
                # Verificar que README.md tenga contenido
                try:
                    with open(readme_md, encoding='utf-8') as f:
                        content = f.read().strip()
                        if content:  # Solo scripts con README no vacío
                            valid_scripts.append(item.name)
                except (OSError, UnicodeDecodeError, PermissionError) as e:
                    # Log la excepción antes de continuar para mejor debugging
                    print(f"⚠️  Error leyendo README para {item.name}: {type(e).__name__}", file=sys.stderr)
                    continue  # Ignorar si hay error leyendo README

    return sorted(valid_scripts)


def show_global_help() -> None:
    """
    Muestra la ayuda global con todos los scripts disponibles.

    Presenta una lista formateada de todos los scripts válidos disponibles
    en el sistema, leyendo su documentación desde los archivos README.md.

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    print('=== Scripts System - Ayuda Global ===')
    print()
    print('Uso: python scripts/run.py <script> [flags...]')
    print()

    valid_scripts = discover_valid_scripts()

    if not valid_scripts:
        print('No se encontraron scripts válidos.')
        return

    print('Scripts disponibles:')
    print('-' * 40)

    for script_name in valid_scripts:
        try:
            # Leer el README.md del script
            script_dir = Path(__file__).parent / script_name
            readme_path = script_dir / 'README.md'

            with open(readme_path, encoding='utf-8') as f:
                content = f.read().strip()

            print(f'\n📁 {script_name}:')
            print(content)

        except (OSError, UnicodeDecodeError, PermissionError) as e:
            print(f'\n📁 {script_name}: (Error leyendo documentación: {e})')

    print('\n' + '=' * 50)
    print('Para ayuda específica de un script: python scripts/run.py <script> --help')


def main() -> None:
    """
    Ejecutor principal del sistema de scripts.

    Punto de entrada principal que maneja la selección de scripts,
    procesamiento de argumentos, validación y ejecución dinámica.
    Implementa el patrón de delegación para scripts modulares.

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    # Verificar si se solicitó ayuda global
    if len(sys.argv) == 2 and sys.argv[1] == '--help':
        show_global_help()
        sys.exit(0)

    if len(sys.argv) < 2:
        print('Uso: python scripts/run.py <script> [flags...]')
        print('      python scripts/run.py --help  (para ver todos los scripts)')
        sys.exit(1)

    script_folder = sys.argv[1]
    raw_flags_args = sys.argv[2:]  # El resto de argumentos son flags

    # Convertir flags a diccionario centralizadamente
    flags_dict = flags_to_dict(raw_flags_args)

    # Verificar si se solicitó ayuda específica del script
    if flags_dict.get('help', False):
        # Mostrar ayuda específica del script
        try:
            scripts_dir = Path(__file__).parent
            script_dir = scripts_dir / script_folder
            readme_path = script_dir / 'README.md'

            if not script_dir.exists():
                print(f"Error: La carpeta '{script_folder}' no existe en scripts/")
                sys.exit(1)

            if not readme_path.exists():
                print(f"Error: No se encontró 'README.md' en scripts/{script_folder}/")
                print('El script debe tener un archivo README.md con documentación')
                sys.exit(1)

            # Leer y mostrar el README.md
            with open(readme_path, encoding='utf-8') as f:
                content = f.read().strip()

            if not content:
                print(f'Error: README.md está vacío en scripts/{script_folder}/')
                sys.exit(1)

            print(f"=== Ayuda para '{script_folder}' ===")
            print()
            print(content)

        except (OSError, UnicodeDecodeError, PermissionError) as e:
            print(f'Error mostrando ayuda del script: {e}')

        sys.exit(0)

    # Construir las rutas de los archivos
    scripts_dir = Path(__file__).parent
    script_dir = scripts_dir / script_folder
    main_py_path = script_dir / 'main.py'
    flags_py_path = script_dir / 'flags.py'
    readme_path = script_dir / 'README.md'

    # Verificar que existan los archivos requeridos
    if not script_dir.exists():
        print(f"Error: La carpeta '{script_folder}' no existe en scripts/")
        valid_scripts = discover_valid_scripts()
        if valid_scripts:
            print('Scripts disponibles:', ', '.join(valid_scripts))
        else:
            print('No hay scripts válidos disponibles.')
        sys.exit(1)

    if not main_py_path.exists():
        print(f"Error: No se encontró 'main.py' en scripts/{script_folder}/")
        print('Un script válido debe tener: main.py, flags.py y README.md')
        sys.exit(1)

    if not flags_py_path.exists():
        print(f"Error: No se encontró 'flags.py' en scripts/{script_folder}/")
        print('Un script válido debe tener: main.py, flags.py y README.md')
        sys.exit(1)

    if not readme_path.exists():
        print(f"Error: No se encontró 'README.md' en scripts/{script_folder}/")
        print('Un script válido debe tener: main.py, flags.py y README.md')
        sys.exit(1)

    # Verificar que README.md tenga contenido
    try:
        with open(readme_path, encoding='utf-8') as f:
            readme_content = f.read().strip()
            if not readme_content:
                print(f'Error: README.md está vacío en scripts/{script_folder}/')
                print('El README.md debe contener la documentación del script')
                sys.exit(1)
    except (OSError, UnicodeDecodeError, PermissionError) as e:
        print(f'Error leyendo README.md: {e}')
        sys.exit(1)

    try:
        # Cargar el módulo flags
        flags_module = load_module_from_path(f'{script_folder}_flags', flags_py_path)

        # Verificar que exista la función flag
        if not hasattr(flags_module, 'flag'):
            print(f"Error: No se encontró la función 'flag' en {flags_py_path}")
            sys.exit(1)

        # Verificar si es modo silencioso (--only-list) para no mostrar mensajes
        is_silent_mode = flags_dict.get('only_list', False)

        # Agregar indicador de origen CLI
        flags_dict['_invoked_from'] = 'cli'

        # Procesar las flags (ahora pasamos el dict en lugar de la lista)
        if not is_silent_mode:
            print(f'Procesando flags para {script_folder}...')

        try:
            parsed_flags = flags_module.flag(flags_dict)
        except ValueError as e:
            # Manejo amigable de errores de validación
            error_msg = str(e)
            print("\n❌ Error en la configuración:")
            print(f"   {error_msg}")
            print("\n💡 Para ver la ayuda completa, usa:")
            print(f"   python scripts/run.py {script_folder} --help")
            sys.exit(1)

        # Cargar el módulo main
        main_module = load_module_from_path(f'{script_folder}_main', main_py_path)

        # Verificar que exista la función main
        if not hasattr(main_module, 'main'):
            print(f"Error: No se encontró la función 'main' en {main_py_path}")
            sys.exit(1)

        # Ejecutar la función main con las flags procesadas
        if not is_silent_mode:
            print(f'Ejecutando {script_folder}...')
            print('-' * 50)
        main_module.main(parsed_flags)

    except (ImportError, AttributeError, ValueError, TypeError, OSError) as e:
        print(f'Error ejecutando el script: {e}')
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
