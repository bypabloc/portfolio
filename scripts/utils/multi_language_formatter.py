"""
Formateador multi-lenguaje para code_formatter.

Este módulo orquesta el formateo de diferentes lenguajes usando
las herramientas específicas configuradas en language_configs.py.

:Authors:
    - Pablo Contreras
:Created:
    - 2025-01-19
:Modified:
    - 2025-01-19
"""

import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional

from .language_configs import (
    get_language_from_extension,
    get_languages_from_files,
    get_tool_config,
    find_config_file,
    build_command,
    validate_languages,
)


def format_files_by_language(
    files_with_errors: Dict[str, Any],
    languages_filter: Optional[List[str]],
    project_path: Path,
    verbose: bool = False,
) -> Dict[str, Any]:
    """
    Formatea archivos agrupándolos por lenguaje y usando herramientas específicas.

    Args:
        files_with_errors: Diccionario con archivos que tienen errores de conformance
        languages_filter: Lista de lenguajes específicos a formatear (None = todos)
        project_path: Ruta raíz del proyecto
        verbose: Si mostrar información detallada

    Returns:
        Diccionario con resultados del formateo por lenguaje
    """
    if verbose:
        print('\n' + '=' * 80)
        print(' MULTI-LANGUAGE CODE FORMATTER')
        print('=' * 80)

    if not files_with_errors:
        if verbose:
            print("✅ No hay archivos con errores para formatear")
        return _create_empty_formatting_result()

    # Detectar lenguajes de los archivos con errores
    files_to_format = list(files_with_errors.keys())
    detected_languages = get_languages_from_files(files_to_format)

    # Aplicar filtro de lenguajes si se especificó
    if languages_filter:
        # Validar que los lenguajes estén soportados
        invalid_languages = validate_languages(languages_filter)
        if invalid_languages:
            raise ValueError(f"Lenguajes no soportados: {', '.join(invalid_languages)}")

        # Usar solo los lenguajes especificados que también fueron detectados
        target_languages = [lang for lang in languages_filter if lang in detected_languages]

        if verbose:
            print(f"🔧 Filtro de lenguajes aplicado: {', '.join(languages_filter)}")
            print(f"🎯 Lenguajes a formatear: {', '.join(target_languages)}")
    else:
        target_languages = detected_languages
        if verbose:
            print(f"🔍 Lenguajes detectados automáticamente: {', '.join(target_languages)}")

    if not target_languages:
        if verbose:
            print("⚠️  No se encontraron lenguajes válidos para formatear")
        return _create_empty_formatting_result()

    # Agrupar archivos por lenguaje
    files_by_language = _group_files_by_language_from_errors(files_with_errors, target_languages, project_path)

    if verbose:
        print(f"\n📊 Distribución de archivos a formatear:")
        for lang, lang_files in files_by_language.items():
            tool_config = get_tool_config(lang)
            formatter_tool = tool_config['formatter_tool'] if tool_config else 'Unknown'
            print(f"  {formatter_tool} ({lang}): {len(lang_files)} archivos")

    # Formatear cada lenguaje por separado
    formatting_summary = {
        'total_files': len(files_to_format),
        'files_formatted': 0,
        'languages_processed': [],
        'tools_used': {},
        'errors': [],
    }

    for language, language_files in files_by_language.items():
        if verbose:
            tool_config = get_tool_config(language)
            formatter_tool = tool_config['formatter_tool'] if tool_config else language
            print(f"\n🔧 Formateando con {formatter_tool} ({len(language_files)} archivos)...")

        try:
            formatting_result = _format_language_files(
                language, language_files, project_path, verbose
            )

            if formatting_result['success']:
                formatting_summary['files_formatted'] += len(language_files)
                formatting_summary['languages_processed'].append(language)

                tool_config = get_tool_config(language)
                if tool_config:
                    formatting_summary['tools_used'][language] = tool_config['formatter_tool']

                if verbose:
                    print(f"  ✅ {len(language_files)} archivos formateados correctamente")
            else:
                formatting_summary['errors'].append({
                    'language': language,
                    'error': formatting_result.get('error', 'Unknown error'),
                    'files_count': len(language_files)
                })

                if verbose:
                    print(f"  ❌ Error formateando archivos: {formatting_result.get('error', 'Unknown error')}")

        except Exception as e:
            formatting_summary['errors'].append({
                'language': language,
                'error': str(e),
                'files_count': len(language_files)
            })

            if verbose:
                print(f"  ⚠️  Error formateando {language}: {e}")
            continue

    if verbose:
        print('\n' + '=' * 80)
        print(f'📊 FORMATEO COMPLETADO: {formatting_summary["files_formatted"]} archivos formateados')
        print(f'🎯 Lenguajes procesados: {", ".join(formatting_summary["languages_processed"])}')
        if formatting_summary['errors']:
            print(f'⚠️  {len(formatting_summary["errors"])} errores encontrados')
        print('=' * 80)

    return formatting_summary


def _group_files_by_language_from_errors(
    files_with_errors: Dict[str, Any],
    target_languages: List[str],
    project_path: Path
) -> Dict[str, List[Path]]:
    """Agrupa archivos con errores por lenguaje."""
    files_by_language = {}

    for file_path_str in files_with_errors.keys():
        file_path = project_path / file_path_str
        extension = file_path.suffix.lower()
        language = get_language_from_extension(extension)

        if language and language in target_languages:
            if language not in files_by_language:
                files_by_language[language] = []
            files_by_language[language].append(file_path)

    return files_by_language


def _format_language_files(
    language: str,
    files: List[Path],
    project_path: Path,
    verbose: bool = False,
) -> Dict[str, Any]:
    """Formatea archivos de un lenguaje específico usando su herramienta correspondiente."""
    tool_config = get_tool_config(language)
    if not tool_config:
        return {
            'success': False,
            'error': f'No hay configuración disponible para {language}'
        }

    # Buscar archivo de configuración
    config_file = find_config_file(language, project_path)

    # Construir comando de formateo
    command = build_command(language, 'formatter', [str(f) for f in files], config_file)
    if not command:
        return {
            'success': False,
            'error': f'No se pudo construir comando de formateo para {language}'
        }

    if verbose:
        config_info = f" (config: {config_file.name})" if config_file else " (config por defecto)"
        print(f"  💻 Ejecutando: {' '.join(command[:3])} ... {config_info}")

    # Ejecutar formateo
    try:
        result = subprocess.run(
            command,
            cwd=str(project_path),
            capture_output=True,
            text=True,
            timeout=180,
            shell=False,
            check=False,
        )

        # Para la mayoría de formateadores, un exit code 0 significa éxito
        # Algunos (como Prettier) pueden devolver código 1 pero aún formatear correctamente
        success = result.returncode == 0

        # Información adicional si verbose
        if verbose and result.stdout.strip():
            output_lines = result.stdout.strip().split('\n')
            if len(output_lines) <= 5:
                for line in output_lines:
                    if line.strip():
                        print(f"    {line}")
            else:
                print(f"    {output_lines[0]}")
                print(f"    ... y {len(output_lines) - 1} líneas más")

        if verbose and result.stderr.strip() and not success:
            print(f"    ⚠️  Stderr: {result.stderr.strip()[:100]}...")

        return {
            'success': success,
            'exit_code': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr,
        }

    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': f'Timeout ejecutando formateo de {language}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Error ejecutando formateo de {language}: {e}'
        }


def _create_empty_formatting_result() -> Dict[str, Any]:
    """Crea un resultado vacío cuando no hay archivos para formatear."""
    return {
        'total_files': 0,
        'files_formatted': 0,
        'languages_processed': [],
        'tools_used': {},
        'errors': [],
    }


def get_files_with_errors_from_conformance(
    conformance_flags: Dict[str, Any],
    project_path: Path,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Ejecuta code_conformance para obtener lista de archivos con errores.

    Args:
        conformance_flags: Flags para pasarle a code_conformance
        project_path: Ruta del proyecto
        verbose: Si mostrar información detallada

    Returns:
        Diccionario con archivos que tienen errores
    """
    if verbose:
        print('\n🔍 Ejecutando análisis de conformance para identificar archivos con errores...')

    # Construir comando code_conformance con JSON output
    import sys
    cmd = [sys.executable, 'scripts/run.py', 'code_conformance', '--output-format=json']

    # Agregar flags apropiadas
    if conformance_flags.get('mode'):
        cmd.append(f'--mode={conformance_flags["mode"]}')
    elif conformance_flags.get('files'):
        files_list = conformance_flags['files']
        if isinstance(files_list, list):
            files_str = ' '.join(files_list)
        else:
            files_str = str(files_list)
        cmd.append(f'--files={files_str}')

    # Agregar otras flags
    for flag_name in ['target_folder', 'exclude_paths', 'languages']:
        if conformance_flags.get(flag_name):
            flag_value = conformance_flags[flag_name]
            if isinstance(flag_value, list):
                flag_value = ','.join(flag_value)
            cmd.append(f'--{flag_name.replace("_", "-")}={flag_value}')

    try:
        # Ejecutar conformance y capturar JSON
        result = subprocess.run(
            cmd,
            cwd=str(project_path),
            capture_output=True,
            text=True,
            timeout=120,
            shell=False,
            check=False,
        )

        if not result.stdout.strip():
            if verbose:
                print("⚠️  No se obtuvo output JSON del análisis de conformance")
            return {}

        # Extraer solo la parte JSON
        json_content = _extract_json_from_output(result.stdout)
        if not json_content:
            if verbose:
                print("⚠️  No se pudo extraer JSON válido del output de conformance")
            return {}

        # Parsear JSON
        import json
        try:
            conformance_data = json.loads(json_content)
        except json.JSONDecodeError as e:
            if verbose:
                print(f"⚠️  Error parseando JSON de conformance: {e}")
            return {}

        # Extraer archivos con errores
        files_with_errors = conformance_data.get('files', {})

        if verbose:
            total_violations = conformance_data.get('summary', {}).get('total_violations', 0)
            print(f"📊 Encontrados {len(files_with_errors)} archivos con errores ({total_violations} violaciones totales)")

            if files_with_errors:
                print("📄 Archivos que serán formateados:")
                file_items = list(files_with_errors.items())
                for file_path, file_data in file_items[:5]:  # Mostrar solo primeros 5
                    violation_count = file_data.get('violation_count', 0)
                    language = file_data.get('language', 'unknown')
                    print(f"   • {file_path} ({violation_count} violaciones - {language})")
                if len(file_items) > 5:
                    print(f"   ... y {len(file_items) - 5} archivos más")

        return files_with_errors

    except subprocess.TimeoutExpired:
        if verbose:
            print("⏰ Timeout ejecutando análisis de conformance")
        return {}
    except Exception as e:
        if verbose:
            print(f"❌ Error ejecutando conformance: {e}")
        return {}


def _extract_json_from_output(output: str) -> str:
    """
    Extrae contenido JSON válido de un output que puede contener texto adicional.

    Args:
        output: Output completo que puede tener texto antes del JSON

    Returns:
        String con solo el contenido JSON, o string vacío si no se encuentra JSON válido
    """
    lines = output.strip().split('\n')

    # Buscar la primera línea que comience con '{'
    json_start = -1
    for i, line in enumerate(lines):
        if line.strip().startswith('{'):
            json_start = i
            break

    if json_start == -1:
        return ''

    # Extraer desde la línea JSON hasta el final
    json_lines = lines[json_start:]
    json_content = '\n'.join(json_lines)

    # Verificar que sea JSON válido básico
    json_content = json_content.strip()
    if json_content.startswith('{') and json_content.endswith('}'):
        return json_content

    return ''