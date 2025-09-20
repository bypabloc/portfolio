"""
Sistema de configuración modular para herramientas de análisis por lenguaje.

Este módulo define las configuraciones y herramientas específicas para cada
lenguaje soportado por los scripts de conformance y formatting.

:Authors:
    - Pablo Contreras
:Created:
    - 2025-01-19
:Modified:
    - 2025-01-19
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
import json


# Mapeo de extensiones a lenguajes
EXTENSION_TO_LANGUAGE = {
    # Python
    '.py': 'py', '.pyi': 'py', '.pyx': 'py',

    # JavaScript/TypeScript
    '.js': 'js', '.mjs': 'js', '.cjs': 'js',
    '.ts': 'ts', '.tsx': 'tsx', '.jsx': 'jsx',

    # Markup & Documentation
    '.md': 'md', '.markdown': 'md',
    '.html': 'html', '.htm': 'html',
    '.vue': 'vue',
    '.astro': 'astro',

    # Data formats
    '.json': 'json', '.json5': 'json',
    '.yml': 'yml', '.yaml': 'yaml',

    # Styles
    '.css': 'css', '.scss': 'scss', '.sass': 'scss',
}

# Configuración de herramientas por lenguaje
LANGUAGE_TOOLS = {
    'py': {
        'name': 'Python',
        'conformance_tool': 'ruff',
        'formatter_tool': 'ruff',
        'config_files': ['ruff.toml', 'pyproject.toml'],
        'executable_paths': [
            '/home/bypabloc/projects/destacame/easy-pay/.venv/bin/ruff',
            'ruff',  # Fallback to PATH
        ],
        'conformance_command': ['{executable}', 'check', '{files}', '--output-format=json', '--no-fix'],
        'formatter_command': ['{executable}', 'check', '--fix', '{files}'],
        'config_flags': ['--config', '{config_file}'],
        'supported_extensions': ['.py', '.pyi', '.pyx'],
        'categories_map': {
            'E': 'style_errors', 'W': 'style_warnings', 'F': 'pyflakes_issues',
            'I': 'import_sorting', 'UP': 'python_upgrade', 'B': 'bugbear_issues',
            'C4': 'comprehensions', 'SIM': 'simplifications', 'PIE': 'pie_issues',
            'RET': 'return_issues', 'N': 'naming_issues', 'S': 'security_issues',
            'BLE': 'blind_except', 'A': 'builtins_issues', 'COM': 'comma_issues',
            'DJ': 'django_issues', 'PT': 'pytest_issues', 'ERA': 'commented_code',
            'T20': 'debug_prints', 'FIX': 'fixme_comments', 'G': 'logging_issues',
            'T10': 'debugger_issues', 'RUF': 'ruff_specific'
        }
    },

    'js': {
        'name': 'JavaScript',
        'conformance_tool': 'eslint',
        'formatter_tool': 'prettier',
        'config_files': ['.eslintrc.js', '.eslintrc.json', '.eslintrc.yml', 'eslint.config.js'],
        'executable_paths': ['npx eslint', 'eslint'],
        'conformance_command': ['{executable}', '{files}', '--format=json'],
        'formatter_command': ['npx', 'prettier', '--write', '{files}'],
        'config_flags': ['--config', '{config_file}'],
        'supported_extensions': ['.js', '.mjs', '.cjs'],
        'categories_map': {
            'error': 'errors',
            'warn': 'warnings',
            'off': 'disabled'
        }
    },

    'ts': {
        'name': 'TypeScript',
        'conformance_tool': 'eslint',
        'formatter_tool': 'prettier',
        'config_files': ['.eslintrc.js', '.eslintrc.json', 'tsconfig.json'],
        'executable_paths': ['npx eslint', 'eslint'],
        'conformance_command': ['{executable}', '{files}', '--format=json', '--parser=@typescript-eslint/parser'],
        'formatter_command': ['npx', 'prettier', '--write', '{files}'],
        'config_flags': ['--config', '{config_file}'],
        'supported_extensions': ['.ts'],
        'categories_map': {
            '@typescript-eslint': 'typescript_specific',
            'error': 'errors',
            'warn': 'warnings'
        }
    },

    'tsx': {
        'name': 'TypeScript JSX',
        'conformance_tool': 'eslint',
        'formatter_tool': 'prettier',
        'config_files': ['.eslintrc.js', '.eslintrc.json', 'tsconfig.json'],
        'executable_paths': ['npx eslint', 'eslint'],
        'conformance_command': ['{executable}', '{files}', '--format=json', '--parser=@typescript-eslint/parser'],
        'formatter_command': ['npx', 'prettier', '--write', '{files}'],
        'config_flags': ['--config', '{config_file}'],
        'supported_extensions': ['.tsx'],
        'categories_map': {
            'react': 'react_specific',
            '@typescript-eslint': 'typescript_specific',
            'error': 'errors',
            'warn': 'warnings'
        }
    },

    'jsx': {
        'name': 'JavaScript JSX',
        'conformance_tool': 'eslint',
        'formatter_tool': 'prettier',
        'config_files': ['.eslintrc.js', '.eslintrc.json'],
        'executable_paths': ['npx eslint', 'eslint'],
        'conformance_command': ['{executable}', '{files}', '--format=json'],
        'formatter_command': ['npx', 'prettier', '--write', '{files}'],
        'config_flags': ['--config', '{config_file}'],
        'supported_extensions': ['.jsx'],
        'categories_map': {
            'react': 'react_specific',
            'error': 'errors',
            'warn': 'warnings'
        }
    },

    'css': {
        'name': 'CSS',
        'conformance_tool': 'stylelint',
        'formatter_tool': 'prettier',
        'config_files': ['.stylelintrc.json', '.stylelintrc.js', 'stylelint.config.js'],
        'executable_paths': ['npx stylelint', 'stylelint'],
        'conformance_command': ['{executable}', '{files}', '--formatter=json'],
        'formatter_command': ['npx', 'prettier', '--write', '{files}'],
        'config_flags': ['--config', '{config_file}'],
        'supported_extensions': ['.css'],
        'categories_map': {
            'error': 'errors',
            'warning': 'warnings'
        }
    },

    'scss': {
        'name': 'SCSS/Sass',
        'conformance_tool': 'stylelint',
        'formatter_tool': 'prettier',
        'config_files': ['.stylelintrc.json', '.stylelintrc.js'],
        'executable_paths': ['npx stylelint', 'stylelint'],
        'conformance_command': ['{executable}', '{files}', '--formatter=json'],
        'formatter_command': ['npx', 'prettier', '--write', '{files}'],
        'config_flags': ['--config', '{config_file}'],
        'supported_extensions': ['.scss', '.sass'],
        'categories_map': {
            'error': 'errors',
            'warning': 'warnings'
        }
    },

    'md': {
        'name': 'Markdown',
        'conformance_tool': 'markdownlint',
        'formatter_tool': 'prettier',
        'config_files': ['.markdownlint.json', '.markdownlint.yml'],
        'executable_paths': ['npx markdownlint', 'markdownlint'],
        'conformance_command': ['{executable}', '{files}', '--json'],
        'formatter_command': ['npx', 'prettier', '--write', '{files}'],
        'config_flags': ['--config', '{config_file}'],
        'supported_extensions': ['.md', '.markdown'],
        'categories_map': {
            'MD': 'markdown_rules'
        }
    },

    'json': {
        'name': 'JSON',
        'conformance_tool': 'jsonlint',
        'formatter_tool': 'prettier',
        'config_files': ['.jsonschema/', 'package.json'],  # JSON Schema directory
        'executable_paths': ['npx jsonlint', 'jsonlint', 'python -m json.tool'],
        'conformance_command': ['{executable}', '{files}'],
        'formatter_command': ['npx', 'prettier', '--write', '{files}'],
        'config_flags': [],  # JSON doesn't typically use config files for linting
        'supported_extensions': ['.json', '.json5'],
        'categories_map': {
            'error': 'syntax_errors'
        }
    },

    'yml': {
        'name': 'YAML',
        'conformance_tool': 'yamllint',
        'formatter_tool': 'prettier',
        'config_files': ['.yamllint.yml', '.yamllint.yaml'],
        'executable_paths': ['yamllint'],
        'conformance_command': ['{executable}', '{files}', '--format=parsable'],
        'formatter_command': ['npx', 'prettier', '--write', '{files}'],
        'config_flags': ['-c', '{config_file}'],
        'supported_extensions': ['.yml', '.yaml'],
        'categories_map': {
            'error': 'syntax_errors',
            'warning': 'style_warnings'
        }
    },

    'yaml': {
        'name': 'YAML',
        'conformance_tool': 'yamllint',
        'formatter_tool': 'prettier',
        'config_files': ['.yamllint.yml', '.yamllint.yaml'],
        'executable_paths': ['yamllint'],
        'conformance_command': ['{executable}', '{files}', '--format=parsable'],
        'formatter_command': ['npx', 'prettier', '--write', '{files}'],
        'config_flags': ['-c', '{config_file}'],
        'supported_extensions': ['.yml', '.yaml'],
        'categories_map': {
            'error': 'syntax_errors',
            'warning': 'style_warnings'
        }
    },

    'html': {
        'name': 'HTML',
        'conformance_tool': 'htmlhint',
        'formatter_tool': 'prettier',
        'config_files': ['.htmlhintrc', 'htmlhint.json'],
        'executable_paths': ['npx htmlhint', 'htmlhint'],
        'conformance_command': ['{executable}', '{files}', '--format=json'],
        'formatter_command': ['npx', 'prettier', '--write', '{files}'],
        'config_flags': ['--config', '{config_file}'],
        'supported_extensions': ['.html', '.htm'],
        'categories_map': {
            'error': 'errors',
            'warning': 'warnings'
        }
    },

    'vue': {
        'name': 'Vue.js',
        'conformance_tool': 'eslint',
        'formatter_tool': 'prettier',
        'config_files': ['.eslintrc.js', '.eslintrc.json'],
        'executable_paths': ['npx eslint', 'eslint'],
        'conformance_command': ['{executable}', '{files}', '--format=json', '--ext=.vue'],
        'formatter_command': ['npx', 'prettier', '--write', '{files}'],
        'config_flags': ['--config', '{config_file}'],
        'supported_extensions': ['.vue'],
        'categories_map': {
            'vue': 'vue_specific',
            'error': 'errors',
            'warn': 'warnings'
        }
    },

    'astro': {
        'name': 'Astro',
        'conformance_tool': 'eslint',
        'formatter_tool': 'prettier',
        'config_files': ['eslint.config.js', '.eslintrc.js', '.eslintrc.json'],
        'executable_paths': ['npx eslint', 'eslint'],
        'conformance_command': ['{executable}', '{files}', '--format=json', '--ext=.astro'],
        'formatter_command': ['npx', 'prettier', '--write', '{files}'],
        'config_flags': ['--config', '{config_file}'],
        'supported_extensions': ['.astro'],
        'categories_map': {
            'astro': 'astro_specific',
            'astro/jsx-a11y': 'accessibility',
            'astro/no-deprecated': 'deprecated_usage',
            'error': 'errors',
            'warn': 'warnings'
        }
    }
}


def get_language_from_extension(file_extension: str) -> Optional[str]:
    """
    Obtiene el lenguaje correspondiente a una extensión de archivo.

    Args:
        file_extension: Extensión del archivo (ej: '.py', '.js')

    Returns:
        Lenguaje correspondiente o None si no está soportado
    """
    return EXTENSION_TO_LANGUAGE.get(file_extension.lower())


def get_languages_from_files(file_paths: List[str]) -> List[str]:
    """
    Detecta automáticamente los lenguajes basándose en las extensiones de archivo.

    Args:
        file_paths: Lista de rutas de archivos

    Returns:
        Lista única de lenguajes detectados
    """
    languages = set()

    for file_path in file_paths:
        extension = Path(file_path).suffix.lower()
        language = get_language_from_extension(extension)
        if language:
            languages.add(language)

    return sorted(list(languages))


def get_tool_config(language: str) -> Optional[Dict[str, Any]]:
    """
    Obtiene la configuración de herramientas para un lenguaje específico.

    Args:
        language: Código del lenguaje (ej: 'py', 'js', 'ts')

    Returns:
        Diccionario con configuración de herramientas o None si no está soportado
    """
    return LANGUAGE_TOOLS.get(language)


def find_config_file(language: str, project_path: Path) -> Optional[Path]:
    """
    Busca el archivo de configuración para un lenguaje en el proyecto.

    Args:
        language: Código del lenguaje
        project_path: Ruta raíz del proyecto

    Returns:
        Ruta al archivo de configuración encontrado o None
    """
    tool_config = get_tool_config(language)
    if not tool_config:
        return None

    for config_file in tool_config['config_files']:
        config_path = project_path / config_file
        if config_path.exists():
            return config_path

    return None


def get_executable_path(language: str) -> Optional[str]:
    """
    Obtiene la ruta del ejecutable para un lenguaje específico.

    Busca en las rutas definidas hasta encontrar un ejecutable válido.

    Args:
        language: Código del lenguaje

    Returns:
        Ruta del ejecutable encontrado o None
    """
    import subprocess

    tool_config = get_tool_config(language)
    if not tool_config:
        return None

    for executable_path in tool_config['executable_paths']:
        try:
            # Para comandos con espacios (ej: 'npx eslint'), tomar solo el primer comando
            test_executable = executable_path.split()[0]

            # Verificar si el ejecutable existe
            if Path(test_executable).exists():
                return executable_path

            # Si no es una ruta absoluta, buscar en PATH
            result = subprocess.run(
                ['which', test_executable],
                capture_output=True,
                text=True,
                shell=False
            )

            if result.returncode == 0:
                return executable_path

        except (subprocess.SubprocessError, OSError):
            continue

    return None


def build_command(language: str, command_type: str, files: List[str],
                  config_file: Optional[Path] = None) -> Optional[List[str]]:
    """
    Construye el comando completo para ejecutar una herramienta.

    Args:
        language: Código del lenguaje
        command_type: Tipo de comando ('conformance' o 'formatter')
        files: Lista de archivos a procesar
        config_file: Archivo de configuración opcional

    Returns:
        Lista con el comando completo o None si no se puede construir
    """
    tool_config = get_tool_config(language)
    if not tool_config:
        return None

    executable = get_executable_path(language)
    if not executable:
        return None

    # Obtener template del comando
    command_key = f'{command_type}_command'
    if command_key not in tool_config:
        return None

    command_template = tool_config[command_key].copy()

    # Reemplazar placeholders
    command = []
    for part in command_template:
        if '{executable}' in part:
            # Si el executable tiene espacios, dividirlo
            executable_parts = executable.split()
            command.extend(executable_parts)
        elif '{files}' in part:
            command.extend(files)
        elif '{config_file}' in part and config_file:
            command.append(str(config_file))
        else:
            command.append(part)

    # Agregar flags de configuración si hay archivo de config
    if config_file and tool_config.get('config_flags'):
        config_flags = []
        for flag in tool_config['config_flags']:
            if '{config_file}' in flag:
                config_flags.append(flag.replace('{config_file}', str(config_file)))
            else:
                config_flags.append(flag)

        # Insertar flags de config antes de los archivos
        files_index = None
        for i, part in enumerate(command):
            if part in files:
                files_index = i
                break

        if files_index is not None:
            command[files_index:files_index] = config_flags
        else:
            command.extend(config_flags)

    return command


def get_supported_languages() -> List[str]:
    """
    Obtiene la lista de lenguajes soportados.

    Returns:
        Lista de códigos de lenguajes soportados
    """
    return sorted(list(LANGUAGE_TOOLS.keys()))


def get_supported_extensions() -> List[str]:
    """
    Obtiene la lista de extensiones de archivo soportadas.

    Returns:
        Lista de extensiones soportadas
    """
    return sorted(list(EXTENSION_TO_LANGUAGE.keys()))


def validate_languages(languages: List[str]) -> List[str]:
    """
    Valida que una lista de lenguajes esté soportada.

    Args:
        languages: Lista de códigos de lenguajes a validar

    Returns:
        Lista de lenguajes no soportados (vacía si todos están soportados)
    """
    supported = get_supported_languages()
    return [lang for lang in languages if lang not in supported]


def categorize_error(language: str, error_code: str) -> str:
    """
    Categoriza un error según las reglas del lenguaje.

    Args:
        language: Código del lenguaje
        error_code: Código del error a categorizar

    Returns:
        Categoría del error o 'unknown_issues' si no se puede categorizar
    """
    tool_config = get_tool_config(language)
    if not tool_config or 'categories_map' not in tool_config:
        return 'unknown_issues'

    categories_map = tool_config['categories_map']

    # Buscar por prefijo del código
    for prefix, category in categories_map.items():
        if error_code.startswith(prefix):
            return category

    return 'unknown_issues'