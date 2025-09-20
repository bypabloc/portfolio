# Configuración de Linters y Formatters - 2025

Este proyecto utiliza las **mejores prácticas de 2025** para linting y formateo de código multi-lenguaje. Todos los archivos de configuración están ubicados en el directorio raíz del proyecto.

## 📁 Archivos de Configuración

### Principales (Directorio Raíz)

| Archivo | Herramienta | Lenguajes | Descripción |
|---------|-------------|-----------|-------------|
| `eslint.config.js` | ESLint (Flat Config) | JS, TS, Vue, React, Astro | **Nuevo formato estándar 2025** - Reemplaza `.eslintrc.*` |
| `.prettierrc` | Prettier | Todos los soportados | Formateo universal con soporte Astro |
| `.prettierignore` | Prettier | - | Archivos a excluir del formateo |
| `.stylelintrc.json` | Stylelint | CSS, SCSS | Linting específico para estilos |
| `.markdownlint.json` | markdownlint | Markdown | Reglas para documentación |
| `.yamllint.yml` | yamllint | YAML | Configuración YAML y archivos CI/CD |
| `ruff.toml` | Ruff | Python | **Existente** - Linting y formateo Python |

## 🚀 Características 2025

### ESLint Flat Config
- **Formato moderno**: `eslint.config.js` con export de array
- **TypeScript nativo**: Soporte completo para TS 5.3+
- **Astro integration**: Plugin oficial con reglas específicas
- **Vue 3**: Composition API y script setup
- **React**: Soporte para JSX moderno sin React import
- **Accessibility**: Reglas a11y integradas

### Prettier Avanzado
- **Plugin Astro**: Formateo nativo de archivos `.astro`
- **100 caracteres**: Line length modernizada
- **Trailing commas**: `"all"` para mejor Git diffs
- **Single quotes**: Consistencia en todo el proyecto
- **Overrides**: Configuración específica por tipo de archivo

### Stylelint Moderno
- **SCSS Standard**: `stylelint-config-standard-scss` únicamente
- **Nesting limits**: Max 4 niveles de anidamiento
- **Naming patterns**: camelCase para variables y mixins
- **Performance**: Selectores optimizados

## 🔧 Herramientas por Lenguaje

### JavaScript/TypeScript
```bash
# Linting
npx eslint . --ext .js,.ts,.tsx,.jsx
# Formateo
npx prettier --write "**/*.{js,ts,tsx,jsx}"
```

### Astro
```bash
# Linting (con ESLint + plugin Astro)
npx eslint . --ext .astro
# Formateo (con Prettier + plugin Astro)
npx prettier --write "**/*.astro"
```

### Vue.js
```bash
# Linting
npx eslint . --ext .vue
# Formateo
npx prettier --write "**/*.vue"
```

### CSS/SCSS
```bash
# Linting
npx stylelint "**/*.{css,scss}"
# Formateo
npx prettier --write "**/*.{css,scss}"
```

### Python
```bash
# Linting y formateo
ruff check . --config ruff.toml
ruff check --fix . --config ruff.toml
```

### Markdown
```bash
# Linting
npx markdownlint "**/*.md"
# Formateo
npx prettier --write "**/*.md"
```

### YAML
```bash
# Linting
yamllint .
# Formateo
npx prettier --write "**/*.{yml,yaml}"
```

## 📋 Scripts Multi-Lenguaje

El proyecto incluye scripts automatizados que utilizan estas configuraciones:

```bash
# Análisis completo (solo lectura)
python scripts/run.py code_conformance --mode="changed" --verbose

# Formateo automático (aplica fixes)
python scripts/run.py code_formatter --mode="changed" --verbose

# Solo lenguajes específicos
python scripts/run.py code_formatter --mode="staged" --languages="astro,js,ts,css"

# Astro completo
python scripts/run.py code_formatter --mode="changed" --languages="astro"
```

## 💻 Integración con Editores

### VS Code (Recomendado)
```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true,
    "source.organizeImports": true
  },
  "prettier.documentSelectors": ["**/*.astro"],
  "[astro]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[css]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

### Extensiones Requeridas
- ESLint
- Prettier - Code formatter
- Astro (oficial)
- Stylelint
- Python (con Ruff support)

## 🏗️ Instalación de Dependencias

### JavaScript/TypeScript/Astro
```bash
# ESLint y plugins
npm install -D eslint @eslint/js typescript-eslint eslint-plugin-astro eslint-plugin-vue eslint-plugin-react globals

# Prettier y plugins
npm install -D prettier prettier-plugin-astro

# Stylelint
npm install -D stylelint stylelint-config-standard-scss stylelint-scss

# Markdown y YAML
npm install -D markdownlint markdownlint-cli
```

### Python
```bash
# Ruff (ya instalado según ruff.toml)
pip install ruff

# YAML linting
pip install yamllint
```

## 📊 Beneficios del Setup 2025

### Técnicos
- **ESLint Flat Config**: Mejor performance y configuración más clara
- **Plugin Astro**: Soporte nativo para el framework moderno
- **100 char line length**: Mejor para pantallas modernas
- **Trailing commas**: Git diffs más limpios
- **TypeScript strict**: Zero-tolerance para errores de tipos

### Desarrollo
- **Auto-fix**: La mayoría de errores se corrigen automáticamente
- **Multi-lenguaje**: Un solo comando para todo el proyecto
- **Eficiencia**: Solo formatea archivos con errores reales
- **Consistencia**: Mismas reglas en todo el equipo

### Mantenimiento
- **Configuración centralizada**: Todo en directorio raíz
- **Versionado**: Configuraciones incluidas en Git
- **Escalabilidad**: Fácil agregar nuevos lenguajes
- **Compatibilidad**: Funciona con todas las herramientas modernas

---

**Fecha de creación**: 2025-01-19
**Estándares**: ESLint Flat Config, Prettier 3.x, Stylelint 16.x, Ruff 0.6.x
**Compatibilidad**: Node.js 20+, Python 3.12+, VS Code 1.85+