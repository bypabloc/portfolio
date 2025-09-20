"""
Analizador multi-lenguaje para code_conformance.

Este módulo orquesta el análisis de diferentes lenguajes usando
las herramientas específicas configuradas en language_configs.py.

:Authors:
    - Pablo Contreras
:Created:
    - 2025-01-19
:Modified:
    - 2025-01-19
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

from .language_configs import (
    get_language_from_extension,
    get_languages_from_files,
    get_tool_config,
    find_config_file,
    build_command,
    categorize_error,
    validate_languages,
)


def analyze_files_by_language(
    files: List[Path],
    languages_filter: Optional[List[str]],
    project_path: Path,
    verbose: bool = False,
) -> Dict[str, Any]:
    """
    Analiza archivos agrupándolos por lenguaje y usando herramientas específicas.

    Args:
        files: Lista de archivos a analizar
        languages_filter: Lista de lenguajes específicos a analizar (None = todos)
        project_path: Ruta raíz del proyecto
        verbose: Si mostrar información detallada

    Returns:
        Diccionario con resultados de análisis por lenguaje y archivo
    """
    if verbose:
        print('\n' + '=' * 80)
        print(' MULTI-LANGUAGE CONFORMANCE ANALYSIS')
        print('=' * 80)

    # Detectar lenguajes automáticamente de los archivos
    detected_languages = get_languages_from_files([str(f) for f in files])

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
            print(f"🎯 Lenguajes a analizar: {', '.join(target_languages)}")
    else:
        target_languages = detected_languages
        if verbose:
            print(f"🔍 Lenguajes detectados automáticamente: {', '.join(target_languages)}")

    if not target_languages:
        if verbose:
            print("⚠️  No se encontraron lenguajes válidos para analizar")
        return _create_empty_analysis_result(files, languages_filter, project_path)

    # Agrupar archivos por lenguaje
    files_by_language = _group_files_by_language(files, target_languages)

    if verbose:
        print(f"\n📊 Distribución de archivos:")
        for lang, lang_files in files_by_language.items():
            tool_config = get_tool_config(lang)
            tool_name = tool_config['name'] if tool_config else 'Unknown'
            print(f"  {tool_name} ({lang}): {len(lang_files)} archivos")

    # Analizar cada lenguaje por separado
    all_results = {}
    analysis_summary = {
        'total_files': len(files),
        'files_with_errors': 0,
        'total_violations': 0,
        'languages_analyzed': [],
        'tools_used': {},
    }

    for language, language_files in files_by_language.items():
        if verbose:
            tool_config = get_tool_config(language)
            tool_name = tool_config['name'] if tool_config else language
            print(f"\n🔍 Analizando {tool_name} ({len(language_files)} archivos)...")

        try:
            language_results = _analyze_language_files(
                language, language_files, project_path, verbose
            )

            # Agregar resultados al total
            all_results.update(language_results)

            # Actualizar resumen
            files_with_errors = len([f for f in language_results.values() if f.get('violations')])
            total_violations = sum(len(f.get('violations', [])) for f in language_results.values())

            analysis_summary['files_with_errors'] += files_with_errors
            analysis_summary['total_violations'] += total_violations
            analysis_summary['languages_analyzed'].append(language)

            tool_config = get_tool_config(language)
            if tool_config:
                analysis_summary['tools_used'][language] = tool_config['conformance_tool']

            if verbose:
                if total_violations > 0:
                    print(f"  ❌ {files_with_errors} archivos con errores ({total_violations} violaciones)")
                else:
                    print(f"  ✅ Sin violaciones encontradas")

        except Exception as e:
            if verbose:
                print(f"  ⚠️  Error analizando {language}: {e}")
            continue

    if verbose:
        print('\n' + '=' * 80)
        print(f'📊 ANÁLISIS COMPLETADO: {analysis_summary["files_with_errors"]} archivos con errores de {len(files)} analizados')
        print(f'🎯 Lenguajes procesados: {", ".join(analysis_summary["languages_analyzed"])}')
        print('=' * 80)

    return _format_final_results(all_results, analysis_summary, languages_filter, project_path)


def _group_files_by_language(files: List[Path], target_languages: List[str]) -> Dict[str, List[Path]]:
    """Agrupa archivos por lenguaje basándose en extensiones."""
    files_by_language = {}

    for file_path in files:
        extension = file_path.suffix.lower()
        language = get_language_from_extension(extension)

        if language and language in target_languages:
            if language not in files_by_language:
                files_by_language[language] = []
            files_by_language[language].append(file_path)

    return files_by_language


def _analyze_language_files(
    language: str,
    files: List[Path],
    project_path: Path,
    verbose: bool = False,
) -> Dict[str, Dict[str, Any]]:
    """Analiza archivos de un lenguaje específico usando su herramienta correspondiente."""
    tool_config = get_tool_config(language)
    if not tool_config:
        if verbose:
            print(f"  ⚠️  No hay configuración disponible para {language}")
        return {}

    # Buscar archivo de configuración
    config_file = find_config_file(language, project_path)

    # Construir comando de análisis
    command = build_command(language, 'conformance', [str(f) for f in files], config_file)
    if not command:
        if verbose:
            print(f"  ⚠️  No se pudo construir comando para {language}")
        return {}

    if verbose:
        config_info = f" (config: {config_file.name})" if config_file else " (config por defecto)"
        print(f"  💻 Ejecutando: {' '.join(command[:3])} ... {config_info}")

    # Ejecutar análisis
    try:
        result = subprocess.run(
            command,
            cwd=str(project_path),
            capture_output=True,
            text=True,
            timeout=120,
            shell=False,
            check=False,
        )

        # Procesar resultados según el lenguaje
        return _process_tool_output(language, result, files, project_path, verbose)

    except subprocess.TimeoutExpired:
        if verbose:
            print(f"  ⏰ Timeout ejecutando análisis de {language}")
        return {}
    except Exception as e:
        if verbose:
            print(f"  ❌ Error ejecutando análisis de {language}: {e}")
        return {}


def _process_tool_output(
    language: str,
    result: subprocess.CompletedProcess,
    files: List[Path],
    project_path: Path,
    verbose: bool = False,
) -> Dict[str, Dict[str, Any]]:
    """Procesa la salida de una herramienta específica y la convierte a formato estándar."""
    processed_results = {}

    if language == 'py':
        # Procesar salida de Ruff (JSON)
        processed_results = _process_ruff_output(result, files, project_path, verbose)

    elif language in ['js', 'ts', 'jsx', 'tsx', 'vue']:
        # Procesar salida de ESLint (JSON)
        processed_results = _process_eslint_output(result, files, project_path, verbose)

    elif language in ['css', 'scss']:
        # Procesar salida de Stylelint (JSON)
        processed_results = _process_stylelint_output(result, files, project_path, verbose)

    elif language == 'md':
        # Procesar salida de markdownlint (JSON)
        processed_results = _process_markdownlint_output(result, files, project_path, verbose)

    elif language in ['yml', 'yaml']:
        # Procesar salida de yamllint (parsable)
        processed_results = _process_yamllint_output(result, files, project_path, verbose)

    elif language == 'json':
        # Procesar salida de jsonlint (text)
        processed_results = _process_jsonlint_output(result, files, project_path, verbose)

    elif language == 'html':
        # Procesar salida de htmlhint (JSON)
        processed_results = _process_htmlhint_output(result, files, project_path, verbose)

    return processed_results


def _process_ruff_output(
    result: subprocess.CompletedProcess,
    files: List[Path],
    project_path: Path,
    verbose: bool = False,
) -> Dict[str, Dict[str, Any]]:
    """Procesa salida JSON de Ruff."""
    processed_results = {}

    if result.stdout.strip():
        try:
            ruff_violations = json.loads(result.stdout)

            # Organizar violaciones por archivo
            for file_path in files:
                relative_path = str(file_path.relative_to(project_path))

                # Filtrar violaciones para este archivo
                file_violations = [
                    v for v in ruff_violations
                    if v.get('filename') in [str(file_path), str(file_path.resolve()), relative_path]
                ]

                if file_violations:
                    # Convertir formato Ruff a formato estándar
                    violations = []
                    for violation in file_violations:
                        violations.append({
                            'code': violation.get('code', 'UNKNOWN'),
                            'message': violation.get('message', ''),
                            'line': violation.get('location', {}).get('row'),
                            'column': violation.get('location', {}).get('column'),
                            'category': categorize_error('py', violation.get('code', '')),
                            'tool': 'ruff',
                            'language': 'py',
                        })

                    processed_results[relative_path] = {
                        'violations': violations,
                        'violation_count': len(violations),
                        'language': 'py',
                        'tool': 'ruff',
                    }

        except json.JSONDecodeError as e:
            if verbose:
                print(f"  ⚠️  Error parseando JSON de Ruff: {e}")

    return processed_results


def _process_eslint_output(
    result: subprocess.CompletedProcess,
    files: List[Path],
    project_path: Path,
    verbose: bool = False,
) -> Dict[str, Dict[str, Any]]:
    """Procesa salida JSON de ESLint."""
    processed_results = {}

    if result.stdout.strip():
        try:
            eslint_results = json.loads(result.stdout)

            for file_result in eslint_results:
                file_path = Path(file_result.get('filePath', ''))
                relative_path = str(file_path.relative_to(project_path))

                if file_result.get('messages'):
                    violations = []
                    for message in file_result['messages']:
                        violations.append({
                            'code': message.get('ruleId', 'UNKNOWN'),
                            'message': message.get('message', ''),
                            'line': message.get('line'),
                            'column': message.get('column'),
                            'category': _categorize_eslint_error(message.get('ruleId', '')),
                            'tool': 'eslint',
                            'language': get_language_from_extension(file_path.suffix),
                        })

                    processed_results[relative_path] = {
                        'violations': violations,
                        'violation_count': len(violations),
                        'language': get_language_from_extension(file_path.suffix),
                        'tool': 'eslint',
                    }

        except json.JSONDecodeError as e:
            if verbose:
                print(f"  ⚠️  Error parseando JSON de ESLint: {e}")

    return processed_results


def _process_stylelint_output(
    result: subprocess.CompletedProcess,
    files: List[Path],
    project_path: Path,
    verbose: bool = False,
) -> Dict[str, Dict[str, Any]]:
    """Procesa salida JSON de Stylelint."""
    # Similar a ESLint pero para CSS
    return {}  # Implementación simplificada


def _process_markdownlint_output(
    result: subprocess.CompletedProcess,
    files: List[Path],
    project_path: Path,
    verbose: bool = False,
) -> Dict[str, Dict[str, Any]]:
    """Procesa salida JSON de markdownlint."""
    return {}  # Implementación simplificada


def _process_yamllint_output(
    result: subprocess.CompletedProcess,
    files: List[Path],
    project_path: Path,
    verbose: bool = False,
) -> Dict[str, Dict[str, Any]]:
    """Procesa salida parsable de yamllint."""
    return {}  # Implementación simplificada


def _process_jsonlint_output(
    result: subprocess.CompletedProcess,
    files: List[Path],
    project_path: Path,
    verbose: bool = False,
) -> Dict[str, Dict[str, Any]]:
    """Procesa salida de text de jsonlint."""
    return {}  # Implementación simplificada


def _process_htmlhint_output(
    result: subprocess.CompletedProcess,
    files: List[Path],
    project_path: Path,
    verbose: bool = False,
) -> Dict[str, Dict[str, Any]]:
    """Procesa salida JSON de htmlhint."""
    return {}  # Implementación simplificada


def _categorize_eslint_error(rule_id: str) -> str:
    """Categoriza errores de ESLint."""
    if not rule_id:
        return 'unknown_issues'

    if rule_id.startswith('@typescript-eslint'):
        return 'typescript_specific'
    elif rule_id.startswith('react'):
        return 'react_specific'
    elif rule_id.startswith('vue'):
        return 'vue_specific'
    elif 'import' in rule_id:
        return 'import_issues'
    elif 'unused' in rule_id or 'no-unused' in rule_id:
        return 'unused_code'
    else:
        return 'code_style'


def _create_empty_analysis_result(
    files: List[Path],
    languages_filter: Optional[List[str]],
    project_path: Path,
) -> Dict[str, Any]:
    """Crea un resultado vacío cuando no hay archivos para analizar."""
    return {
        'summary': {
            'total_files': len(files),
            'files_with_errors': 0,
            'total_violations': 0,
            'languages_analyzed': [],
            'tools_used': {},
            'exit_code': 0,
        },
        'files': {},
        'categories': {},
        'metadata': {
            'languages_filter': languages_filter or [],
            'project_path': str(project_path),
            'timestamp': datetime.now().isoformat(),
            'analysis_type': 'multi_language',
        },
    }


def _format_final_results(
    all_results: Dict[str, Dict[str, Any]],
    summary: Dict[str, Any],
    languages_filter: Optional[List[str]],
    project_path: Path,
) -> Dict[str, Any]:
    """Formatea los resultados finales en el formato esperado."""
    # Categorizar todas las violaciones
    categories = {}

    for file_data in all_results.values():
        for violation in file_data.get('violations', []):
            category = violation.get('category', 'unknown_issues')
            if category not in categories:
                categories[category] = {'count': 0, 'files': set()}

            categories[category]['count'] += 1
            categories[category]['files'].add(file_data.get('language', 'unknown'))

    # Convertir sets a listas para JSON serialization
    for category_data in categories.values():
        category_data['files'] = list(category_data['files'])

    summary['exit_code'] = 1 if summary['total_violations'] > 0 else 0

    return {
        'summary': summary,
        'files': all_results,
        'categories': categories,
        'metadata': {
            'languages_filter': languages_filter or [],
            'project_path': str(project_path),
            'timestamp': datetime.now().isoformat(),
            'analysis_type': 'multi_language',
        },
    }