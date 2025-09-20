# code_conformance

**Script de análisis de conformidad de código para múltiples lenguajes (modo read-only)**

Analiza la calidad del código, estándares y mejores prácticas usando herramientas especializadas para cada lenguaje.

⚠️  **IMPORTANTE**: Este script **SOLO ANALIZA** código (read-only). **NO aplica correcciones automáticas**.

## ¿Qué hace?

- ✅ **Analiza código multi-lenguaje** con herramientas especializadas
- ✅ **Reporta violaciones** categorizadas por lenguaje y tipo
- ✅ **Retorna exit codes** apropiados (0=sin errores, 1=hay errores) para CI/CD
- ✅ **Modo read-only** garantizado - NO modifica archivos
- ✅ **Auto-detección** de lenguajes por extensión de archivo
- ❌ **NO formatea archivos** (usar script `code_formatter` para eso)
- ❌ **NO aplica correcciones** automáticamente

## Lenguajes Soportados

### Python - Ruff (800+ reglas)
- **Extensiones**: `.py`, `.pyi`, `.ipynb`, `.pyw`, `.py3`, `.pyz`, `.pyx`, `.pxd`, `.pxi`
- **Herramienta**: Ruff con configuración `ruff.toml`
- **Categorías**: E/W, F, I, UP, B, C4, SIM, PIE, RET, N, S, BLE, A, COM, DJ, PT, ERA, T20, FIX, G, T10, RUF

### JavaScript/TypeScript - ESLint + Prettier
- **Extensiones**: `.js`, `.mjs`, `.cjs`, `.ts`, `.tsx`, `.jsx`
- **Herramientas**: ESLint + Prettier
- **Configuración**: `.eslintrc.js`, `.prettierrc`, `tsconfig.json`

### CSS/SCSS - Stylelint
- **Extensiones**: `.css`, `.scss`, `.sass`
- **Herramienta**: Stylelint
- **Configuración**: `.stylelintrc.json`

### Markdown - markdownlint
- **Extensiones**: `.md`, `.markdown`
- **Herramienta**: markdownlint
- **Configuración**: `.markdownlint.json`

### JSON - JSON Schema
- **Extensiones**: `.json`, `.json5`
- **Herramienta**: JSON Schema validation
- **Configuración**: `.jsonschema/` directory

### YAML - yamllint
- **Extensiones**: `.yml`, `.yaml`
- **Herramienta**: yamllint
- **Configuración**: `.yamllint.yml`

### HTML - HTMLHint
- **Extensiones**: `.html`, `.htm`
- **Herramienta**: HTMLHint
- **Configuración**: `.htmlhintrc`

### Vue - Vue ESLint
- **Extensiones**: `.vue`
- **Herramienta**: Vue ESLint plugin
- **Configuración**: `.eslintrc.js` con Vue plugin

## Flags disponibles

**Selección de archivos (obligatorio - elegir una):**
- `--mode="all|changed|staged|unstaged|stash|unmerged"` - Archivos por modo git
- `--files="archivo1 archivo2"` - Archivos específicos a analizar

**Filtros de lenguaje:**
- `--languages="js,ts,py"` - Lenguajes específicos a analizar (opcional)
  - **Lenguajes soportados**: `js`, `ts`, `py`, `md`, `json`, `yml`, `yaml`, `html`, `css`, `scss`, `vue`, `jsx`, `tsx`
  - **Auto-detección**: Si no se especifica, detecta automáticamente por extensión de archivo

**Opciones de salida:**
- `--output-format="console|json|html"` - Formato de salida (default: console)
- `--output-location="path/to/output"` - Ubicación del archivo de salida

**Opciones adicionales:**
- `--verbose` - Mostrar información detallada del proceso (default: false)
- `--project-path="/path/to/project"` - Ruta del proyecto (default: auto-detect)
- `--target-folder="path/to/folder"` - Carpeta específica a analizar (default: todos los archivos)
- `--exclude-paths="tests,node_modules"` - Paths a excluir del análisis

⚠️ **IMPORTANTE**: Debe usar o `--mode` o `--files`, pero no ambos. Son opciones mutuamente excluyentes.

⚠️  **NOTA**: El formato `html` con `--output-location` está **pendiente de implementación**. Los formatos `console` y `json` están completamente implementados.

## Ejemplos de uso

### Análisis básico (multi-lenguaje)
```bash
# Auto-detecta todos los lenguajes en archivos no mergeados
python scripts/run.py code_conformance --mode="unmerged"

# Con información detallada
python scripts/run.py code_conformance --mode="changed" --verbose

# Todos los archivos del proyecto
python scripts/run.py code_conformance --mode="all"
```

### Por lenguajes específicos
```bash
# Solo Python
python scripts/run.py code_conformance --mode="changed" --languages="py"

# JavaScript y TypeScript
python scripts/run.py code_conformance --mode="staged" --languages="js,ts"

# Solo archivos de estilo
python scripts/run.py code_conformance --mode="all" --languages="css,scss"

# Documentación
python scripts/run.py code_conformance --mode="changed" --languages="md,json,yml"

# Frontend completo
python scripts/run.py code_conformance --mode="unmerged" --languages="js,ts,vue,css,html"
```

### Por modo de git
```bash
# Archivos no mergeados (útil para PRs)
python scripts/run.py code_conformance --mode="unmerged" --verbose

# Archivos con cambios locales
python scripts/run.py code_conformance --mode="changed" --languages="py,js"

# Archivos en staging area (pre-commit)
python scripts/run.py code_conformance --mode="staged"

# Archivos modificados pero no staged
python scripts/run.py code_conformance --mode="unstaged" --languages="js,ts,vue"
```

### Para carpetas específicas
```bash
# Analizar solo carpeta src (auto-detect lenguajes)
python scripts/run.py code_conformance --target-folder="src"

# Solo Python en carpeta de tests
python scripts/run.py code_conformance --target-folder="tests" --languages="py"

# Frontend en carpeta components
python scripts/run.py code_conformance --target-folder="src/components" --languages="vue,js,css"
```

### Para archivos específicos multi-lenguaje
```bash
# Analizar archivos específicos (auto-detect)
python scripts/run.py code_conformance --files="src/main.py src/utils.js styles.css"

# Solo Python en archivos específicos
python scripts/run.py code_conformance --files="models.py views.py" --languages="py"

# Mix de lenguajes específicos
python scripts/run.py code_conformance --files="main.js style.css README.md" --languages="js,css,md"

# Con verbose para debugging
python scripts/run.py code_conformance --files="src/app.vue src/main.ts" --verbose
```

### Output JSON (integración con CLIs)
```bash
# JSON a stdout (para pipes e integración)
python scripts/run.py code_conformance --mode="unmerged" --output-format="json"

# JSON a archivo específico
python scripts/run.py code_conformance --mode="changed" --output-format="json" --output-location="report.json"

# Procesar JSON con jq (ejemplo)
python scripts/run.py code_conformance --mode="staged" --output-format="json" 2>/dev/null | jq '.summary'

# Extraer solo archivos con errores
python scripts/run.py code_conformance --mode="unmerged" --output-format="json" 2>/dev/null | jq '.files | keys[]'

# Contar violaciones por categoría
python scripts/run.py code_conformance --mode="all" --output-format="json" 2>/dev/null | jq '.categories'

# JSON para archivos específicos
python scripts/run.py code_conformance --files="easy_pay/models.py accounts/views.py" --output-format="json" 2>/dev/null | jq '.summary'
```

### Verificar exit codes (CI/CD)
```bash
# Ejecutar y verificar si hay errores
python scripts/run.py code_conformance --mode="staged"
echo $?  # Retorna: 0 si sin errores, 1 si hay errores

# JSON con exit code verificado
python scripts/run.py code_conformance --mode="unmerged" --output-format="json" --output-location="ci_report.json"
echo $?  # Retorna: 1 si hay errores (mismo comportamiento)

# Uso en scripts de CI/CD (modo git)
if python scripts/run.py code_conformance --mode="unmerged"; then
    echo "✅ Code quality OK"
else
    echo "❌ Code quality issues found"
    exit 1
fi

# Uso en scripts para archivos específicos
FILES="easy_pay/models.py accounts/views.py"
if python scripts/run.py code_conformance --files="$FILES"; then
    echo "✅ Code quality OK for specified files"
else
    echo "❌ Code quality issues found in specified files"
    exit 1
fi
```

## Comando Ruff equivalente

El script ejecuta internamente:
```bash
ruff check [archivos...] --output-format=json --no-fix --config ruff.toml
```

Si prefieres usar Ruff directamente:
```bash
# Análisis básico
ruff check . --config ruff.toml --no-fix

# Con estadísticas
ruff check . --config ruff.toml --no-fix --statistics

# Solo archivos específicos
ruff check archivo.py --config ruff.toml --no-fix
```

## Estructura del JSON Output

Cuando usas `--output-format="json"`, el output tiene esta estructura:

```json
{
  "summary": {
    "total_files": 61,           // Total archivos analizados
    "files_with_errors": 37,     // Archivos que tienen violaciones
    "total_violations": 585,     // Total de violaciones encontradas
    "exit_code": 1               // 0=sin errores, 1=hay errores
  },
  "files": {
    "path/to/file.py": {
      "violations": [
        {
          "code": "E501",              // Código de regla Ruff
          "message": "Line too long",  // Descripción de la violación
          "line": 42,                  // Línea del error
          "column": 80,                // Columna del error
          "category": "style_errors",  // Categoría automática
          "url": "https://docs..."     // Link a documentación
        }
      ],
      "violation_count": 1
    }
  },
  "categories": {
    "style_errors": {
      "count": 120,                    // Total violaciones de esta categoría
      "files": ["file1.py", "file2.py"] // Archivos afectados
    }
  },
  "metadata": {
    "mode": "unmerged",              // Modo usado
    "timestamp": "2025-09-06...",    // Timestamp del análisis
    "extensions_analyzed": [".py", ".pyi", ...],
    "ruff_config": "ruff.toml"       // Archivo de configuración usado
  }
}
```

## Categorías de análisis Ruff

El script categoriza automáticamente las **800+ reglas** en:

- **E/W** - `style_errors/style_warnings`: pycodestyle errors/warnings
- **F** - `pyflakes_issues`: imports, unused variables, syntax errors  
- **I** - `import_sorting`: isort import organization
- **UP** - `python_upgrade`: pyupgrade syntax modernization
- **B** - `bugbear_issues`: flake8-bugbear likely bugs
- **C4** - `comprehensions`: flake8-comprehensions optimization
- **SIM** - `simplifications`: flake8-simplify complex expressions
- **PIE** - `pie_issues`: flake8-pie miscellaneous rules
- **RET** - `return_issues`: flake8-return statement improvements
- **N** - `naming_issues`: pep8-naming conventions
- **S** - `security_issues`: flake8-bandit security vulnerability scanning
- **BLE** - `blind_except`: flake8-blind-except avoid bare except
- **A** - `builtins_issues`: flake8-builtins avoid shadowing built-ins
- **COM** - `comma_issues`: flake8-commas trailing comma enforcement
- **DJ** - `django_issues`: flake8-django Django-specific antipatterns
- **PT** - `pytest_issues`: flake8-pytest-style pytest best practices
- **ERA** - `commented_code`: eradicate remove commented-out code
- **T20** - `debug_prints`: flake8-print detect print statements
- **FIX** - `fixme_comments`: flake8-fixme detect TODO/FIXME comments
- **G** - `logging_issues`: flake8-logging-format logging validation
- **T10** - `debugger_issues`: flake8-debugger detect debugger usage
- **RUF** - `ruff_specific`: Ruff-specific additional checks

## Casos de uso comunes

### Desarrollo local
- **Pre-commit**: `--mode="staged"` - Verificar archivos antes de commit
- **Durante desarrollo**: `--mode="changed"` - Ver errores en archivos modificados
- **Verificación local**: `--mode="unstaged"` - Archivos locales sin staged
- **Archivos específicos**: `--files="file1.py file2.py"` - Verificar archivos exactos que estás trabajando

### CI/CD Pipeline
- **Pull Request**: `--mode="unmerged"` - Solo cambios nuevos vs rama base
- **Full audit**: `--mode="all"` - Análisis completo del proyecto
- **Release validation**: `--mode="staged"` - Verificar archivos finales

### Debug y análisis específico
- **Verbose**: `--verbose` - Ver detalles de categorización y archivos procesados
- **Carpeta específica**: `--target-folder="path"` - Análisis focalizado
- **Ruff directo**: Usar comandos ruff nativos para casos muy específicos

## Integración con otros scripts

```bash
# Workflow con modo git
# 1. Verificar errores (este script)
python scripts/run.py code_conformance --mode="changed"

# 2. Si hay errores, aplicar fixes automáticos
python scripts/run.py code_formatter --mode="changed"

# 3. Verificar que los fixes funcionaron
python scripts/run.py code_conformance --mode="changed"

# Workflow con archivos específicos
FILES="easy_pay/models.py accounts/views.py"
# 1. Verificar errores en archivos específicos
python scripts/run.py code_conformance --files="$FILES"

# 2. Si hay errores, aplicar fixes automáticos
python scripts/run.py code_formatter --files="$FILES"

# 3. Verificar que los fixes funcionaron
python scripts/run.py code_conformance --files="$FILES"
```

## Diferencias con code_formatter

| Característica | code_conformance | code_formatter |
|----------------|------------------|----------------|
| **Propósito** | Análisis read-only | Aplicar correcciones |
| **Archivos** | No modifica | Modifica archivos |
| **Exit code** | 0/1 según errores | Siempre 0 |
| **Uso CI/CD** | Validación | Fix automático |
| **Flag Ruff** | `--no-fix` | `--fix` |
| **Selección archivos** | `--mode` o `--files` | `--mode` o `--files` (misma funcionalidad) |

---

**📋 Para ver todos los estándares implementados y reglas específicas, consultar `ruff.toml`**