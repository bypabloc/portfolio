# genstruct

Muestra la estructura de archivos y carpetas del proyecto, con soporte avanzado para:
- Archivos con cambios pendientes vs rama base (uncommitted)  
- Archivos eliminados con recuperación desde git history
- Filtrado de archivos vacíos para identificar código importante
- Múltiples formatos de salida (visual, JSON, lista procesable)

## Flags disponibles

- `--include-ignored` - Incluir archivos ignorados por git (por defecto se excluyen)
- `--excludes-extension="ext1|ext2|..."` - Excluir archivos con extensiones específicas  
  - Ejemplo: `--excludes-extension="json|csv|sql"`
- `--only-extension="ext1|ext2|..."` - Incluir SOLO archivos con extensiones específicas
  - Ejemplo: `--only-extension="py|js|ts"`
  - **Nota**: No se puede usar junto con `--excludes-extension`  
- `--only-folders-root` - Mostrar solo carpetas raíz del proyecto
- `--only-list` - Devolver solo lista con separador (;) sin formato visual
- `--git-mode="unmerged"` - Mostrar archivos no mergeados a rama base (detecta automáticamente dev/main/master)
- `--include-deleted` - Incluir archivos eliminados en key 'deleted' (solo funciona con --git-mode="unmerged")
- `--exclude-empty` - Excluir archivos vacíos/sin contenido (ej: __init__.py vacíos) para identificar archivos importantes
- `--git-mode="modo"` - Filtrar por modo git específico (changed, staged, unstaged, stash, all)

## Comportamiento por defecto

- Muestra solo archivos y carpetas rastreados por git
- Excluye automáticamente archivos en .gitignore y no rastreados
- Para carpetas raíz usa: `git ls-files --others --ignored --exclude-standard --directory`
- Con `--git-mode="unmerged"`: Detecta automáticamente la rama base (dev > main > master > develop) y compara archivos
- Con `--git-mode`: Filtra archivos por estado específico de git sin comparar con rama base

## Modos de Git disponibles

La flag `--git-mode` permite filtrar archivos por su estado específico en git:

| Modo | Descripción | Archivos incluidos |
|------|-------------|-------------------|
| `changed` | Archivos con cambios | staged + unstaged + untracked |
| `staged` | Archivos en staging area | Listos para commit |
| `unstaged` | Archivos con cambios no staged | Modificados pero no añadidos |
| `untracked` | Archivos no rastreados | Nuevos archivos no en git |
| `unmerged` | Archivos no mergeados | Cambios vs rama base |
| `stash` | Archivos en stash | Del stash más reciente (stash@{0}) |
| `all` | Todos los modos | Separados por categoría |

## Estructura de respuesta (nuevo formato)

### Formato JSON cuando se invoca desde Python

```json
{
  "folders": ["carpeta1", "carpeta2/subcarpeta"],
  "files": {
    "archivo1.py": {
      "path": "archivo1.py",
      "content": "contenido completo del archivo...",
      "created_date": "2025-01-14T10:30:00",
      "modified_date": "2025-01-14T15:45:00"
    },
    "empty_file.py": {
      "path": "empty_file.py",
      "content": false,
      "created_date": "2025-01-14T10:30:00",
      "modified_date": "2025-01-14T15:45:00"
    },
    "carpeta/archivo2.js": {
      "path": "carpeta/archivo2.js", 
      "content": "contenido completo...",
      "created_date": "2025-01-14T11:20:00",
      "modified_date": "2025-01-14T16:10:00"
    }
  },
  "structure": {
    "archivo1.py": "archivo1.py",
    "carpeta": {
      "archivo2.js": "carpeta/archivo2.js"
    }
  },
  "structure_folders": {
    "carpeta": {
      "subcarpeta": {}
    }
  },
  "deleted": {
    "folders": ["carpeta_eliminada"],
    "files": {
      "archivo_eliminado.py": {
        "path": "archivo_eliminado.py",
        "content": "contenido recuperado desde git...",
        "created_date": "2025-01-10T10:30:00",
        "deleted_date": "2025-01-14T15:45:00"
      }
    },
    "structure": {
      "archivo_eliminado.py": "archivo_eliminado.py",
      "carpeta_eliminada": {
        "otro_eliminado.js": "carpeta_eliminada/otro_eliminado.js"
      }
    },
    "structure_folders": {
      "carpeta_eliminada": {}
    }
  }
}
```

### Formato JSON con git_modes (cuando se usa --git-mode)

```json
{
  "git_modes": {
    "staged": {
      "folders": ["src"],
      "files": {
        "src/main.py": {
          "path": "src/main.py",
          "content": "contenido en staging area...",
          "created_date": "2025-01-14T10:30:00",
          "modified_date": "2025-01-14T15:45:00"
        }
      },
      "structure": { "src": { "main.py": "src/main.py" } },
      "structure_folders": { "src": {} }
    },
    "unstaged": {
      "folders": [],
      "files": {
        "README.md": {
          "path": "README.md",
          "content": "cambios no staged...",
          "created_date": "2025-01-13T10:30:00",
          "modified_date": "2025-01-14T16:00:00"
        }
      },
      "structure": { "README.md": "README.md" },
      "structure_folders": {}
    }
  }
}
```

## Ejemplos de uso

### Estructura básica
```bash
python scripts/run.py genstruct
```

### Solo carpetas raíz
```bash
python scripts/run.py genstruct --only-folders-root
```

### Archivos no mergeados (unmerged)
```bash
# Mostrar solo archivos no mergeados a rama base
python scripts/run.py genstruct --git-mode="unmerged"

# Incluir archivos eliminados junto con los no mergeados
python scripts/run.py genstruct --git-mode="unmerged" --include-deleted

# Combinar con solo lista para procesamiento
python scripts/run.py genstruct --git-mode="unmerged" --only-list

# Excluir archivos temporales de los unmerged
python scripts/run.py genstruct --git-mode="unmerged" --excludes-extension="tmp|log|pyc"

# Solo archivos Python no mergeados
python scripts/run.py genstruct --git-mode="unmerged" --only-extension="py"

# Solo documentación no mergeada
python scripts/run.py genstruct --git-mode="unmerged" --only-extension="md|rst"

# Obtener archivos eliminados con contenido desde git history
python scripts/run.py genstruct --git-mode="unmerged" --include-deleted --only-list

# Excluir archivos vacíos para identificar solo archivos importantes
python scripts/run.py genstruct --git-mode="unmerged" --exclude-empty

# Combinaciones útiles para análisis
python scripts/run.py genstruct --git-mode="unmerged" --include-deleted --exclude-empty
```

### Modos de Git específicos (nuevo)
```bash
# Ver solo archivos en staging area
python scripts/run.py genstruct --git-mode="staged"

# Ver archivos con cambios no staged
python scripts/run.py genstruct --git-mode="unstaged"

# Ver archivos no rastreados por git
python scripts/run.py genstruct --git-mode="untracked"

# Ver archivos en stash
python scripts/run.py genstruct --git-mode="stash"

# Ver archivos con cualquier cambio (staged + unstaged + untracked)
python scripts/run.py genstruct --git-mode="changed"

# Ver todos los modos separados por categoría
python scripts/run.py genstruct --git-mode="all"

# Combinar con otras flags
python scripts/run.py genstruct --git-mode="staged" --exclude-empty
python scripts/run.py genstruct --git-mode="all" --only-list
```

### Lista para procesamiento en scripts
```bash
python scripts/run.py genstruct --only-list --only-folders-root
```

### Filtrar por tipos de archivos específicos
```bash
# Excluir tipos de archivos específicos
python scripts/run.py genstruct --excludes-extension="json|csv|sql"
python scripts/run.py genstruct --excludes-extension="pyc|log|tmp"

# Incluir SOLO tipos de archivos específicos  
python scripts/run.py genstruct --only-extension="py|js|ts"
python scripts/run.py genstruct --only-extension="md|txt|yml"

# Combinar con git-mode
python scripts/run.py genstruct --git-mode="unmerged" --only-extension="py|md"
```

### Incluir archivos ignorados
```bash
python scripts/run.py genstruct --include-ignored --only-folders-root
```

### Combinando flags
```bash
python scripts/run.py genstruct --only-list --excludes-extension="pyc|log"
```

## Casos de uso comunes

### Para desarrollo
- **Ver estructura git limpia**: `python scripts/run.py genstruct`
- **Solo carpetas principales**: `python scripts/run.py genstruct --only-folders-root`
- **Excluir archivos temporales**: `python scripts/run.py genstruct --excludes-extension="tmp|log|cache"`
- **Solo archivos Python**: `python scripts/run.py genstruct --only-extension="py"`
- **Solo documentación**: `python scripts/run.py genstruct --only-extension="md|rst|txt"`
- **Archivos no mergeados**: `python scripts/run.py genstruct --git-mode="unmerged"`
- **Incluir archivos eliminados**: `python scripts/run.py genstruct --git-mode="unmerged" --include-deleted`
- **Solo archivos importantes (no vacíos)**: `python scripts/run.py genstruct --git-mode="unmerged" --exclude-empty`
- **Revisar cambios antes de commit**: `python scripts/run.py genstruct --git-mode="unmerged" --only-list`
- **Analizar eliminaciones**: `python scripts/run.py genstruct --git-mode="unmerged" --include-deleted --only-list`
- **Análisis completo sin archivos vacíos**: `python scripts/run.py genstruct --git-mode="unmerged" --include-deleted --exclude-empty`
- **Solo archivos en staging area**: `python scripts/run.py genstruct --git-mode="staged"`
- **Archivos con cambios locales**: `python scripts/run.py genstruct --git-mode="unstaged"`
- **Vista completa por categorías**: `python scripts/run.py genstruct --git-mode="all"`

### Para scripts y automatización
- **Lista procesable**: `python scripts/run.py genstruct --only-list --only-folders-root`
- **Archivos no mergeados para CI/CD**: `python scripts/run.py genstruct --git-mode="unmerged" --only-list`
- **Incluir eliminados en CI/CD**: `python scripts/run.py genstruct --git-mode="unmerged" --include-deleted --only-list`
- **Solo archivos importantes para CI/CD**: `python scripts/run.py genstruct --git-mode="unmerged" --exclude-empty --only-list`
- **Solo archivos staged para CI/CD**: `python scripts/run.py genstruct --git-mode="staged" --only-list`
- **Archivos por modo específico**: `python scripts/run.py genstruct --git-mode="unstaged" --only-list`
- **En scripts bash**:
  ```bash
  # Procesar carpetas
  FOLDERS=$(python scripts/run.py genstruct --only-list --only-folders-root)
  for folder in $(echo "$FOLDERS" | tr ';' ' '); do
      echo "Procesando carpeta: $folder"
  done
  
  # Procesar archivos no mergeados
  UNMERGED_FILES=$(python scripts/run.py genstruct --git-mode="unmerged" --only-list)
  for file in $(echo "$UNMERGED_FILES" | tr ';' ' '); do
      echo "Archivo no mergeado: $file"
      # Ejecutar lint, tests, etc. solo en archivos no mergeados
  done
  
  # Procesar archivos eliminados junto con no mergeados
  ALL_CHANGES=$(python scripts/run.py genstruct --git-mode="unmerged" --include-deleted --only-list)
  for file in $(echo "$ALL_CHANGES" | tr ';' ' '); do
      echo "Cambio detectado: $file"
      # Procesar tanto no mergeados como eliminados
  done
  
  # Procesar solo archivos importantes (no vacíos)
  IMPORTANT_FILES=$(python scripts/run.py genstruct --git-mode="unmerged" --exclude-empty --only-list)
  for file in $(echo "$IMPORTANT_FILES" | tr ';' ' '); do
      echo "Archivo importante no mergeado: $file"
      # Ejecutar análisis solo en archivos con contenido relevante
  done
  ```

### Para análisis
- **Ver todo incluyendo ignorados**: `python scripts/run.py genstruct --include-ignored` (no recomendado para uso regular)
- **Analizar archivos no mergeados**: `python scripts/run.py genstruct --git-mode="unmerged"` (incluye fechas)
- **Filtrar solo archivos importantes**: `python scripts/run.py genstruct --exclude-empty` (excluye __init__.py vacíos, etc.)

## Formato de salida

### Modo visual (por defecto)
```
Estructura del proyecto - Directorio: /path/to/project
Modo: Solo archivos rastreados por git (por defecto)
============================================================
Carpetas raíz del proyecto:
------------------------------
📁 src
📁 lib
...
Total: 19 carpetas
```

### Modo visual con archivos modificados (incluye fechas)
```
Estructura del proyecto - Directorio: /path/to/project
Modo: Archivos con cambios pendientes vs rama 'dev' (incluye eliminados)
============================================================
Archivos:
--------------------
📄 main.py (Creado: 2025-01-14, Modificado: 2025-01-14)
📄 tests/test_feature.py (Creado: 2025-01-13, Modificado: 2025-01-14)

Archivos eliminados:
--------------------
🗑️ old_file.py (Eliminado: 2025-01-14)
🗑️ deprecated/utils.js (Eliminado: 2025-01-13)

Resumen: 2 carpetas, 2 archivos, 2 eliminados
```

### Modo lista (`--only-list`)
```
src;lib;components;utils;tests;docs;scripts;...
```

## Notas técnicas

- **Separador en modo lista**: `;` (no permitido en nombres de archivos/carpetas)
- **Integración con git**: Usa `git ls-files` para determinar archivos rastreados
- **Detección de rama base**: Prioridad: dev > main > master > develop
- **Fechas de archivos**: Incluye fecha de creación y modificación en formato ISO
- **Archivos eliminados**: Recupera contenido desde git history con fecha de eliminación
- **Contenido de archivos**: Lee contenido completo, maneja archivos binarios automáticamente  
- **Estructura jerárquica**: Devuelve `structure` y `structure_folders` para representación en árbol
- **Key 'deleted'**: Solo se incluye cuando se usa `--include-deleted` con `--git-mode="unmerged"`
- **Archivos vacíos**: Con `--exclude-empty` se omiten, sin la flag `content: false` indica archivo vacío
- **Detección de vacíos**: Archivos con contenido vacío o solo espacios en blanco se consideran vacíos
- **Casos comunes**: __init__.py vacíos, archivos de configuración sin contenido, etc.
- **Modo silencioso**: `--only-list` suprime todos los mensajes de debug y encabezados
- **Compatibilidad**: Todas las flags se pueden combinar entre sí
- **Modos de git**: `--git-mode` filtra por estado específico (staged, unstaged, untracked, stash, changed, all)\n- **Key 'git_modes'**: Solo se incluye cuando se usa `--git-mode`, organiza archivos por categoría\n- **Diferencia con --git-mode="unmerged"**: otros `--git-mode` no comparan con rama base, solo estado local\n- **Manejo de errores**: Archivos no accesibles devuelven `null` en lugar de fallar