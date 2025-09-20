import sys
from pathlib import Path
from typing import Any, Dict

# Añadir utils al path
sys.path.append(str(Path(__file__).parent.parent / 'utils'))

from multi_language_formatter import (
    format_files_by_language,
    get_files_with_errors_from_conformance
)


def main(flags: Dict[str, Any]) -> None:
    """
    Ejecuta formateo de código multi-lenguaje en archivos que tienen errores.

    Este script ejecuta primero code_conformance para identificar archivos con errores,
    luego aplica herramientas de formateo específicas por lenguaje solo a esos archivos.
    Soporta Python (ruff), JavaScript/TypeScript (prettier+eslint), CSS (stylelint),
    Markdown (prettier), JSON/YAML (prettier), HTML (prettier) y Vue.js.

    Parameters
    ----------
    flags : Dict[str, Any]
        Diccionario con las flags procesadas y validadas, incluyendo 'languages' opcional

    Side Effects
    ------------
    - Ejecuta subprocess de code_conformance para identificar archivos con errores
    - Aplica correcciones automáticas con herramientas específicas por lenguaje
    - Imprime resultados en stdout

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-19
    """
    try:
        # Determinar la ruta del proyecto
        current_path = Path(__file__).parent.parent.parent
        project_path = current_path

        # Extraer configuración de conformance para obtener archivos con errores
        conformance_flags = {
            'mode': flags.get('mode'),
            'files': flags.get('files'),
            'target_folder': flags.get('target_folder'),
            'exclude_paths': flags.get('exclude_paths'),
            'languages': flags.get('languages')
        }

        # Paso 1: Obtener archivos con errores usando code_conformance
        files_with_errors = get_files_with_errors_from_conformance(
            conformance_flags,
            project_path,
            verbose=flags.get('verbose', False)
        )

        if not files_with_errors:
            if flags.get('verbose'):
                print("✅ No hay archivos con errores para formatear")
            return

        # Paso 2: Aplicar formateo multi-lenguaje solo a archivos con errores
        formatting_result = format_files_by_language(
            files_with_errors,
            languages_filter=flags.get('languages'),
            project_path=project_path,
            verbose=flags.get('verbose', False)
        )

        # Mostrar resumen final
        if flags.get('verbose') or formatting_result['files_formatted'] > 0:
            files_count = formatting_result['files_formatted']
            total_count = formatting_result['total_files']
            languages_used = ', '.join(formatting_result['languages_processed'])

            if files_count > 0:
                print(f"\n✅ Formateo completado: {files_count}/{total_count} archivos")
                if languages_used:
                    print(f"🎯 Lenguajes procesados: {languages_used}")
            else:
                print(f"\n⚠️  No se pudieron formatear archivos: {total_count} intentados")

            if formatting_result['errors']:
                print(f"❌ {len(formatting_result['errors'])} errores encontrados")
                for error in formatting_result['errors']:
                    print(f"   • {error['language']}: {error['error']}")

    except (ValueError, TypeError, AttributeError, KeyError, OSError, ImportError) as e:
        print(f'❌ Error ejecutando el formatter multi-lenguaje: {e}')
        if flags.get('verbose'):
            import traceback
            traceback.print_exc()
        sys.exit(1)

