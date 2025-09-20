from datetime import datetime
import fnmatch
import os
from pathlib import Path
import re
import sys
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Union

import git


def get_ignored_files_from_gitignore() -> Set[str]:
    """
    Lee el .gitignore y devuelve un conjunto de patrones de ignorado.

    Parsea el archivo .gitignore para extraer los patrones de archivos
    y directorios que deben ser ignorados por git.

    Returns
    -------
    set
        Conjunto de patrones de ignorado encontrados en .gitignore

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    patterns = set()
    gitignore_path = '.gitignore'
    if not os.path.exists(gitignore_path):
        return patterns

    with open(gitignore_path) as f:
        for line in f:
            line = line.strip()
            # Ignora líneas vacías y comentarios
            if line and not line.startswith('#'):
                patterns.add(line)
    return patterns


def is_ignored_by_pattern(file_path: str, patterns: Set[str]) -> bool:
    """
    Verifica si una ruta de archivo coincide con alguno de los patrones de ignorado.

    Compara la ruta de archivo contra los patrones usando fnmatch
    para determinar si debe ser ignorado.

    Parameters
    ----------
    file_path : str
        Ruta del archivo a verificar
    patterns : set or list
        Conjunto de patrones de ignorado

    Returns
    -------
    bool
        True si el archivo coincide con algún patrón de ignorado

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    for pattern in patterns:
        # Los patrones de fnmatch no manejan las barras diagonales al inicio,
        # así que las quitamos para la comparación
        if pattern.startswith('/'):
            pattern = pattern[1:]

        # Maneja patrones de directorio terminados en /
        if pattern.endswith('/'):
            if os.path.isdir(file_path):
                file_path += '/'
            if fnmatch.fnmatch(file_path, pattern + '*'):
                return True
        elif fnmatch.fnmatch(file_path, pattern):
            return True

    return False


def get_git_ignored_files() -> List[str]:
    """
    Obtiene archivos ignorados por git que no están cubiertos por .gitignore.

    Utiliza comandos git para identificar archivos ignorados por git
    que no están explícitamente listados en .gitignore.

    Returns
    -------
    List[str]
        Lista de archivos ignorados por git no cubiertos por .gitignore

    Raises
    ------
    git.InvalidGitRepositoryError
        Si el directorio actual no es un repositorio git válido

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    try:
        repo = git.Repo('.')
        ignored_patterns = get_ignored_files_from_gitignore()

        # Obtiene todos los archivos ignorados por git
        git_ignored_files_output = repo.git.ls_files('--others', '--ignored', '--exclude-standard').splitlines()

        unique_ignored_files = []

        for file_path in git_ignored_files_output:
            # Normaliza la ruta para que sea consistente
            normalized_path = os.path.normpath(file_path)

            # Filtra los archivos que ya están cubiertos por un patrón en .gitignore
            if not is_ignored_by_pattern(normalized_path, ignored_patterns):
                unique_ignored_files.append(normalized_path)

        return unique_ignored_files
    except git.InvalidGitRepositoryError:
        print('Advertencia: No es un repositorio Git válido')
        return []


def matches_ignore_pattern(file_path: str, pattern: str) -> bool:
    r"""
    Verifica si un archivo coincide con un patrón de ignorado usando regex.

    Convierte patrones tipo glob a regex y verifica coincidencias,
    soportando patrones complejos para filtrado avanzado de archivos.

    Soporta patrones como:
    - **/*/__init__ (todos los archivos __init__ en cualquier directorio)
    - .*\.pyc$ (archivos .pyc)
    - tests/.*\.py$ (archivos .py en directorio tests)

    Parameters
    ----------
    file_path : str
        Ruta del archivo a verificar
    pattern : str
        Patrón regex o glob a usar para la verificación

    Returns
    -------
    bool
        True si el archivo coincide con el patrón, False en caso contrario

    Raises
    ------
    re.error
        Si el patrón regex es inválido (maneja como búsqueda literal)

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    try:
        # Normalizar la ruta del archivo
        normalized_path = os.path.normpath(file_path).replace('\\', '/')

        # Convertir patrones tipo glob a regex si es necesario
        if '**/' in pattern or '*' in pattern:
            # Convertir patrón glob-like a regex
            regex_pattern = pattern.replace('**/', '.*/')  # **/ -> .*/
            regex_pattern = regex_pattern.replace('*', '[^/]*')  # * -> [^/]* (no cruza directorios)
            regex_pattern = regex_pattern.replace('/.*/', '/.*/')  # Restaurar .*/ para **/

            # Agregar ^ al inicio si no está presente para coincidencia desde el inicio
            if not regex_pattern.startswith('^'):
                regex_pattern = '.*' + regex_pattern  # Permitir coincidencia parcial

            # Si termina en directorio específico sin extensión, permitir extensiones
            if not regex_pattern.endswith('$') and '\\.' not in regex_pattern:
                regex_pattern += '(\\..*)?$'  # Permitir cualquier extensión
            elif not regex_pattern.endswith('$'):
                regex_pattern += '$'
        else:
            # Es un patrón regex normal
            regex_pattern = pattern

        # Compilar y verificar el patrón
        compiled_pattern = re.compile(regex_pattern, re.IGNORECASE)
        return bool(compiled_pattern.search(normalized_path))

    except re.error:
        # Si el patrón regex es inválido, intentar como patrón literal
        return pattern in file_path
    except (ValueError, TypeError, AttributeError):
        # En caso de error, no excluir el archivo
        return False


def should_exclude_file(file_path: str, flags: Dict[str, Any]) -> bool:
    """
    Determina si un archivo debe ser excluido según las flags.

    Aplica múltiples criterios de exclusión basados en extensiones,
    archivos vacíos y patrones regex según la configuración de flags.

    Parameters
    ----------
    file_path : str
        Ruta del archivo a evaluar
    flags : dict
        Diccionario de flags con criterios de exclusión

    Returns
    -------
    bool
        True si el archivo debe ser excluido, False si debe incluirse

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    file_ext = Path(file_path).suffix.lower()
    if file_ext.startswith('.'):
        file_ext = file_ext[1:]  # Remover el punto

    # Si se especifica only_extension, solo incluir esas extensiones
    only_extension = flags.get('only_extension', [])
    if only_extension and file_ext not in only_extension:
        return True  # Excluir si no está en la lista de extensiones permitidas

    # Excluir por extensiones (solo si no se usa only_extension)
    excludes_extension = flags.get('excludes_extension', [])
    if excludes_extension and not only_extension and file_ext in excludes_extension:
        return True

    # Excluir archivos vacíos si se especifica
    exclude_empty = flags.get('exclude_empty', False)
    if exclude_empty and should_exclude_empty_file(file_path):
        return True

    # Excluir por patrones regex si se especifica
    ignore_patterns = flags.get('ignore_patterns', [])
    if ignore_patterns:
        for pattern in ignore_patterns:
            if matches_ignore_pattern(file_path, pattern):
                return True

    return False


def get_git_tracked_files() -> Set[str]:
    """
    Obtiene lista de archivos trackeados por git.

    Utiliza comandos git para obtener todos los archivos que están
    actualmente bajo control de versiones.

    Returns
    -------
    set
        Conjunto de archivos trackeados por git

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    try:
        repo = git.Repo('.')
        # Obtener archivos trackeados y staged
        tracked_files = repo.git.ls_files().splitlines()
        return set(tracked_files)
    except (git.InvalidGitRepositoryError, git.GitCommandError, OSError):
        return set()


def get_git_tracked_directories() -> Set[str]:
    """
    Obtiene carpetas que contienen archivos trackeados por git.

    Analiza los archivos trackeados por git para identificar todos
    los directorios padre que contienen contenido versionado.

    Returns
    -------
    set
        Conjunto de directorios que contienen archivos trackeados

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    tracked_files = get_git_tracked_files()
    tracked_dirs = set()

    for file_path in tracked_files:
        # Agregar todas las carpetas padre del archivo
        dir_path = os.path.dirname(file_path)
        while dir_path:
            tracked_dirs.add(dir_path)
            parent_dir = os.path.dirname(dir_path)
            if parent_dir == dir_path:  # Llegamos a la raíz
                break
            dir_path = parent_dir

    return tracked_dirs


def get_git_base_branch() -> str:
    """
    Detecta la rama base del repositorio.

    Identifica automáticamente la rama base principal del repositorio
    buscando entre ramas comunes como dev, main, master, develop.

    Returns
    -------
    str
        Nombre de la rama base detectada, 'main' por defecto si no se encuentra

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    try:
        repo = git.Repo('.')

        # Lista de ramas base comunes en orden de preferencia
        base_branches = ['dev', 'main', 'master', 'develop']

        # Obtener todas las ramas remotas
        remote_refs = [ref.name for ref in repo.refs if 'origin/' in ref.name]

        # Buscar rama base que existe
        for branch in base_branches:
            if f'origin/{branch}' in remote_refs:
                return branch

        # Si no encuentra ninguna, usar la primera rama remota disponible
        if remote_refs:
            return remote_refs[0].split('/')[-1]

        return 'main'  # Fallback por defecto
    except (git.InvalidGitRepositoryError, git.GitCommandError, OSError):
        return 'main'


def get_git_files_by_mode(mode: str = 'changed') -> Dict[str, List[str]]:
    """
    Obtiene archivos según el modo de git especificado.

    Utiliza comandos git para obtener archivos en diferentes estados
    (staged, unstaged, untracked, stash, unmerged) y los organiza
    por categorías para fácil procesamiento.

    Parameters
    ----------
    mode : str, default='changed'
        Modo de git: 'changed', 'staged', 'unstaged', 'stash', 'unmerged', 'all'

    Returns
    -------
    dict
        Diccionario con archivos organizados por categoría:
        {'staged': [], 'unstaged': [], 'untracked': [], 'stash': [], 'unmerged': [], 'changed': []}

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    try:
        repo = git.Repo('.')
        result = {
            'staged': [],
            'unstaged': [],
            'untracked': [],
            'stash': [],
            'unmerged': [],  # Archivos no mergeados a rama base
            'changed': [],  # Combinación de staged + unstaged + untracked
        }

        if mode in ['changed', 'staged', 'unmerged'] or mode == 'all':
            # Archivos staged (en el index vs HEAD)
            for item in repo.index.diff('HEAD'):
                if item.a_path:
                    result['staged'].append(item.a_path)

        if mode in ['changed', 'unstaged', 'unmerged'] or mode == 'all':
            # Archivos unstaged (working dir vs index)
            for item in repo.index.diff(None):
                if item.a_path:
                    result['unstaged'].append(item.a_path)

        if mode in ['changed', 'unmerged'] or mode == 'all':
            # Archivos untracked
            result['untracked'] = list(repo.untracked_files)

        if mode == 'stash' or mode == 'all':
            # Archivos en stash
            try:
                stash_list = repo.git.stash('list').splitlines()
                if stash_list:
                    # Obtener archivos del stash más reciente (stash@{0})
                    stash_files = repo.git.stash('show', '--name-only', 'stash@{0}').splitlines()
                    result['stash'] = [f.strip() for f in stash_files if f.strip()]
            except (git.GitCommandError, git.GitCommandNotFound, OSError):
                # Si no hay stash o error, lista vacía
                result['stash'] = []

        if mode == 'unmerged' or mode == 'all':
            # Archivos no mergeados a rama base (implementación directa)
            try:
                base_branch = get_git_base_branch()
                current_branch = repo.active_branch.name

                if current_branch == base_branch:
                    # Si estamos en la rama base, no hay archivos no mergeados
                    result['unmerged'] = []
                else:
                    # Obtener archivos de commits no mergeados
                    base_ref = base_branch
                    try:
                        # Verificar si existe origin/base_branch
                        repo.commit(f'origin/{base_branch}')
                        base_ref = f'origin/{base_branch}'
                    except (git.BadName, git.GitCommandError) as e:
                        print(f"⚠️  Error accediendo a origen/{base_branch}: {type(e).__name__}", file=sys.stderr)

                    # Usar git diff con rango para obtener archivos no mergeados
                    diff_output = repo.git.diff('--name-only', f'{base_ref}..HEAD')
                    unmerged_files = []
                    if diff_output:
                        for file_path in diff_output.splitlines():
                            if file_path.strip():
                                unmerged_files.append(file_path.strip())

                    result['unmerged'] = unmerged_files
            except (git.InvalidGitRepositoryError, git.GitCommandError, OSError) as e:
                print(f'Error obteniendo archivos no mergeados: {e}')
                result['unmerged'] = []

        # Construir lista 'changed' como combinación
        result['changed'] = list(set(result['staged'] + result['unstaged'] + result['untracked']))

        return result

    except (git.InvalidGitRepositoryError, git.GitCommandError, OSError) as e:
        print(f"Error obteniendo archivos por modo '{mode}': {e}")
        return {
            'staged': [],
            'unstaged': [],
            'untracked': [],
            'stash': [],
            'changed': [],
        }


def get_uncommitted_files() -> List[str]:
    """
    Obtiene archivos que tienen cambios en commits no mergeados vs la rama base.

    Identifica archivos que han sido modificados en commits de la rama actual
    que no han sido mergeados a la rama base, incluyendo cambios locales.

    Returns
    -------
    List[str]
        Lista de archivos con cambios no mergeados a la rama base

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    try:
        repo = git.Repo('.')
        base_branch = get_git_base_branch()
        current_branch = repo.active_branch.name

        if current_branch == base_branch:
            # Si estamos en la rama base, obtener solo archivos modificados localmente (uncommitted)
            git_files = get_git_files_by_mode('changed')
            return git_files['changed']
        # Obtener archivos de commits no mergeados a la rama base
        try:
            # Intentar usar origin/base_branch si existe, sino usar base_branch local
            base_ref = base_branch
            try:
                # Verificar si existe origin/base_branch
                repo.commit(f'origin/{base_branch}')
                base_ref = f'origin/{base_branch}'
            except (git.BadName, git.GitCommandError) as e:
                # Si no existe origin/base_branch, usar la rama local
                print(f"⚠️  Error accediendo a origen/{base_branch}: {type(e).__name__}", file=sys.stderr)

            # Obtener archivos modificados en commits no mergeados usando el rango correcto
            unmerged_files = set()

            # Usar git diff con rango base_ref..HEAD para obtener archivos de commits no mergeados
            diff_output = repo.git.diff('--name-only', f'{base_ref}..HEAD')
            if diff_output:
                for file_path in diff_output.splitlines():
                    if file_path.strip():
                        unmerged_files.add(file_path.strip())

            # Agregar archivos locales no committed también
            git_files = get_git_files_by_mode('changed')
            unmerged_files.update(git_files['changed'])

            return list(unmerged_files)

        except (git.InvalidGitRepositoryError, git.GitCommandError, OSError):
            # Fallback: intentar con git diff básico
            try:
                diff_output = repo.git.diff('--name-only', base_branch)
                return [f.strip() for f in diff_output.splitlines() if f.strip()]
            except (git.GitCommandError, OSError):
                # Último fallback: archivos locales únicamente
                git_files = get_git_files_by_mode('changed')
                return git_files['changed']

    except (git.InvalidGitRepositoryError, git.GitCommandError, OSError) as e:
        print(f'Error obteniendo archivos no mergeados: {e}')
        return []


def get_deleted_files() -> List[str]:
    """
    Obtiene archivos que han sido eliminados vs la rama base.

    Identifica archivos que existían en la rama base pero han sido
    eliminados en la rama actual o en el working directory.

    Returns
    -------
    List[str]
        Lista de archivos eliminados respecto a la rama base

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    try:
        repo = git.Repo('.')
        base_branch = get_git_base_branch()
        current_branch = repo.active_branch.name

        deleted_files = []

        if current_branch == base_branch:
            # Si estamos en la rama base, obtener archivos eliminados localmente
            # Archivos eliminados en el working directory pero aún en el index
            for item in repo.index.diff(None):
                if item.deleted_file:
                    deleted_files.append(item.a_path)

            # Archivos eliminados en el index vs HEAD
            for item in repo.index.diff('HEAD'):
                if item.deleted_file:
                    deleted_files.append(item.a_path)

        else:
            # Comparar rama actual vs rama base para encontrar eliminados
            try:
                base_ref = f'origin/{base_branch}'
                if base_ref not in [ref.name for ref in repo.refs]:
                    base_ref = base_branch

                # Obtener archivos eliminados entre ramas usando --diff-filter=D
                deleted_output = repo.git.diff('--name-only', '--diff-filter=D', base_ref)
                if deleted_output:
                    for item in deleted_output.splitlines():
                        if item.strip():
                            deleted_files.append(item.strip())

                # También verificar archivos eliminados localmente
                for item in repo.index.diff(None):
                    if item.deleted_file:
                        deleted_files.append(item.a_path)

                for item in repo.index.diff('HEAD'):
                    if item.deleted_file:
                        deleted_files.append(item.a_path)

            except (git.InvalidGitRepositoryError, git.GitCommandError, OSError):
                # Fallback: solo archivos localmente eliminados
                for item in repo.index.diff(None):
                    if item.deleted_file:
                        deleted_files.append(item.a_path)

        return list(set(deleted_files))

    except (git.InvalidGitRepositoryError, git.GitCommandError, OSError) as e:
        print(f'Error obteniendo archivos eliminados: {e}')
        return []


def get_file_deleted_date(file_path: str) -> Optional[datetime]:
    """
    Obtiene la fecha de eliminación de un archivo desde git.

    Busca en el historial de git el último commit donde el archivo
    fue eliminado para determinar cuándo ocurrió la eliminación.

    Parameters
    ----------
    file_path : str
        Ruta del archivo eliminado

    Returns
    -------
    datetime or None
        Fecha de eliminación del archivo, None si no se puede determinar

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    try:
        repo = git.Repo('.')
        # Buscar el último commit donde el archivo fue eliminado
        commits = list(repo.iter_commits(paths=file_path, max_count=10))

        for commit in commits:
            # Verificar si el archivo fue eliminado en este commit
            for item in commit.diff(commit.parents[0] if commit.parents else None):
                if item.deleted_file and item.a_path == file_path:
                    return datetime.fromtimestamp(commit.committed_date)

        # Si no se encuentra eliminación específica, usar fecha del último commit
        if commits:
            return datetime.fromtimestamp(commits[0].committed_date)

        return None
    except (git.InvalidGitRepositoryError, git.GitCommandError, OSError):
        return None


def get_file_content_from_git(file_path: str, base_branch: Optional[str] = None) -> Optional[str]:
    """
    Obtiene el contenido de un archivo eliminado desde git history.

    Recupera el contenido de un archivo que ya no existe en el working directory
    pero que puede obtenerse desde el historial de git.

    Parameters
    ----------
    file_path : str
        Ruta del archivo eliminado
    base_branch : str, optional
        Rama base desde donde obtener el archivo, auto-detectada si es None

    Returns
    -------
    str or None
        Contenido del archivo desde git history, None si no se puede obtener

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    try:
        repo = git.Repo('.')

        # Si no se especifica rama base, usar la detectada
        if base_branch is None:
            base_branch = get_git_base_branch()

        # Intentar obtener el archivo desde la rama base
        try:
            base_ref = f'origin/{base_branch}'
            if base_ref not in [ref.name for ref in repo.refs]:
                base_ref = base_branch

            # Obtener el contenido del archivo desde la rama base
            return repo.git.show(f'{base_ref}:{file_path}')
        except (git.GitCommandError, git.BadName):
            # Si falla con la rama base, intentar desde el último commit
            try:
                commits = list(repo.iter_commits(paths=file_path, max_count=1))
                if commits:
                    commit = commits[0]
                    return repo.git.show(f'{commit.hexsha}:{file_path}')
            except (git.GitCommandError, git.BadName) as e:
                print(f"⚠️  Error obteniendo contenido de archivo desde git: {type(e).__name__}", file=sys.stderr)

        return None
    except (git.InvalidGitRepositoryError, git.GitCommandError, OSError):
        return None


def get_file_dates(file_path: str) -> Tuple[Optional[datetime], Optional[datetime]]:
    """
    Obtiene fechas de creación y modificación de un archivo.

    Utiliza información del sistema de archivos para obtener las fechas
    de creación y modificación de un archivo.

    Parameters
    ----------
    file_path : str
        Ruta del archivo

    Returns
    -------
    Tuple[datetime, datetime] or Tuple[None, None]
        Tupla con fecha de creación y fecha de modificación,
        (None, None) si el archivo no existe o hay error

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    try:
        if not os.path.exists(file_path):
            return None, None

        stat_info = os.stat(file_path)

        # Fecha de modificación
        modified_time = datetime.fromtimestamp(stat_info.st_mtime)

        # Fecha de creación (en sistemas Unix, st_ctime es cambio de metadatos, no creación)
        # En Windows, st_ctime sí es creación. Para Unix usamos st_mtime como aproximación
        if hasattr(stat_info, 'st_birthtime'):
            # macOS tiene st_birthtime
            created_time = datetime.fromtimestamp(stat_info.st_birthtime)
        else:
            # En Linux, usamos st_ctime como aproximación
            created_time = datetime.fromtimestamp(stat_info.st_ctime)

        return created_time, modified_time
    except (OSError, PermissionError):
        return None, None


def get_file_content(file_path: str, exclude_empty: bool = False) -> Union[str, bool, None]:
    """
    Obtiene el contenido completo de un archivo de forma segura.

    Lee el contenido de un archivo manejando diferentes codificaciones
    y tipos de archivo (texto, binario) de forma robusta.

    Parameters
    ----------
    file_path : str
        Ruta del archivo a leer
    exclude_empty : bool, default=False
        Si excluir archivos vacíos (devolver None en lugar del contenido)

    Returns
    -------
    str, bool, or None
        Contenido del archivo (str), False si está vacío, None si se excluye o hay error

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    try:
        # Verificar que el archivo existe
        if not os.path.exists(file_path):
            return None

        # Intentar leer como texto UTF-8 primero
        try:
            with open(file_path, encoding='utf-8') as f:
                content = f.read()

                # Si está vacío y se debe excluir, devolver None
                if exclude_empty and (not content or content.strip() == ''):
                    return None

                # Si está vacío pero no se excluye, devolver False para indicarlo
                if not exclude_empty and (not content or content.strip() == ''):
                    return False

                return content
        except UnicodeDecodeError:
            # Si falla UTF-8, intentar con latin1
            try:
                with open(file_path, encoding='latin1') as f:
                    content = f.read()

                    # Si está vacío y se debe excluir, devolver None
                    if exclude_empty and (not content or content.strip() == ''):
                        return None

                    # Si está vacío pero no se excluye, devolver False para indicarlo
                    if not exclude_empty and (not content or content.strip() == ''):
                        return False

                    return content
            except (UnicodeDecodeError, PermissionError):
                # Si es un archivo binario, devolver información básica
                file_size = os.path.getsize(file_path)
                return f'<Archivo binario - {file_size} bytes>'
    except (OSError, PermissionError):
        return None


def should_exclude_empty_file(file_path: str) -> bool:
    """
    Determina si un archivo debe ser excluido por estar vacío.

    Verifica si un archivo no tiene contenido o solo contiene espacios en blanco
    para determinar si debe ser excluido del análisis.

    Parameters
    ----------
    file_path : str
        Ruta del archivo a verificar

    Returns
    -------
    bool
        True si el archivo está vacío y debe ser excluido

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    try:
        if not os.path.exists(file_path):
            return True

        # Leer contenido para verificar si está vacío
        try:
            with open(file_path, encoding='utf-8') as f:
                content = f.read()
                return not content or content.strip() == ''
        except UnicodeDecodeError:
            # Intentar con latin1
            try:
                with open(file_path, encoding='latin1') as f:
                    content = f.read()
                    return not content or content.strip() == ''
            except (OSError, UnicodeDecodeError, PermissionError):
                # Si no se puede leer como texto, no excluir (puede ser binario)
                return False
    except (OSError, PermissionError):
        return True


def build_structure_dict(folders: List[str], files: List[str]) -> Dict[str, Any]:
    """
    Construye un diccionario de estructura jerárquica.

    Crea una representación jerárquica anidada de la estructura
    de carpetas y archivos para visualización y procesamiento.

    Parameters
    ----------
    folders : List[str]
        Lista de rutas de carpetas
    files : List[str]
        Lista de rutas de archivos

    Returns
    -------
    dict
        Diccionario anidado representando la estructura jerárquica

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    structure = {}

    # Agregar carpetas
    for folder in folders:
        parts = folder.split('/')
        current = structure
        for part in parts:
            if part not in current:
                current[part] = {}
            current = current[part]

    # Agregar archivos
    for file_path in files:
        parts = file_path.split('/')
        if len(parts) == 1:
            # Archivo en raíz
            structure[parts[0]] = file_path
        else:
            # Archivo en subcarpeta
            folder_parts = parts[:-1]
            file_name = parts[-1]

            current = structure
            for part in folder_parts:
                if part not in current:
                    current[part] = {}
                current = current[part]

            current[file_name] = file_path

    return structure


def build_folders_structure(folders: List[str]) -> Dict[str, Any]:
    """
    Construye estructura solo de carpetas/directorios.

    Crea una representación jerárquica anidada conteniendo únicamente
    la estructura de directorios sin incluir archivos.

    Parameters
    ----------
    folders : List[str]
        Lista de rutas de carpetas

    Returns
    -------
    dict
        Diccionario anidado representando solo la estructura de directorios

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    structure = {}

    for folder in folders:
        parts = folder.split('/')
        current = structure

        for part in parts:
            if part not in current:
                current[part] = {}
            current = current[part]

    return structure


def get_project_structure(flags: Dict[str, Any]) -> Dict[str, Any]:
    """
    Obtiene la estructura del proyecto según las flags.

    Función principal que coordina la obtención de archivos y carpetas
    del proyecto según las configuraciones especificadas en flags,
    aplicando filtros y modos git correspondientes.

    Parameters
    ----------
    flags : dict
        Diccionario de configuraciones que incluye modos git,
        filtros de extensiones, exclusiones y opciones de formato

    Returns
    -------
    dict
        Estructura completa del proyecto con archivos, carpetas,
        contenido y metadatos organizados por categorías

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    structure = {'folders': [], 'files': {}}

    # Inicializar deleted si se solicita
    if flags.get('include_deleted', False):
        structure['deleted'] = {
            'folders': [],
            'files': {},
            'structure': {},
            'structure_folders': {},
        }

    # Inicializar git_modes si se especifica un modo de git
    git_mode = flags.get('git_mode')
    if git_mode and git_mode != 'all':
        structure['git_modes'] = {
            git_mode: {
                'folders': [],
                'files': {},
                'structure': {},
                'structure_folders': {},
            },
        }
    elif git_mode == 'all':
        structure['git_modes'] = {
            'staged': {
                'folders': [],
                'files': {},
                'structure': {},
                'structure_folders': {},
            },
            'unstaged': {
                'folders': [],
                'files': {},
                'structure': {},
                'structure_folders': {},
            },
            'untracked': {
                'folders': [],
                'files': {},
                'structure': {},
                'structure_folders': {},
            },
            'stash': {
                'folders': [],
                'files': {},
                'structure': {},
                'structure_folders': {},
            },
            'unmerged': {
                'folders': [],
                'files': {},
                'structure': {},
                'structure_folders': {},
            },
            'changed': {
                'folders': [],
                'files': {},
                'structure': {},
                'structure_folders': {},
            },
        }

    include_ignored = flags.get('include_ignored', False)
    include_deleted = flags.get('include_deleted', False)
    git_mode = flags.get('git_mode')

    # Si se especifica git_mode, procesarlo
    if git_mode:
        git_files_by_mode = get_git_files_by_mode(git_mode)

        if git_mode == 'all':
            # Procesar todos los modos
            for mode_name, file_list in git_files_by_mode.items():
                if mode_name in structure['git_modes']:
                    processed_files = {}
                    processed_folders = set()

                    for file_path in file_list:
                        if not should_exclude_file(file_path, flags):
                            exclude_empty = flags.get('exclude_empty', False)
                            content = get_file_content(file_path, exclude_empty)

                            if exclude_empty and content is None:
                                continue

                            created_date, modified_date = get_file_dates(file_path)

                            processed_files[file_path] = {
                                'path': file_path,
                                'content': content,
                                'created_date': created_date.isoformat() if created_date else None,
                                'modified_date': modified_date.isoformat() if modified_date else None,
                            }

                            # Agregar carpetas padre
                            dir_path = os.path.dirname(file_path)
                            while dir_path and dir_path != '.':
                                processed_folders.add(dir_path)
                                parent_dir = os.path.dirname(dir_path)
                                if parent_dir == dir_path:
                                    break
                                dir_path = parent_dir

                    structure['git_modes'][mode_name]['files'] = processed_files
                    structure['git_modes'][mode_name]['folders'] = sorted(processed_folders)
                    structure['git_modes'][mode_name]['structure'] = build_structure_dict(
                        structure['git_modes'][mode_name]['folders'],
                        list(processed_files.keys()),
                    )
                    structure['git_modes'][mode_name]['structure_folders'] = build_folders_structure(
                        structure['git_modes'][mode_name]['folders'],
                    )
        else:
            # Procesar modo específico
            file_list = git_files_by_mode.get(git_mode, [])
            processed_files = {}
            processed_folders = set()

            for file_path in file_list:
                if not should_exclude_file(file_path, flags):
                    exclude_empty = flags.get('exclude_empty', False)
                    content = get_file_content(file_path, exclude_empty)

                    if exclude_empty and content is None:
                        continue

                    created_date, modified_date = get_file_dates(file_path)

                    processed_files[file_path] = {
                        'path': file_path,
                        'content': content,
                        'created_date': created_date.isoformat() if created_date else None,
                        'modified_date': modified_date.isoformat() if modified_date else None,
                    }

                    # Agregar carpetas padre
                    dir_path = os.path.dirname(file_path)
                    while dir_path and dir_path != '.':
                        processed_folders.add(dir_path)
                        parent_dir = os.path.dirname(dir_path)
                        if parent_dir == dir_path:
                            break
                        dir_path = parent_dir

            # Para modo específico, guardar directamente en structure principal
            structure['files'] = processed_files
            structure['folders'] = sorted(processed_folders)
            structure['structure'] = build_structure_dict(structure['folders'], list(processed_files.keys()))
            structure['structure_folders'] = build_folders_structure(structure['folders'])

            # Devolver inmediatamente para modos específicos
            return structure

    # Si queremos archivos eliminados junto con unmerged
    if git_mode == 'unmerged' and include_deleted:
        deleted_files = get_deleted_files()

        # Procesar archivos eliminados
        processed_deleted_files = {}
        deleted_folders = set()

        for file_path in deleted_files:
            if not should_exclude_file(file_path, flags):
                # Obtener contenido desde git history y fecha de eliminación
                content = get_file_content_from_git(file_path)

                # Si el archivo eliminado estaba vacío y se deben excluir vacíos, omitir
                exclude_empty = flags.get('exclude_empty', False)
                if exclude_empty and (not content or content.strip() == ''):
                    continue

                # Si no se excluyen vacíos pero el contenido está vacío, marcar como False
                if not exclude_empty and (not content or content.strip() == ''):
                    content = False

                created_date, _ = get_file_dates(file_path) if os.path.exists(file_path) else (None, None)
                deleted_date = get_file_deleted_date(file_path)

                processed_deleted_files[file_path] = {
                    'path': file_path,
                    'content': content,
                    'created_date': created_date.isoformat() if created_date else None,
                    'deleted_date': deleted_date.isoformat() if deleted_date else None,
                }

                # Agregar carpetas padre
                dir_path = os.path.dirname(file_path)
                while dir_path and dir_path != '.':
                    deleted_folders.add(dir_path)
                    parent_dir = os.path.dirname(dir_path)
                    if parent_dir == dir_path:
                        break
                    dir_path = parent_dir

        structure['deleted']['files'] = processed_deleted_files
        structure['deleted']['folders'] = sorted(deleted_folders)
        structure['deleted']['structure'] = build_structure_dict(
            structure['deleted']['folders'], list(processed_deleted_files.keys()),
        )
        structure['deleted']['structure_folders'] = build_folders_structure(structure['deleted']['folders'])

    # Si queremos archivos no mergeados (unmerged)
    if git_mode == 'unmerged':
        unmerged_files = get_uncommitted_files()  # Renombrar para claridad

        # Procesar archivos unmerged (no mergeados a rama base)
        processed_files = {}
        processed_folders = set()

        for file_path in unmerged_files:
            if not should_exclude_file(file_path, flags):
                # Obtener contenido y fechas
                exclude_empty = flags.get('exclude_empty', False)
                content = get_file_content(file_path, exclude_empty)

                # Si el archivo está vacío y se debe excluir, omitirlo
                if exclude_empty and content is None:
                    continue

                created_date, modified_date = get_file_dates(file_path)

                processed_files[file_path] = {
                    'path': file_path,
                    'content': content,
                    'created_date': created_date.isoformat() if created_date else None,
                    'modified_date': modified_date.isoformat() if modified_date else None,
                }

                # Agregar carpetas padre
                dir_path = os.path.dirname(file_path)
                while dir_path and dir_path != '.':
                    processed_folders.add(dir_path)
                    parent_dir = os.path.dirname(dir_path)
                    if parent_dir == dir_path:
                        break
                    dir_path = parent_dir

        structure['files'] = processed_files
        structure['folders'] = sorted(processed_folders)
        structure['structure'] = build_structure_dict(structure['folders'], list(processed_files.keys()))
        structure['structure_folders'] = build_folders_structure(structure['folders'])

        return structure

    # Si solo queremos carpetas raíz
    if flags.get('only_folders_root', False):
        if include_ignored:
            # Incluir todo - comportamiento original
            for item in os.listdir('.'):
                if (os.path.isdir(item) and not item.startswith('.') and
                        not should_exclude_file(item, flags)):
                    structure['folders'].append(item)
        else:
            # Solo carpetas que contienen archivos rastreados por git
            tracked_dirs = get_git_tracked_directories()
            root_dirs = set()
            for tracked_dir in tracked_dirs:
                # Obtener solo el directorio raíz
                root_part = tracked_dir.split('/')[0] if '/' in tracked_dir else tracked_dir
                if root_part and not root_part.startswith('.'):
                    root_dirs.add(root_part)

            # Filtrar por extensiones si es necesario
            structure['folders'] = sorted([d for d in root_dirs if not should_exclude_file(d, flags)])

        return structure

    if include_ignored:
        # Comportamiento original - incluir todo
        for root, dirs, files in os.walk('.'):
            # Normalizar la ruta root
            root_display = '' if root == '.' else root[2:]  # Remover './'

            # Filtrar directorios ocultos y excluidos
            dirs[:] = [
                d for d in dirs if not d.startswith('.') and not should_exclude_file(os.path.join(root, d), flags)
            ]

            # Agregar carpetas
            for dir_name in dirs:
                full_dir_path = os.path.join(root_display, dir_name) if root_display else dir_name
                structure['folders'].append(full_dir_path)

            # Agregar archivos con contenido y fechas
            for file_name in files:
                if not file_name.startswith('.'):  # Ignorar archivos ocultos
                    full_file_path = os.path.join(root_display, file_name) if root_display else file_name
                    if not should_exclude_file(full_file_path, flags):
                        exclude_empty = flags.get('exclude_empty', False)
                        content = get_file_content(full_file_path, exclude_empty)

                        # Si el archivo está vacío y se debe excluir, omitirlo
                        if exclude_empty and content is None:
                            continue

                        created_date, modified_date = get_file_dates(full_file_path)

                        if full_file_path not in structure['files']:
                            structure['files'][full_file_path] = {
                                'path': full_file_path,
                                'content': content,
                                'created_date': created_date.isoformat() if created_date else None,
                                'modified_date': modified_date.isoformat() if modified_date else None,
                            }
    else:
        # Solo archivos y carpetas rastreados por git
        tracked_files = get_git_tracked_files()
        tracked_dirs = get_git_tracked_directories()

        # Procesar archivos rastreados con contenido y fechas
        processed_files = {}
        for file_path in tracked_files:
            if not should_exclude_file(file_path, flags):
                exclude_empty = flags.get('exclude_empty', False)
                content = get_file_content(file_path, exclude_empty)

                # Si el archivo está vacío y se debe excluir, omitirlo
                if exclude_empty and content is None:
                    continue

                created_date, modified_date = get_file_dates(file_path)

                processed_files[file_path] = {
                    'path': file_path,
                    'content': content,
                    'created_date': created_date.isoformat() if created_date else None,
                    'modified_date': modified_date.isoformat() if modified_date else None,
                }

        structure['files'] = processed_files

        # Filtrar carpetas rastreadas
        for dir_path in tracked_dirs:
            if not should_exclude_file(dir_path, flags):
                structure['folders'].append(dir_path)

    # Ordenar resultados
    structure['folders'].sort()

    # Agregar estructuras jerárquicas
    file_paths = list(structure['files'].keys())
    structure['structure'] = build_structure_dict(structure['folders'], file_paths)
    structure['structure_folders'] = build_folders_structure(structure['folders'])

    return structure


def display_structure(structure: Dict[str, Any], flags: Dict[str, Any]) -> None:
    """
    Muestra la estructura del proyecto.

    Presenta la estructura del proyecto en formato visual o lista
    según las configuraciones de flags, incluyendo archivos, carpetas
    y metadatos relevantes.

    Parameters
    ----------
    structure : dict
        Estructura del proyecto obtenida de get_project_structure
    flags : dict
        Configuraciones de formato y visualización

    Side Effects
    ------------
    Imprime la estructura formateada en stdout

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    only_list = flags.get('only_list', False)

    if only_list:
        # Formato de lista con separador para procesamiento
        separator = ';'

        if flags.get('only_folders_root', False):
            # Solo carpetas, una lista separada por ;
            print(separator.join(structure['folders']))
        else:
            # Todas las carpetas y archivos juntos
            file_paths = list(structure['files'].keys())
            all_items = structure['folders'] + file_paths
            if all_items:
                print(separator.join(all_items))
            else:
                print('')  # Lista vacía
    else:
        # Formato visual original
        if flags.get('only_folders_root', False):
            print('Carpetas raíz del proyecto:')
            print('-' * 30)
            for folder in structure['folders']:
                print(f'📁 {folder}')

            print(f'\nTotal: {len(structure["folders"])} carpetas')
        else:
            # Mostrar carpetas
            if structure['folders']:
                print('Carpetas:')
                print('-' * 20)
                for folder in structure['folders']:
                    print(f'📁 {folder}')
                print()

            # Mostrar archivos
            if structure['files']:
                print('Archivos:')
                print('-' * 20)
                for file_path, file_info in structure['files'].items():
                    dates_info = ''
                    if file_info.get('created_date') and file_info.get('modified_date'):
                        dates_info = f' (Creado: {file_info["created_date"][:10]}, Modificado: {file_info["modified_date"][:10]})'
                    print(f'📄 {file_path}{dates_info}')
                print()

            # Mostrar información de archivos eliminados si están disponibles
            if 'deleted' in structure and structure['deleted']['files']:
                print('\nArchivos eliminados:')
                print('-' * 20)
                for file_path, file_info in structure['deleted']['files'].items():
                    dates_info = ''
                    if file_info.get('deleted_date'):
                        dates_info = f' (Eliminado: {file_info["deleted_date"][:10]})'
                    print(f'🗑️ {file_path}{dates_info}')
                print()

            deleted_count = len(structure.get('deleted', {}).get('files', {}))
            summary_text = f'Resumen: {len(structure["folders"])} carpetas, {len(structure["files"])} archivos'
            if deleted_count > 0:
                summary_text += f', {deleted_count} eliminados'
            print(summary_text)


def main(flags: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Función principal que muestra la estructura de archivos y carpetas del proyecto.

    Detecta automáticamente si fue invocada desde CLI o desde Python y
    actúa en consecuencia, devolviendo datos o imprimiendo resultados.
    Coordina toda la funcionalidad del script de estructura de archivos.

    Parameters
    ----------
    flags : dict
        Diccionario con las flags procesadas que incluye configuraciones
        de filtrado, modos git y opciones de formato

    Returns
    -------
    dict or None
        Si es invocada desde Python, devuelve la estructura como dict.
        Si es invocada desde CLI, imprime la estructura y no devuelve nada.

    Examples
    --------
    >>> structure = main({'include_ignored': False, 'git_mode': 'unmerged'})
    >>> main({'only_list': True, 'only_extension': ['py']})

    :Authors:
        - Pablo Contreras
    :Created:
        - 2025-09-04
    :Modified:
        - 2025-01-14
    """
    invoked_from = flags.get('_invoked_from', 'python')  # Por defecto asume Python
    only_list = flags.get('only_list', False)

    # Obtener la estructura
    structure = get_project_structure(flags)

    # Si fue invocada desde Python, devolver la estructura directamente
    if invoked_from == 'python':
        return structure

    # Si fue invocada desde CLI, mostrar la información
    if not only_list:
        # Solo mostrar encabezado si NO es modo lista (para permitir procesamiento limpio)
        print(f'Estructura del proyecto - Directorio: {os.getcwd()}')

        # Mostrar información del modo activo
        git_mode = flags.get('git_mode')
        if git_mode == 'unmerged':
            base_branch = get_git_base_branch()
            mode_text = f"Modo: Archivos no mergeados a rama '{base_branch}'"
            if flags.get('include_deleted', False):
                mode_text += ' (incluye eliminados)'
            print(mode_text)
        elif git_mode:
            mode_descriptions = {
                'staged': 'Archivos en staging area (listos para commit)',
                'unstaged': 'Archivos con cambios no staged',
                'untracked': 'Archivos nuevos no rastreados por git',
                'changed': 'Archivos con cualquier cambio (staged + unstaged + untracked)',
                'stash': 'Archivos del stash más reciente',
                'unmerged': 'Archivos no mergeados a rama base',
                'all': 'Todos los archivos separados por categoría',
            }
            description = mode_descriptions.get(git_mode, f'Modo git: {git_mode}')
            print(f'Modo: {description}')
        elif flags.get('include_ignored', False):
            print('Modo: Incluye archivos ignorados por git')
        else:
            print('Modo: Solo archivos rastreados por git (por defecto)')

        print('=' * 60)

    # Mostrar la estructura en formato CLI
    display_structure(structure, flags)
    return None


if __name__ == '__main__':
    # Para pruebas directas (normalmente se ejecuta a través de run.py)
    test_flags = {
        'include_ignored': False,
        'excludes_extension': [],
        'only_folders_root': False,
        'include_deleted': False,
        'exclude_empty': False,
        'git_mode': None,
    }
    main(test_flags)
