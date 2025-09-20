# code_formatter

**Script de formateo automático multi-lenguaje integrado con code_conformance**

Aplica correcciones automáticas usando herramientas especializadas **solo a archivos que tienen errores**, usando `code_conformance` para identificar qué archivos necesitan formateo.

⚡ **Estrategia eficiente**: En lugar de formatear todos los archivos, solo formatea los que realmente tienen violaciones detectadas por las herramientas de análisis.

## ¿Cómo funciona?

1. 🔍 **Ejecuta `code_conformance`** con output JSON para identificar archivos con errores
2. 📋 **Extrae lista de archivos** que tienen violaciones por lenguaje
3. 🔧 **Aplica herramientas de formateo** específicas solo a esos archivos
4. ✅ **Reporta cambios aplicados** con detalles de las correcciones por lenguaje

## Herramientas de Formateo por Lenguaje (2025)

### **Python - Ruff (`ruff --fix`)**:
- **Estilo**: Trailing whitespace, espaciado, líneas en blanco
- **Imports**: Reorganización automática con isort
- **Modernización**: Conversión a f-strings, sintaxis Python 3.12+
- **Trailing commas**: Agrega automáticamente en dicts, listas, argumentos
- **Simplificaciones**: Expresiones booleanas, optimizaciones de comprehensions
- **Config**: `ruff.toml` en directorio raíz

### **JavaScript/TypeScript - ESLint Flat Config + Prettier**:
- **Formateo**: Indentación, quotes, semicolons, line length (100 chars)
- **Import sorting**: Organización automática de imports
- **TypeScript**: Strict mode obligatorio, fixing de tipos básicos
- **Modern features**: ES2025 features, async/await patterns
- **Config**: `eslint.config.js` (flat config) + `.prettierrc` en directorio raíz

### **Astro - ESLint + Prettier + Plugin Astro**:
- **Frontmatter**: Análisis TypeScript en frontmatter
- **Template**: JSX-like syntax linting y formateo
- **Accessibility**: Reglas a11y específicas para Astro
- **Integration**: Soporte completo para Vue/React en componentes Astro
- **Config**: `eslint.config.js` con `eslint-plugin-astro` + `.prettierrc` con `prettier-plugin-astro`

### **Vue.js - ESLint + Prettier**:
- **Composition API**: Reglas específicas para setup script
- **Template**: Directivas Vue y syntax específico
- **TypeScript**: Support completo en SFC
- **Config**: `eslint.config.js` con soporte Vue + `.prettierrc`

### **CSS/SCSS - Stylelint + Prettier**:
- **Formateo**: Indentación, quotes, espaciado de selectores
- **Properties**: Ordenamiento automático de propiedades CSS
- **Valores**: Normalización de colores, unidades

### **Markdown - Prettier**:
- **Formateo**: Line length, list indentation, table formatting
- **Links**: Normalización de referencias y URLs

### **JSON/YAML - Prettier**:
- **Formateo**: Indentación consistente, quotes, trailing commas
- **Estructura**: Organización de objetos y arrays

### **HTML - Prettier**:
- **Formateo**: Indentación, attribute wrapping, void elements

## Flags disponibles

**Selección de archivos (obligatorio - elegir una):**
- `--mode="all|changed|staged|unstaged|unmerged"` - Archivos por modo git
- `--files="archivo1 archivo2"` - Archivos específicos a formatear

**Filtros de lenguaje:**
- `--languages="js,ts,py,astro"` - Lenguajes específicos a formatear (opcional)
  - **Lenguajes soportados**: `js`, `ts`, `py`, `md`, `json`, `yml`, `yaml`, `html`, `css`, `scss`, `vue`, `jsx`, `tsx`, `astro`
  - **Auto-detección**: Si no se especifica, detecta automáticamente por extensión de archivo

**Opciones adicionales:**
- `--verbose` - Mostrar información detallada del proceso (default: false)
- `--target-folder="path/to/folder"` - Formatear solo archivos de una carpeta específica
- `--project-path="/path/to/project"` - Ruta del proyecto (default: auto-detect)
- `--exclude-paths="tests,node_modules"` - Paths a excluir del formateo

⚠️ **IMPORTANTE**: Debe usar o `--mode` o `--files`, pero no ambos. Son opciones mutuamente excluyentes.

## Ejemplos de uso

### Formateo básico (multi-lenguaje)
```bash
# Auto-detecta y formatea todos los lenguajes en archivos no mergeados
python scripts/run.py code_formatter --mode="unmerged"

# Con información detallada de qué se está formateando
python scripts/run.py code_formatter --mode="changed" --verbose

# Formatear todos los archivos del proyecto que tienen errores
python scripts/run.py code_formatter --mode="all"
```

### Por lenguajes específicos
```bash
# Solo Python
python scripts/run.py code_formatter --mode="changed" --languages="py"

# JavaScript y TypeScript
python scripts/run.py code_formatter --mode="staged" --languages="js,ts"

# Solo archivos de estilo
python scripts/run.py code_formatter --mode="all" --languages="css,scss"

# Documentación
python scripts/run.py code_formatter --mode="changed" --languages="md,json,yml"

# Frontend completo
python scripts/run.py code_formatter --mode="unmerged" --languages="js,ts,vue,css,html"

# Astro completo (frontend moderno)
python scripts/run.py code_formatter --mode="changed" --languages="astro,js,ts,css"

# Solo archivos Astro
python scripts/run.py code_formatter --mode="staged" --languages="astro"
```

### Por modo de git
```bash
# Archivos no mergeados (útil para PRs)
python scripts/run.py code_formatter --mode="unmerged" --verbose

# Archivos con cambios locales
python scripts/run.py code_formatter --mode="changed" --languages="py,js"

# Archivos en staging area (pre-commit)
python scripts/run.py code_formatter --mode="staged"

# Archivos modificados pero no staged
python scripts/run.py code_formatter --mode="unstaged" --languages="js,ts,vue"
```

### Para carpetas específicas
```bash
# Formatear solo carpeta src (auto-detect lenguajes)
python scripts/run.py code_formatter --target-folder="src"

# Solo Python en carpeta de tests
python scripts/run.py code_formatter --target-folder="tests" --languages="py"

# Frontend en carpeta components
python scripts/run.py code_formatter --target-folder="src/components" --languages="vue,js,css"
```

### Para archivos específicos multi-lenguaje
```bash
# Formatear archivos específicos (auto-detect)
python scripts/run.py code_formatter --files="src/main.py src/utils.js styles.css"

# Solo Python en archivos específicos
python scripts/run.py code_formatter --files="models.py views.py" --languages="py"

# Mix de lenguajes específicos
python scripts/run.py code_formatter --files="main.js style.css README.md" --languages="js,css,md"

# Con verbose para debugging
python scripts/run.py code_formatter --files="src/app.vue src/main.ts" --verbose
```

### Output con información detallada
```bash
# Ejemplo de output verbose:
python scripts/run.py code_formatter --mode="unmerged" --verbose --target-folder="myproject/api"

# Muestra:
# 🔍 Ejecutando análisis de conformance para identificar archivos con errores...
# 📊 Encontrados 5 archivos con errores (73 violaciones totales)
# 📄 Archivos que serán formateados:
#    • myproject/api/status_payment.py (15 violaciones)
#    • myproject/api/prepare_payment.py (27 violaciones)
# 🔧 Aplicando formateo automático con Ruff a 5 archivos...
# 💻 Ejecutando: ruff check --fix archivo1.py archivo2.py...
# ✅ Formateo completado en 5 archivos
```

## Workflow recomendado (integrado)

```bash
# 1. Verificar qué archivos tienen errores
python scripts/run.py code_conformance --mode="unmerged" --verbose

# 2. Formatear automáticamente solo archivos que tienen errores  
python scripts/run.py code_formatter --mode="unmerged" --verbose

# 3. Verificar que se corrigieron los errores automáticamente
python scripts/run.py code_conformance --mode="unmerged" --verbose

# 4. Los errores restantes requieren corrección manual
```

## Diferencias con code_conformance

| Característica | code_conformance | code_formatter |
|----------------|------------------|----------------|
| **Propósito** | Análisis read-only | Aplicar correcciones |
| **Archivos** | No modifica | Modifica archivos |
| **Estrategia** | Analiza todos los archivos del modo | Solo procesa archivos que tienen errores |
| **Eficiencia** | Completo pero lento | Rápido y focalizado |
| **Exit code** | 0/1 según errores | Siempre 0 (successful formatting) |
| **Output** | JSON/console con categorías | Progress con cambios aplicados |
| **Selección archivos** | `--mode` o `--files` | `--mode` o `--files` (misma funcionalidad) |

## Casos de uso comunes

### Desarrollo local
- **Pre-commit**: `--mode="staged"` - Formatear archivos staged antes de commit
- **Durante desarrollo**: `--mode="changed"` - Formatear archivos modificados
- **Fixes rápidos**: `--target-folder="path"` - Formatear una carpeta específica
- **Archivos específicos**: `--files="file1.py file2.py"` - Formatear archivos exactos que estás trabajando

### CI/CD Pipeline  
- **Pull Request**: `--mode="unmerged"` - Formatear solo cambios nuevos vs rama base
- **Maintenance**: `--mode="all"` - Formatear todos los archivos con errores del proyecto
- **Targeted fixes**: `--target-folder="critical/path"` - Formatear área específica

### Integración eficiente
```bash
# Workflow CI/CD optimizado (modo git)
if python scripts/run.py code_conformance --mode="unmerged" > /dev/null 2>&1; then
    echo "✅ No formatting needed"
else  
    echo "🔧 Applying auto-fixes..."
    python scripts/run.py code_formatter --mode="unmerged"
    echo "✅ Auto-formatting completed"
fi

# Workflow para archivos específicos
FILES="easy_pay/models.py accounts/views.py"
if python scripts/run.py code_conformance --files="$FILES" > /dev/null 2>&1; then
    echo "✅ No formatting needed for specified files"
else
    echo "🔧 Applying auto-fixes to specific files..."
    python scripts/run.py code_formatter --files="$FILES"
    echo "✅ Auto-formatting completed for specific files"
fi
```

## Limitaciones importantes

❌ **No implementado**: 
- `--dry-run` (usa `code_conformance` para preview)
- `--module` o `--file` específico (usa `--target-folder`)
- Formateo de archivos sin errores (por diseño - eficiencia)

⚡ **Por diseño**: 
- Solo formatea archivos que tienen violaciones detectadas por Ruff
- Requiere que `code_conformance` funcione correctamente  
- Usa la misma configuración `ruff.toml` que code_conformance

## Comando Ruff equivalente

El script ejecuta internamente:
```bash  
# 1. Identificar archivos con errores
python scripts/run.py code_conformance --mode="unmerged" --output-format="json"

# 2. Extraer lista de archivos del JSON  

# 3. Aplicar fixes solo a esos archivos
ruff check --fix [archivos_con_errores...] --config ruff.toml
```

Si prefieres usar Ruff directamente:
```bash
# Formatear archivos específicos
ruff check --fix archivo1.py archivo2.py --config ruff.toml

# Formatear todo (menos eficiente)
ruff check --fix . --config ruff.toml
```

---

**🔧 Integración perfecta**: Este script funciona en tándem con `code_conformance` para un workflow de calidad de código eficiente y automatizado.