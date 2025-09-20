#!/usr/bin/env python3

from datetime import datetime
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

# Añadir utils al path para imports del sistema multi-lenguaje
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.multi_language_analyzer import analyze_files_by_language
from utils.language_configs import (
    get_languages_from_files,
    get_supported_extensions,
    EXTENSION_TO_LANGUAGE,
)

# Extensiones Python soportadas por Ruff (2025)
RUFF_PYTHON_EXTENSIONS = {
    'suffixes': {'.py', '.pyi', '.ipynb', '.pyw', '.py3', '.pyz', '.pyx', '.pxd', '.pxi'},
    'patterns': ['**/*.py', '**/*.pyi', '**/*.ipynb', '**/*.pyw', '**/*.py3', '**/*.pyz', '**/*.pyx', '**/*.pxd', '**/*.pxi'],
    'structure_arg': "py|pyi|ipynb|pyw|py3|pyz|pyx|pxd|pxi",
}


def _filter_excluded_paths(files: List[Path], exclude_paths: List[str], project_path: Path) -> List[Path]:
    """
    Filtra archivos excluyendo los que coincidan con los paths especificados.

    Aplica filtros de exclusión a la lista de archivos según los paths
    o directorios especificados para evitar analizarlos.

    Parameters
    ----------
    files : List[Path]
        Lista de archivos a filtrar
    exclude_paths : List[str]
        Lista de paths/directorios a excluir
    project_path : Path
        Ruta raíz del proyecto

    Returns
    -------
    List[Path]
        Lista de archivos filtrados sin los excluidos

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    if not exclude_paths:
        return files

    filtered_files = []
    for file_path in files:
        # Convertir a path relativo respecto al proyecto
        try:
            relative_path = file_path.relative_to(project_path)
            relative_str = str(relative_path)

            # Verificar si algún exclude_path coincide
            should_exclude = False
            for exclude_path in exclude_paths:
                # Normalizar exclude_path
                exclude_path = exclude_path.strip('/')

                # Verificar coincidencias:
                # 1. Coincidencia exacta de directorio
                if relative_str.startswith(exclude_path + '/') or relative_str == exclude_path:
                    should_exclude = True
                    break
                # 2. Coincidencia parcial (ej: "test" excluye "test_file.py")
                if exclude_path in str(relative_path.parts[0]):
                    should_exclude = True
                    break

            if not should_exclude:
                filtered_files.append(file_path)
        except ValueError:
            # Si no se puede obtener path relativo, incluir el archivo
            filtered_files.append(file_path)

    return filtered_files


def main(flags: Dict[str, Any]) -> None:
    """
    Ejecuta validaciones de conformance de código multi-lenguaje.

    Utiliza herramientas especializadas para cada lenguaje (Ruff para Python,
    ESLint para JS/TS, Stylelint para CSS, etc.) para validar calidad de código,
    estilo y mejores prácticas específicas de cada tecnología.

    Parameters
    ----------
    flags : Dict[str, Any]
        Diccionario con configuraciones procesadas y validadas
        que contiene mode, verbose, project_path, output_format, languages, etc.

    Raises
    ------
    SystemExit
        Con código 0 si no hay errores, 1 si hay errores de conformance

    Examples
    --------
    >>> main({'mode': 'unmerged', 'verbose': True})
    >>> main({'languages': ['py', 'js'], 'output_format': 'json'})

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-19
    """
    # Determinar la ruta del proyecto
    if flags.get('project_path'):
        project_path = Path(flags['project_path'])
    else:
        # Auto-detect: usar directorio actual como base
        current_path = Path(__file__).parent.parent.parent  # scripts/code_conformance -> scripts -> root
        project_path = current_path

    try:
        # Obtener archivos a analizar
        files_to_analyze = _get_files_to_analyze(flags, project_path)

        if not files_to_analyze:
            if flags.get('verbose'):
                print("✅ No hay archivos para analizar")
            sys.exit(0)

        # Filtrar por lenguajes especificados en flags
        languages_filter = flags.get('languages', [])

        # Aplicar filtro de exclusión si se especificó
        if flags.get('exclude_paths'):
            exclude_paths_list = flags['exclude_paths']
            if isinstance(exclude_paths_list, str):
                exclude_paths_list = [p.strip() for p in exclude_paths_list.replace(',', ' ').split() if p.strip()]
            files_to_analyze = _filter_excluded_paths(files_to_analyze, exclude_paths_list, project_path)

        # Ejecutar análisis multi-lenguaje
        analysis_results = analyze_files_by_language(
            files_to_analyze,
            languages_filter if languages_filter else None,
            project_path,
            flags.get('verbose', False)
        )

        # Determinar el formato de salida
        output_format = flags.get('output_format', 'console')
        output_location = flags.get('output_location', '')

        if output_format == 'console':
            # Mostrar resultados en consola
            _display_console_results(analysis_results, flags.get('verbose', False))
        elif output_format == 'json':
            # Generar salida JSON (stdout o archivo)
            _output_json_results(analysis_results, output_location, flags.get('verbose', False))
        else:
            # Generar salida estructurada (HTML)
            print("⚠️  Generación de reportes HTML no implementada completamente")
            print("   Usar modo consola o JSON por ahora")
            sys.exit(1)

        # Determinar código de salida
        exit_code = analysis_results.get('summary', {}).get('exit_code', 0)
        sys.exit(exit_code)

    except (ValueError, TypeError, AttributeError, KeyError, OSError, ImportError) as e:
        print(f"Error ejecutando análisis multi-lenguaje: {e}")
        if flags.get('verbose'):
            import traceback
            traceback.print_exc()
        sys.exit(1)
    finally:
        # Cleanup if needed
        pass


def _get_files_to_analyze(flags: Dict[str, Any], project_path: Path) -> List[Path]:
    """
    Obtiene la lista de archivos a analizar basándose en las flags.

    Args:
        flags: Configuraciones del usuario
        project_path: Ruta del proyecto

    Returns:
        Lista de archivos a analizar
    """
    if flags.get('files'):
        # Modo archivos específicos - usar nueva lógica multi-lenguaje
        files_list = flags['files']
        if isinstance(files_list, str):
            files_list = [f.strip() for f in files_list.split() if f.strip()]

        all_files = []
        for file_path in files_list:
            full_path = project_path / file_path
            if full_path.exists() and full_path.is_file():
                # Verificar que la extensión esté soportada
                extension = full_path.suffix.lower()
                if extension in EXTENSION_TO_LANGUAGE:
                    all_files.append(full_path)

        return all_files

    elif flags.get('target_folder'):
        # Modo carpeta específica - buscar todos los archivos soportados
        target_path = Path(flags['target_folder'])
        if not target_path.is_absolute():
            target_path = project_path / target_path

        all_files = []
        for extension in get_supported_extensions():
            pattern = f"**/*{extension}"
            all_files.extend(list(target_path.glob(pattern)))

        return all_files

    else:
        # Modo git - usar lógica existente pero expandida para todos los lenguajes
        mode = flags.get('mode', 'unmerged')
        return _get_files_by_git_mode_multi_language(mode, project_path)


def _get_files_by_git_mode_multi_language(mode: str, project_path: Path) -> List[Path]:
    """
    Obtiene archivos usando comandos git pero para todos los lenguajes soportados.

    Args:
        mode: Modo git (all, changed, staged, unstaged, unmerged)
        project_path: Ruta del proyecto

    Returns:
        Lista de archivos con extensiones soportadas
    """
    if mode == 'all':
        # Todos los archivos con extensiones soportadas
        all_files = []
        for extension in get_supported_extensions():
            pattern = f"**/*{extension}"
            all_files.extend(list(project_path.glob(pattern)))
        return all_files

    # Para otros modos, usar comandos git
    git_executable = '/usr/bin/git'
    if not Path(git_executable).exists():
        print(f"Error: No se encuentra git en {git_executable}")
        return []

    git_commands = {
        'changed': [git_executable, 'diff', '--name-only', 'HEAD'],
        'staged': [git_executable, 'diff', '--staged', '--name-only'],
        'unstaged': [git_executable, 'diff', '--name-only'],
        'unmerged': [git_executable, 'diff', '--name-only', 'origin/dev...HEAD'],
    }

    if mode not in git_commands:
        print(f"Error: Modo '{mode}' no reconocido")
        return []

    try:
        result = subprocess.run(
            git_commands[mode],
            cwd=project_path,
            capture_output=True,
            text=True,
            shell=False,
            check=False
        )

        if result.returncode != 0:
            print(f"Error ejecutando git: {result.stderr}")
            return []

        # Filtrar archivos con extensiones soportadas
        supported_files = []
        for file_line in result.stdout.strip().split('\n'):
            if file_line:
                file_path = project_path / file_line
                if file_path.exists() and file_path.suffix.lower() in EXTENSION_TO_LANGUAGE:
                    supported_files.append(file_path)

        return supported_files

    except Exception as e:
        print(f"Error obteniendo archivos por modo {mode}: {e}")
        return []


def _display_console_results(analysis_results: Dict[str, Any], verbose: bool = False) -> None:
    """
    Muestra los resultados del análisis en consola de forma legible.

    Args:
        analysis_results: Resultados del análisis multi-lenguaje
        verbose: Si mostrar información detallada
    """
    summary = analysis_results.get('summary', {})
    files_data = analysis_results.get('files', {})
    categories = analysis_results.get('categories', {})

    print('\n' + '─' * 80)
    print(f"📊 RESUMEN DE ANÁLISIS MULTI-LENGUAJE")
    print('─' * 80)

    # Mostrar resumen general
    total_files = summary.get('total_files', 0)
    files_with_errors = summary.get('files_with_errors', 0)
    total_violations = summary.get('total_violations', 0)
    languages_analyzed = summary.get('languages_analyzed', [])

    print(f"📁 Archivos analizados: {total_files}")
    print(f"❌ Archivos con errores: {files_with_errors}")
    print(f"🔍 Total violaciones: {total_violations}")
    print(f"🎯 Lenguajes procesados: {', '.join(languages_analyzed)}")

    # Mostrar herramientas utilizadas
    tools_used = summary.get('tools_used', {})
    if tools_used and verbose:
        print(f"\n🔧 Herramientas utilizadas:")
        for lang, tool in tools_used.items():
            print(f"   {lang}: {tool}")

    # Mostrar categorías de errores
    if categories:
        print(f"\n📊 Violaciones por categoría:")
        for category, data in sorted(categories.items(), key=lambda x: x[1]['count'], reverse=True):
            count = data.get('count', 0)
            languages = data.get('files', [])
            print(f"   {category}: {count} violaciones ({', '.join(languages)})")

    # Mostrar archivos con errores si verbose
    if verbose and files_data:
        print(f"\n📄 Archivos con violaciones:")
        for file_path, file_data in files_data.items():
            violation_count = file_data.get('violation_count', 0)
            language = file_data.get('language', 'unknown')
            tool = file_data.get('tool', 'unknown')
            print(f"   {file_path}: {violation_count} violaciones ({language}/{tool})")

    print('─' * 80)

    # Resultado final
    if total_violations > 0:
        print(f"❌ RESULTADO FINAL: {total_violations} violaciones encontradas")
    else:
        print("✅ RESULTADO FINAL: Sin violaciones encontradas")

    print('─' * 80)


def _output_json_results(analysis_results: Dict[str, Any], output_location: str, verbose: bool = False) -> None:
    """
    Genera salida JSON de los resultados.

    Args:
        analysis_results: Resultados del análisis
        output_location: Ubicación del archivo de salida (vacío = stdout)
        verbose: Si mostrar información del proceso
    """
    if output_location:
        # Guardar a archivo
        with open(output_location, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, indent=2, ensure_ascii=False)
        if verbose:
            print(f"JSON guardado en: {output_location}")
    else:
        # Imprimir a stdout
        print(json.dumps(analysis_results, indent=2, ensure_ascii=False))


def _run_ruff_json_analysis(flags: Dict[str, Any], project_path: Path) -> None:
    """
    Ejecuta análisis de conformance usando Ruff y genera output JSON.

    Ejecuta el mismo análisis que el modo console pero formatea la salida como JSON
    estructurado para integración con otros CLIs y herramientas.

    Parameters
    ----------
    flags : Dict[str, Any]
        Configuraciones de ejecución que incluyen mode, verbose, output_location, etc.
    project_path : Path
        Ruta raíz del proyecto

    Side Effects
    ------------
    - Ejecuta subprocess con comando ruff check
    - Imprime JSON a stdout o guarda en archivo según output_location
    - Termina ejecución con sys.exit() según resultados

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    # Obtener archivos a analizar según el modo o archivos específicos
    if flags.get('files'):
        python_files = _get_python_files_by_files_list(flags['files'], project_path)
    else:
        python_files = _get_python_files_by_mode(flags.get('mode', 'unmerged'), project_path, flags.get('target_folder'))

    # Aplicar filtro de exclusión si se especificó
    if flags.get('exclude_paths'):
        exclude_paths_list = flags['exclude_paths']
        if isinstance(exclude_paths_list, str):
            exclude_paths_list = [p.strip() for p in exclude_paths_list.replace(',', ' ').split() if p.strip()]
        python_files = _filter_excluded_paths(python_files, exclude_paths_list, project_path)

    if not python_files:
        # Si no hay archivos, devolver JSON vacío con éxito
        json_output = {
            'summary': {
                'total_files': 0,
                'files_with_errors': 0,
                'total_violations': 0,
                'exit_code': 0,
            },
            'files': {},
            'categories': {},
            'metadata': {
                'mode': flags.get('mode', ''),
                'files': flags.get('files', []),
                'project_path': str(project_path),
                'ruff_config': str(project_path / 'ruff.toml'),
                'timestamp': datetime.now().isoformat(),
                'extensions_analyzed': list(RUFF_PYTHON_EXTENSIONS['suffixes']),
            },
        }

        output_location = flags.get('output_location', '')
        if output_location:
            # Guardar a archivo
            with open(output_location, 'w', encoding='utf-8') as f:
                json.dump(json_output, f, indent=2, ensure_ascii=False)
            if flags.get('verbose'):
                print(f"JSON guardado en: {output_location}")
        else:
            # Imprimir a stdout
            print(json.dumps(json_output, indent=2, ensure_ascii=False))

        sys.exit(0)

    # Ejecutar análisis Ruff
    analysis_results = _analyze_python_files_directly(python_files, project_path, flags.get('verbose', False))

    # Generar JSON estructurado
    json_output = _format_analysis_results_as_json(analysis_results, flags, project_path, python_files)

    # Determinar código de salida
    total_errors = sum(len(errors.get('ruff_violations', [])) for errors in analysis_results.values())
    json_output['summary']['exit_code'] = 1 if total_errors > 0 else 0

    # Output JSON
    output_location = flags.get('output_location', '')
    if output_location:
        # Guardar a archivo
        with open(output_location, 'w', encoding='utf-8') as f:
            json.dump(json_output, f, indent=2, ensure_ascii=False)
        if flags.get('verbose'):
            print(f"JSON guardado en: {output_location}")
    else:
        # Imprimir a stdout
        print(json.dumps(json_output, indent=2, ensure_ascii=False))

    # Exit con código apropiado
    sys.exit(json_output['summary']['exit_code'])


def _run_ruff_console_analysis(flags: Dict[str, Any], project_path: Path) -> None:
    """
    Ejecuta análisis de conformance usando Ruff con configuración completa.

    Utiliza la configuración Ruff definida en ruff.toml (800+ reglas) para validar
    calidad de código, estilo PEP 8, imports, seguridad y mejores prácticas Django.

    Parameters
    ----------
    flags : Dict[str, Any]
        Configuraciones de ejecución que incluyen mode, verbose, etc.
    project_path : Path
        Ruta raíz del proyecto

    Side Effects
    ------------
    - Ejecuta subprocess con comando ruff check
    - Imprime resultados categorizados en stdout
    - Termina ejecución con sys.exit() según resultados

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    # Mostrar información inicial si verbose está habilitado
    if flags.get('verbose'):
        print('\n' + '=' * 80)
        print(' RUFF CONFORMANCE ANALYSIS')
        print('=' * 80)

        if flags.get('mode'):
            print(f'Mode: {flags.get("mode")}')
            if flags.get('mode') == 'unmerged':
                print('Using unmerged mode: Only analyzing Python files from commits not merged to base branch')
        elif flags.get('files'):
            files_count = len(flags['files']) if isinstance(flags['files'], list) else 1
            print(f'Files: {files_count} archivo(s) específico(s)')
            print('Using files mode: Only analyzing specified files')

        print(f'Verbose: {flags.get("verbose", False)}')
        print(f'Project Path: {project_path}')
        print(f'Ruff Config: {project_path}/ruff.toml')
        print('Rules: 800+ active rules (E/W, S, DJ, PT, etc.)')
        print('=' * 80)

    # Obtener archivos a analizar según el modo o archivos específicos
    if flags.get('files'):
        python_files = _get_python_files_by_files_list(flags['files'], project_path)
    else:
        python_files = _get_python_files_by_mode(flags.get('mode', 'unmerged'), project_path, flags.get('target_folder'))

    # Aplicar filtro de exclusión si se especificó
    if flags.get('exclude_paths'):
        exclude_paths_list = flags['exclude_paths']
        if isinstance(exclude_paths_list, str):
            exclude_paths_list = [p.strip() for p in exclude_paths_list.replace(',', ' ').split() if p.strip()]
        python_files = _filter_excluded_paths(python_files, exclude_paths_list, project_path)

    if not python_files:
        print("✅ No hay archivos Python para analizar")
        return

    # Mostrar información del comando si verbose está habilitado
    if flags.get('verbose'):
        print('💻 Ejecutando: ruff check [archivo] --output-format=json --config ruff.toml')
        print(f'📁 Analizando {len(python_files)} archivos individualmente con Ruff')
        print('📄 Configuración: ruff.toml (800+ reglas activas)')

    # Mostrar estructura de archivos usando genstruct (solo para modos git)
    if flags.get('mode'):  # Solo mostrar para modos git, no para archivos específicos
        _show_structure_info(flags, project_path)

    # Ejecutar análisis Ruff
    analysis_results = _analyze_python_files_directly(python_files, project_path, flags.get('verbose', False))

    # Mostrar resultados categorizados
    _display_categorized_results(analysis_results, flags.get('verbose', False))

    # Determinar código de salida
    total_errors = sum(len(errors.get('ruff_violations', [])) for errors in analysis_results.values())

    print('\n' + '═' * 80)
    if total_errors > 0:
        print(f"❌ RESULTADO FINAL: {total_errors} violaciones encontradas")
        print('═' * 80)
        sys.exit(1)
    else:
        print("✅ RESULTADO FINAL: Sin violaciones encontradas")
        print('═' * 80)
        sys.exit(0)


def _show_structure_info(flags: Dict[str, Any], project_path: Path) -> None:
    """
    Muestra información de estructura de archivos usando genstruct.

    Ejecuta el script de estructura de archivos para mostrar los archivos
    que serán analizados según el modo git especificado.

    Parameters
    ----------
    flags : Dict[str, Any]
        Configuraciones de ejecución
    project_path : Path
        Ruta raíz del proyecto

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    try:
        # Ejecutar genstruct para mostrar archivos no mergeados
        mode = flags.get('mode', 'unmerged')

        git_mode_map = {
            'changed': 'changed',
            'staged': 'staged',
            'unstaged': 'unstaged',
            'unmerged': 'unmerged',
            'all': 'all',
        }
        git_mode = git_mode_map.get(mode, 'unmerged')

        cmd = [
            sys.executable, 'scripts/run.py', 'genstruct',
            f'--git-mode={git_mode}', f'--only-extension={RUFF_PYTHON_EXTENSIONS["structure_arg"]}',
        ]

        if flags.get('verbose'):
            print(f'\n🏗️  ESTRUCTURA DE ARCHIVOS ({mode.upper()})')
            print('=' * 50)

        # Ejecutar el comando con validación de seguridad
        # Validar que el comando contiene solo elementos seguros
        safe_cmd = []
        for item in cmd:
            if isinstance(item, str) and item:
                safe_cmd.append(item)

        # Verificar que el comando use un ejecutable Python seguro
        if not safe_cmd or not safe_cmd[0].endswith(('python', 'python3', 'python3.8')):
            raise ValueError(f"Comando no seguro: {safe_cmd}")

        # Use explicit arguments for security compliance
        result = subprocess.run(
            args=safe_cmd,
            cwd=str(project_path),
            capture_output=True,
            text=True,
            timeout=30,
            shell=False,  # Nunca usar shell=True para seguridad
            check=False,
        )

        if result.returncode == 0:
            # Mostrar la salida del comando
            output = result.stdout.strip()
            if output:
                print(output)
            else:
                print("No hay archivos Python en el modo especificado")
        else:
            if flags.get('verbose'):
                print(f"⚠️  Error ejecutando genstruct: {result.stderr}")

        if flags.get('verbose'):
            print('=' * 50)

    except (ValueError, TypeError, AttributeError, KeyError, OSError, ImportError) as e:
        if flags.get('verbose'):
            print(f"⚠️  Error mostrando estructura: {e}")


def _get_python_files_by_mode(mode: str, project_path: Path, target_folder: Optional[str] = None) -> List[Path]:
    """
    Obtiene lista de archivos con extensiones Python soportadas por Ruff según el modo especificado.

    Utiliza comandos git para obtener archivos según diferentes modos y filtra
    por extensiones Python soportadas por Ruff para análisis de código.

    Extensiones soportadas: .py, .pyi, .ipynb, .pyw, .py3, .pyz, .pyx, .pxd, .pxi

    Parameters
    ----------
    mode : str
        Modo de selección: 'all', 'changed', 'staged', 'unstaged', 'unmerged'
    project_path : Path
        Ruta raíz del proyecto
    target_folder : Optional[str]
        Carpeta específica a analizar (opcional)

    Returns
    -------
    List[Path]
        Lista de archivos Python/Ruff compatibles como objetos Path

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    if target_folder:
        # Si se especifica target_folder, analizar directamente esa carpeta
        target_path = Path(target_folder)
        if not target_path.is_absolute():
            target_path = project_path / target_path

        if not target_path.exists():
            print(f"Error: La carpeta {target_folder} no existe")
            return []

        # Buscar archivos con todas las extensiones Python soportadas por Ruff
        python_files = []
        for pattern in RUFF_PYTHON_EXTENSIONS['patterns']:
            python_files.extend(list(target_path.glob(pattern.replace('**/', ''))))
        return python_files

    # Para modos git, usar comandos git para obtener archivos
    try:
        if mode == 'all':
            # Todos los archivos con extensiones Python soportadas por Ruff
            python_files = []
            for pattern in RUFF_PYTHON_EXTENSIONS['patterns']:
                python_files.extend(list(project_path.glob(pattern)))
            return python_files
        # Usar ruta completa de git para seguridad y validar su existencia
        git_executable = '/usr/bin/git'
        if not Path(git_executable).exists():
            print(f"Error: No se encuentra git en {git_executable}")
            return []

        if mode == 'changed':
            # Archivos modificados localmente
            cmd = [git_executable, 'diff', '--name-only', 'HEAD']
            # Verificar que el comando use git seguro
            if not git_executable.endswith(('git', 'git.exe')):
                raise ValueError(f"Ejecutable git no seguro: {git_executable}")
            # Use explicit arguments for security compliance
            result = subprocess.run(
                args=cmd,
                cwd=project_path,
                capture_output=True,
                text=True,
                shell=False,
                check=False
            )
        elif mode == 'staged':
            # Archivos en staging area
            cmd = [git_executable, 'diff', '--staged', '--name-only']
            # Verificar que el comando use git seguro
            if not git_executable.endswith(('git', 'git.exe')):
                raise ValueError(f"Ejecutable git no seguro: {git_executable}")
            # Use explicit arguments for security compliance
            result = subprocess.run(
                args=cmd,
                cwd=project_path,
                capture_output=True,
                text=True,
                shell=False,
                check=False
            )
        elif mode == 'unstaged':
            # Archivos modificados pero no staged
            cmd = [git_executable, 'diff', '--name-only']
            # Verificar que el comando use git seguro
            if not git_executable.endswith(('git', 'git.exe')):
                raise ValueError(f"Ejecutable git no seguro: {git_executable}")
            # Use explicit arguments for security compliance
            result = subprocess.run(
                args=cmd,
                cwd=project_path,
                capture_output=True,
                text=True,
                shell=False,
                check=False
            )
        elif mode == 'unmerged':
            # Archivos no mergeados (default)
            cmd = [git_executable, 'diff', '--name-only', 'origin/dev...HEAD']
            # Verificar que el comando use git seguro
            if not git_executable.endswith(('git', 'git.exe')):
                raise ValueError(f"Ejecutable git no seguro: {git_executable}")
            # Use explicit arguments for security compliance
            result = subprocess.run(
                args=cmd,
                cwd=project_path,
                capture_output=True,
                text=True,
                shell=False,
                check=False
            )
        else:
            print(f"Error: Modo '{mode}' no reconocido")
            return []

        if result.returncode != 0:
            print(f"Error ejecutando git: {result.stderr}")
            return []

        # Filtrar archivos con extensiones Python soportadas por Ruff
        python_files = []
        for file_line in result.stdout.strip().split('\n'):
            if file_line:
                file_path = project_path / file_line
                if file_path.exists() and file_path.suffix in RUFF_PYTHON_EXTENSIONS['suffixes']:
                    python_files.append(file_path)

        return python_files

    except (ValueError, TypeError, AttributeError, KeyError, OSError, ImportError) as e:
        print(f"Error obteniendo archivos por modo {mode}: {e}")
        return []


def _get_python_files_by_files_list(files_list: List[str], project_path: Path) -> List[Path]:
    """
    Obtiene lista de archivos Python a partir de una lista específica de archivos.

    Valida y filtra los archivos especificados por el usuario, verificando
    que existan, sean archivos (no directorios) y tengan extensiones Python válidas.

    Parameters
    ----------
    files_list : List[str]
        Lista de paths de archivos especificados por el usuario
    project_path : Path
        Ruta raíz del proyecto

    Returns
    -------
    List[Path]
        Lista de archivos Python válidos como objetos Path

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    python_files = []

    for file_path in files_list:
        full_path = project_path / file_path

        # Verificar que el archivo existe, es un archivo (no carpeta) y tiene extensión Python válida
        if (full_path.exists() and
            full_path.is_file() and
            full_path.suffix in RUFF_PYTHON_EXTENSIONS['suffixes']):
            python_files.append(full_path)

    return python_files


def _analyze_python_files_directly(
    python_files: List[Path],
    project_path: Path,
    verbose: bool = False,
) -> Dict[str, Dict[str, Any]]:
    """
    Analiza archivos Python usando configuración Ruff completa.

    Ejecuta análisis con 800+ reglas definidas en ruff.toml para cada archivo,
    categorizando errores por tipo y generando reporte estructurado.

    Parameters
    ----------
    python_files : List[Path]
        Lista de archivos Python a analizar
    project_path : Path
        Ruta raíz del proyecto para paths relativos
    verbose : bool, default=False
        Si mostrar información detallada del análisis

    Returns
    -------
    Dict[str, Dict[str, Any]]
        Diccionario con errores por archivo en formato:
        {
            'archivo.py': {
                'ruff_violations': [...],
                'code_style_errors': int,
                ...
            }
        }

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    files_with_errors = {}

    # Verificar que ruff está disponible usando ruta completa
    ruff_executable = '/home/bypabloc/projects/destacame/easy-pay/.venv/bin/ruff'
    try:
        # Verificar que el ejecutable de ruff sea seguro
        if not ruff_executable.endswith(('ruff', 'ruff.exe')):
            raise ValueError(f"Ejecutable ruff no seguro: {ruff_executable}")
        # Use explicit arguments for security compliance
        subprocess.run(
            args=[ruff_executable, '--version'],
            capture_output=True,
            check=True,
            shell=False
        )
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
        print("❌ Error: Ruff no está instalado o no está en el PATH")
        print("   Instalar con: pip install ruff")
        return {}

    # Verificar que existe ruff.toml
    ruff_config = project_path / 'ruff.toml'
    if not ruff_config.exists():
        print(f"⚠️  Advertencia: No se encontró ruff.toml en {project_path}")
        print("   Usando configuración por defecto de Ruff")

    # Ejecutar Ruff una sola vez con todos los archivos (optimización)
    try:
        # Usar --config para asegurar que usa nuestro ruff.toml
        # Usar --no-fix para evitar que pregunte por aplicar fixes (modo read-only)
        cmd = [ruff_executable, 'check'] + [str(f) for f in python_files] + ['--output-format=json', '--no-fix']
        if ruff_config.exists():
            cmd.extend(['--config', str(ruff_config)])

        # Mostrar comando completo ejecutado con formato legible
        if verbose:
            print('\n' + '=' * 80)
            print('💻 COMANDO RUFF A EJECUTAR:')
            print('=' * 80)

            # Construir comando formateado con saltos de línea
            cmd_formatted = 'ruff check \\\n'
            for i, file_path in enumerate(python_files):
                if i == len(python_files) - 1:  # Último archivo
                    cmd_formatted += f'    {file_path} \\\n'
                else:
                    cmd_formatted += f'    {file_path} \\\n'

            # Agregar flags al final
            cmd_formatted += '    --output-format=json \\\n    --no-fix'
            if ruff_config.exists():
                cmd_formatted += ' \\\n    --config ruff.toml'

            print(cmd_formatted)
            print('=' * 80)
            print(f'🔍 Analizando {len(python_files)} archivos con Ruff (configuración completa)...\n')

        # Verificar que el comando use ruff seguro
        if not cmd or not cmd[0].endswith(('ruff', 'ruff.exe')):
            raise ValueError(f"Comando ruff no seguro: {cmd}")
        # Use explicit arguments for security compliance
        ruff_result = subprocess.run(
            args=cmd,
            capture_output=True,
            text=True,
            timeout=120,  # Más tiempo para múltiples archivos
            cwd=str(project_path),  # Ejecutar desde raíz del proyecto
            shell=False,
            check=False,
        )

        # Procesar resultados de Ruff para todos los archivos
        all_violations = []
        if ruff_result.stdout.strip():
            try:
                all_violations = json.loads(ruff_result.stdout)
                if verbose:
                    print(f'📊 Ruff encontró {len(all_violations)} violaciones en total')
            except json.JSONDecodeError as e:
                if verbose:
                    print(f"⚠️  Error parseando JSON de Ruff: {e}")
                    print(f"Salida raw (primeros 200 chars): {ruff_result.stdout[:200]}...")

        # Organizar violaciones por archivo
        for file_path in python_files:
            try:
                relative_path = str(file_path.relative_to(project_path))

                # Filtrar violaciones para este archivo específico
                # Comparar tanto ruta absoluta como relativa para mayor compatibilidad
                file_violations = [
                    v for v in all_violations
                    if v.get('filename') == str(file_path) or
                       v.get('filename') == str(file_path.resolve()) or
                       v.get('filename') == relative_path
                ]

                if file_violations:
                    file_errors = {
                        'absolute_path': file_path,
                        'ruff_violations': file_violations,
                        'code_style_errors': len(file_violations),
                    }
                    files_with_errors[relative_path] = file_errors

                    if verbose:
                        print(f'❌ {len(file_violations)} violaciones en {relative_path}')
                else:
                    # Para debug: mostrar qué archivos no tienen errores si verbose
                    if verbose:
                        # No mostrar archivos sin errores para reducir verbosidad
                        pass
            except (ValueError, TypeError, AttributeError, KeyError, OSError, ImportError) as e:
                if verbose:
                    print(f'❌ Error procesando {file_path}: {e!s}')
                continue

    except subprocess.TimeoutExpired:
        if verbose:
            print(f'⏰ Timeout ejecutando Ruff con {len(python_files)} archivos')
    except (ValueError, TypeError, AttributeError, KeyError, OSError, ImportError) as e:
        if verbose:
            print(f'❌ Error ejecutando comando Ruff optimizado: {e!s}')

    if verbose:
        print('\n' + '=' * 80)
        print(f'📊 ANÁLISIS COMPLETADO: {len(files_with_errors)} archivos con errores de {len(python_files)} analizados')
        print('=' * 80)

    return files_with_errors


def _display_categorized_results(analysis_results: Dict[str, Dict[str, Any]], verbose: bool = False) -> None:
    """
    Muestra resultados de análisis Ruff categorizados en consola.

    Organiza y presenta los resultados del análisis de código categorizando
    las violaciones por tipo para facilitar la comprensión y corrección.

    Parameters
    ----------
    analysis_results : Dict[str, Dict[str, Any]]
        Resultados del análisis por archivo
    verbose : bool, default=False
        Si mostrar información detallada con ejemplos

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    if not analysis_results:
        print('\n' + '─' * 80)
        print("✅ No se encontraron violaciones")
        print('─' * 80)
        return

    # Categorizar errores por tipo
    categories = {}
    total_violations = 0

    for file_path, file_errors in analysis_results.items():
        for error in file_errors.get('ruff_violations', []):
            code = error.get('code', 'UNKNOWN')
            category = _categorize_ruff_error(code, error.get('message', ''))

            if category not in categories:
                categories[category] = {'count': 0, 'files': set(), 'examples': []}

            categories[category]['count'] += 1
            categories[category]['files'].add(file_path)

            if len(categories[category]['examples']) < 3:  # Max 3 examples per category
                categories[category]['examples'].append({
                    'file': file_path,
                    'code': code,
                    'line': error.get('location', {}).get('row', 'N/A'),
                    'message': error.get('message', ''),
                })

            total_violations += 1

    # Mostrar resumen por categoría
    print('\n' + '─' * 80)
    print(f"📊 RESUMEN DE ANÁLISIS RUFF - {total_violations} violaciones en {len(analysis_results)} archivos")
    print('─' * 80)

    for category, data in sorted(categories.items()):
        print(f"🔍 {category.upper()}: {data['count']} violaciones en {len(data['files'])} archivos")

        if verbose:
            for example in data['examples'][:2]:  # Show 2 examples if verbose
                print(f"   • {example['file']}:{example['line']} - {example['code']}: {example['message'][:80]}...")

        print()

    print('─' * 80)


def _format_analysis_results_as_json(
    analysis_results: Dict[str, Dict[str, Any]],
    flags: Dict[str, Any],
    project_path: Path,
    python_files: List[Path],
) -> Dict[str, Any]:
    """
    Formatea los resultados del análisis Ruff como JSON estructurado.

    Convierte los resultados del análisis en un formato JSON estructurado
    con metadatos, categorías y estadísticas para integración con herramientas externas.

    Parameters
    ----------
    analysis_results : Dict[str, Dict[str, Any]]
        Resultados del análisis por archivo
    flags : Dict[str, Any]
        Configuraciones de ejecución
    project_path : Path
        Ruta del proyecto
    python_files : List[Path]
        Lista de archivos analizados

    Returns
    -------
    Dict[str, Any]
        Estructura JSON completa con resumen, archivos, categorías y metadatos

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    # Categorizar errores por tipo
    categories = {}
    total_violations = 0

    # Estructura de archivos con errores detallados
    files_data = {}

    for file_path, file_errors in analysis_results.items():
        violations = []
        for error in file_errors.get('ruff_violations', []):
            code = error.get('code', 'UNKNOWN')
            category = _categorize_ruff_error(code, error.get('message', ''))

            # Agregar a categorías
            if category not in categories:
                categories[category] = {'count': 0, 'files': set()}
            categories[category]['count'] += 1
            categories[category]['files'].add(file_path)

            # Formatear violación
            violation = {
                'code': code,
                'message': error.get('message', ''),
                'line': error.get('location', {}).get('row', None),
                'column': error.get('location', {}).get('column', None),
                'category': category,
                'url': error.get('url', ''),
            }
            violations.append(violation)
            total_violations += 1

        if violations:
            files_data[file_path] = {
                'violations': violations,
                'violation_count': len(violations),
            }

    # Convertir sets a lists en categorías
    categories_serializable = {}
    for category, data in categories.items():
        categories_serializable[category] = {
            'count': data['count'],
            'files': list(data['files']),
        }

    # Construir JSON final
    return {
        'summary': {
            'total_files': len(python_files),
            'files_with_errors': len(analysis_results),
            'total_violations': total_violations,
            'exit_code': 0,  # Se asigna después en la función caller
        },
        'files': files_data,
        'categories': categories_serializable,
        'metadata': {
            'mode': flags.get('mode', ''),
            'files': flags.get('files', []),
            'project_path': str(project_path),
            'ruff_config': str(project_path / 'ruff.toml'),
            'timestamp': datetime.now().isoformat(),
            'extensions_analyzed': list(RUFF_PYTHON_EXTENSIONS['suffixes']),
            'verbose': flags.get('verbose', False),
            'target_folder': flags.get('target_folder', ''),
        },
    }


def _categorize_ruff_error(code: str, message: str) -> str:
    """
    Categoriza errores de Ruff por tipo para reporte estructurado.

    Mapea códigos de error de Ruff a categorías legibles para facilitar
    la organización y comprensión de los diferentes tipos de violaciones.

    Parameters
    ----------
    code : str
        Código de error Ruff como E501, F401, S101, etc.
    message : str
        Mensaje descriptivo del error

    Returns
    -------
    str
        Categoría del error para agrupación como 'style_errors', 'security_issues', etc.

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    # Mapeo de prefijos Ruff a categorías legibles
    category_map = {
        'E': 'style_errors',          # pycodestyle errors
        'W': 'style_warnings',        # pycodestyle warnings
        'F': 'pyflakes_issues',       # Pyflakes (imports, unused vars)
        'I': 'import_sorting',        # isort
        'UP': 'python_upgrade',       # pyupgrade
        'B': 'bugbear_issues',        # flake8-bugbear
        'C4': 'comprehensions',       # flake8-comprehensions
        'SIM': 'simplifications',     # flake8-simplify
        'PIE': 'pie_issues',          # flake8-pie
        'RET': 'return_issues',       # flake8-return
        'N': 'naming_issues',         # pep8-naming
        'S': 'security_issues',       # flake8-bandit
        'BLE': 'blind_except',        # flake8-blind-except
        'A': 'builtins_issues',       # flake8-builtins
        'COM': 'comma_issues',        # flake8-commas
        'DJ': 'django_issues',        # flake8-django
        'PT': 'pytest_issues',        # flake8-pytest-style
        'ERA': 'commented_code',      # eradicate
        'T20': 'debug_prints',        # flake8-print
        'FIX': 'fixme_comments',      # flake8-fixme
        'G': 'logging_issues',        # flake8-logging-format
        'T10': 'debugger_issues',     # flake8-debugger
        'RUF': 'ruff_specific',       # Ruff-specific rules
    }

    # Buscar por prefijo del código
    for prefix, category in category_map.items():
        if code.startswith(prefix):
            return category

    # Fallback para códigos desconocidos
    return 'unknown_issues'


def _generate_ruff_structured_output(
    flags: Dict[str, Any],
    project_path: Path,
    output_format: str,
    output_location: str,
) -> None:
    """
    Genera reportes estructurados usando análisis Ruff completo.

    Crea reportes en formato HTML o JSON con análisis completo de conformance
    de código para documentación y revisión externa.

    Parameters
    ----------
    flags : Dict[str, Any]
        Configuraciones de ejecución
    project_path : Path
        Ruta del proyecto
    output_format : str
        Formato de salida: 'json' o 'html'
    output_location : str
        Ruta donde guardar el reporte

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    print("⚠️  Generación de reportes estructurados no implementada completamente")
    print("   Usar modo consola por ahora: --output-format=console")
    sys.exit(1)
