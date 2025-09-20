# Scripts - Sistema de Automatización de Tareas

Este directorio contiene un sistema de scripts modular y extensible diseñado para automatizar diversas tareas del proyecto.

## 🏗️ Arquitectura del Sistema

El sistema está diseñado con una arquitectura modular que permite agregar nuevos scripts de forma sencilla y consistente con manejo centralizado de flags y sistema de ayuda integrado.

### Estructura General
```
scripts/
├── README.md                      # Este archivo
├── run.py                         # Ejecutor principal del sistema
├── utils/                         # Utilidades compartidas
│   ├── __init__.py
│   └── flags_to_dict.py          # Conversor de flags a diccionarios
└── <nombre_script>/               # Cada script tiene su propia carpeta
    ├── __init__.py
    ├── main.py                   # Lógica principal del script
    └── flags.py                  # Validación de flags y documentación
```

### Características Principales
- **Manejo centralizado de flags**: `run.py` convierte todas las flags a diccionario automáticamente
- **Sistema de ayuda integrado**: Ayuda global y específica por script
- **Descubrimiento dinámico**: Detecta automáticamente scripts válidos
- **Validación robusta**: Control de errores y mensajes informativos

## 🚀 Uso General

### Sistema de Ayuda
```bash
# Ayuda global - muestra todos los scripts disponibles
python scripts/run.py --help

# Ayuda específica de un script
python scripts/run.py <nombre_script> --help
```

### Comando Base
```bash
python scripts/run.py <nombre_script> [flags...]
```

### Ejemplos
```bash
# Ver ayuda global
python scripts/run.py --help

# Ver ayuda específica
python scripts/run.py <script_name> --help

# Ejecutar script con flags
python scripts/run.py <script_name> --flag1 --flag2="valor"

# Combinando múltiples flags
python scripts/run.py <script_name> --flag1 --flag2="a|b|c" --flag3
```

## 📋 Scripts Disponibles

Para ver todos los scripts disponibles usa:
```bash
python scripts/run.py --help
```

Cada script tiene su propia documentación:
```bash
python scripts/run.py <nombre_script> --help
```

## 🔧 Componentes del Sistema

### 1. Ejecutor Principal (`run.py`)
El archivo `run.py` es el punto de entrada único para todos los scripts. Se encarga de:
- **Manejo centralizado de flags**: Convierte automáticamente todas las flags a diccionario
- **Sistema de ayuda integrado**: Maneja `--help` global y específico por script
- **Descubrimiento dinámico de scripts**: Detecta automáticamente scripts válidos
- **Validación de estructura**: Verifica que existan `main.py` y `flags.py`
- **Carga dinámica de módulos**: Importa y ejecuta scripts dinámicamente
- **Manejo robusto de errores**: Mensajes informativos y manejo de excepciones

**Nuevas Características v2.0**:
- **Conversión de flags centralizada**: Ya no se pasa lista a `flags.py`, se pasa diccionario procesado
- **Sistema de ayuda con descubrimiento**: `--help` muestra automáticamente todos los scripts válidos
- **Separación de responsabilidades**: El argumento `<script>` no se pasa a `flags.py`
- **Validación automática de documentación**: Verifica que cada script tenga método `help()`

### 2. Utilidades (`utils/`)
Contiene funciones compartidas que pueden ser utilizadas por todos los scripts.

#### `flags_to_dict.py`
Convierte argumentos de línea de comandos a diccionarios de Python con las siguientes características:
- Maneja flags booleanas (`--flag`)
- Maneja flags con valores (`--flag=valor`)
- Convierte strings separados por `|` a listas
- Validación de flags permitidas y requeridas
- Establecimiento de valores por defecto

**Funciones principales**:
- `flags_to_dict(args_list)`: Conversión principal
- `validate_required_flags(flags_dict, required_flags)`: Validación de flags requeridas
- `validate_allowed_flags(flags_dict, allowed_flags)`: Validación de flags permitidas
- `set_default_values(flags_dict, defaults)`: Establecer valores por defecto

### 3. Estructura de Scripts Individuales

Cada script debe seguir esta estructura obligatoria:

#### `main.py`
```python
def main(flags):
    """
    Función principal del script.
    
    Args:
        flags (dict): Diccionario con las flags procesadas y validadas
    """
    # Lógica principal del script
    pass
```

#### `flags.py` (Interfaz v3.0)
```python
def flag(flags_dict):
    """
    Procesa y valida las flags del script.
    
    Args:
        flags_dict (dict): Diccionario de flags ya procesado por run.py
        
    Returns:
        dict: Diccionario con las flags validadas y valores por defecto aplicados
    """
    # Validación y procesamiento específico del script
    pass
```

#### `README.md` (Nuevo en v3.0)
```markdown
# nombre_script

Descripción detallada de qué hace el script.

## Flags disponibles

- `--flag1` - Descripción de flag1 (boolean)
- `--flag2="valor"` - Descripción de flag2 (string)
- `--flag3="a|b|c"` - Lista separada por | (array)

## Ejemplos de uso

### Básico
\`\`\`bash
python scripts/run.py nombre_script --flag1
\`\`\`

### Con valores
\`\`\`bash  
python scripts/run.py nombre_script --flag2="valor"
python scripts/run.py nombre_script --flag3="opcion1|opcion2"
\`\`\`

## Casos de uso comunes

- Caso 1: descripción
- Caso 2: descripción
```

**🔄 Cambios en v3.0**:
- **README.md obligatorio**: Cada script debe tener documentación en Markdown
- **Sin función `help()`**: La documentación se lee desde README.md
- **Validación de contenido**: README.md debe tener contenido para ser válido
- **Mejor formato**: Documentación más rica con Markdown

## 📖 Guía para Desarrolladores

### Crear un Nuevo Script (v2.0)

El sistema soporta diferentes tipos de flags que se convierten automáticamente:

#### Tipos de Flags Soportados

| Tipo | Formato | Ejemplo | Resultado en Python |
|------|---------|---------|---------------------|
| **Boolean** | `--flag` | `--verbose` | `{'verbose': True}` |
| **String** | `--flag="valor"` | `--name="Juan"` | `{'name': 'Juan'}` |
| **Array/Lista** | `--flag="a\|b\|c"` | `--extensions="py\|js\|css"` | `{'extensions': ['py', 'js', 'css']}` |

#### Conversiones Automáticas
- **Guiones a underscore**: `--my-flag` → `my_flag` en Python
- **Separador de listas**: `"a|b|c"` → `['a', 'b', 'c']`
- **Manejo de comillas**: Automáticamente removidas
- **Valores booleanos**: Presencia = `True`, ausencia = `False`

### Paso a Paso: Crear un Nuevo Script (v3.0)

1. **Crear la estructura de carpetas**:
```bash
mkdir scripts/<nombre_script>
touch scripts/<nombre_script>/__init__.py
```

2. **Crear `README.md` con documentación**:
```markdown
# <nombre_script>

[Descripción del script]

## Flags disponibles

- `--flag1` - Descripción (boolean)
- `--flag2="valor"` - Descripción (string)

## Ejemplos de uso

\`\`\`bash
python scripts/run.py <nombre_script> --flag1
\`\`\`

## Casos de uso comunes

- Caso 1: descripción
```

3. **Crear `flags.py` con nueva interfaz**:
```python
import sys
import os

# Añadir utils al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.flags_to_dict import validate_allowed_flags, set_default_values

def help():
    """Documentación de ayuda para el script."""
    return """
Script: <nombre_script>
Descripción: [Descripción detallada de qué hace el script]

Flags disponibles:
  --verbose                    Mostrar información detallada (boolean)
  --output-format="json|xml"   Formato de salida (lista)
  --config-file="path"         Archivo de configuración (string)
  --dry-run                    Simular sin ejecutar (boolean)

Ejemplos de uso:
  python scripts/run.py <nombre_script> --verbose
  python scripts/run.py <nombre_script> --output-format="json|csv" 
  python scripts/run.py <nombre_script> --config-file="config.yaml" --dry-run

Casos de uso comunes:
  - Ejecución básica: sin flags
  - Con configuración: --config-file="archivo"
  - Modo verbose: --verbose para debug
    """

def flag(flags_dict):
    """
    Procesa y valida las flags del script.
    
    Args:
        flags_dict (dict): Diccionario de flags ya procesado por run.py
        
    Returns:
        dict: Diccionario validado con valores por defecto
    """
    # Definir flags permitidas (incluir 'help' siempre)
    allowed_flags = [
        'verbose',           # Boolean flag
        'output_format',     # Lista separada por |
        'config_file',       # String con path
        'dry_run',           # Boolean flag  
        'help'               # Siempre incluir help
    ]
    
    # Definir valores por defecto con tipos apropiados
    defaults = {
        'verbose': False,           # Boolean por defecto
        'output_format': [],        # Lista vacía por defecto
        'config_file': '',          # String vacío por defecto
        'dry_run': False            # Boolean por defecto
    }
    
    # Validar flags permitidas
    validate_allowed_flags(flags_dict, allowed_flags)
    
    # Aplicar valores por defecto
    flags_dict = set_default_values(flags_dict, defaults)
    
    # Procesamiento específico de listas separadas por |
    if 'output_format' in flags_dict and isinstance(flags_dict['output_format'], str):
        flags_dict['output_format'] = flags_dict['output_format'].split('|')
    
    # Mostrar flags procesadas para debug (opcional)
    print("Flags procesadas:")
    for flag_name, flag_value in flags_dict.items():
        if flag_value and flag_name != 'help':
            display_name = flag_name.replace('_', '-')
            if isinstance(flag_value, list):
                print(f"  --{display_name}: {', '.join(flag_value)}")
            else:
                print(f"  --{display_name}: {flag_value}")
    
    return flags_dict
```

3. **Crear `main.py`**:
```python
def main(flags):
    """
    Lógica principal del script.
    
    Args:
        flags (dict): Diccionario con las flags procesadas y validadas
    """
    # Manejo de diferentes tipos de flags
    
    # 1. Boolean flags
    if flags.get('verbose'):
        print("Modo verbose activado - mostrando información detallada")
        
    if flags.get('dry_run'):
        print("Modo dry-run - simulando sin ejecutar")
    
    # 2. String flags
    config_file = flags.get('config_file')
    if config_file:
        print(f"Cargando configuración desde: {config_file}")
        # Lógica para cargar archivo
    
    # 3. Lista/Array flags
    output_formats = flags.get('output_format', [])
    if output_formats:
        print(f"Formatos de salida: {', '.join(output_formats)}")
        for format_type in output_formats:
            print(f"Procesando formato: {format_type}")
    
    # 4. Lógica principal del script
    print("Ejecutando lógica principal...")
    
    # Ejemplo de procesamiento con diferentes flags
    result = process_data(
        verbose=flags.get('verbose', False),
        dry_run=flags.get('dry_run', False),
        config=config_file
    )
    
    # Generar salida según formatos solicitados
    if output_formats:
        for fmt in output_formats:
            generate_output(result, fmt)
    else:
        # Salida por defecto
        print(result)

def process_data(verbose=False, dry_run=False, config=None):
    """Lógica de procesamiento del script."""
    if verbose:
        print("Procesando datos...")
    
    if dry_run:
        print("Simulando procesamiento...")
        return {"status": "simulated"}
    
    # Lógica real aquí
    return {"status": "processed", "count": 42}

def generate_output(data, format_type):
    """Generar salida en diferentes formatos."""
    if format_type == 'json':
        import json
        print(json.dumps(data, indent=2))
    elif format_type == 'csv':
        print("CSV output:", data)
    else:
        print(f"Formato {format_type} no soportado")
```

4. **Probar el script**:
```bash
# Ver ayuda del script  
python scripts/run.py <nombre_script> --help

# Ejecutar con diferentes tipos de flags
python scripts/run.py <nombre_script> --verbose
python scripts/run.py <nombre_script> --config-file="settings.yaml" 
python scripts/run.py <nombre_script> --output-format="json|csv"
python scripts/run.py <nombre_script> --verbose --dry-run --output-format="json"
```

### Mejores Prácticas (v3.0)

#### Manejo de Flags
- **Incluir siempre 'help'**: En la lista de `allowed_flags` para compatibilidad
- **Nombres descriptivos**: Usar snake_case para flags internas
- **Valores por defecto sensatos**: Definir defaults apropiados para cada flag
- **Validación específica**: Procesar listas separadas por `|` si es necesario
- **Información de procesamiento**: Mostrar flags activas para debug

#### Documentación Obligatoria  
- **README.md requerido**: Cada script debe tener documentación en Markdown
- **Formato estándar**: Usar el formato mostrado en el ejemplo
- **Ejemplos completos**: Incluir casos de uso comunes y ejemplos prácticos
- **Descripción clara**: Explicar qué hace el script y cuándo usarlo
- **Contenido no vacío**: README.md debe tener contenido para ser válido

#### Estructura de Código
- **Separación de responsabilidades**: `flags.py` solo para validación, `main.py` para lógica
- **Manejo robusto**: Usar try/catch apropiadamente
- **Logging consistente**: Usar print() para información de debug
- **Convenciones de nomenclatura**: Seguir estándares del proyecto

#### Compatibilidad
- **Interfaz v3.0**: Siempre recibir dict en `flag()`, nunca lista  
- **Estructura obligatoria**: main.py + flags.py + README.md
- **Validación automática**: El sistema verifica README.md con contenido
- **Testing**: Probar tanto ayuda como funcionalidad

## 🔍 Validación y Errores

### Errores Comunes y Soluciones

1. **"La carpeta 'X' no existe en scripts/"**
   - **Causa**: Nombre de script incorrecto o no existe
   - **Solución**: Verificar que existe `scripts/<nombre>/`

2. **"No se encontró 'main.py' en scripts/X/"**
   - **Causa**: Falta el archivo `main.py`
   - **Solución**: Crear `main.py` con función `main(flags)`

3. **"No se encontró 'flags.py' en scripts/X/"**
   - **Causa**: Falta el archivo `flags.py`
   - **Solución**: Crear `flags.py` con función `flag(flags_dict)`

4. **"No se encontró 'README.md' en scripts/X/"**
   - **Causa**: Falta el archivo `README.md`
   - **Solución**: Crear `README.md` con documentación del script

5. **"README.md está vacío en scripts/X/"**
   - **Causa**: README.md existe pero no tiene contenido
   - **Solución**: Agregar documentación al README.md

6. **"No se encontró la función 'flag' en flags.py"**
   - **Causa**: La función `flag` no está definida
   - **Solución**: Implementar `def flag(flags_dict):`

7. **"Flags no permitidas: X"**
   - **Causa**: Se usó una flag no definida en `allowed_flags`
   - **Solución**: Agregar la flag a la lista de permitidas

## 🛠️ Mantenimiento

### Agregar Nuevas Utilidades
Las utilidades compartidas van en `scripts/utils/`. Para agregar una nueva:

1. Crear el archivo en `utils/`
2. Documentar su uso
3. Importar en scripts que la necesiten
4. Actualizar este README

### Actualizar Scripts Existentes
1. Mantener compatibilidad con flags existentes
2. Agregar nuevas flags de forma opcional
3. Documentar cambios
4. Probar funcionamiento

### Versionado
- Mantener compatibilidad hacia atrás
- Documentar cambios breaking
- Usar semantic versioning para cambios mayores

## 📚 Referencias

### Dependencias
- **GitPython**: Para operaciones con repositorio git
- **Python 3.8+**: Versión mínima requerida
- **pathlib**: Para manejo de rutas

### Instalación de Dependencias para Scripts

Para usar los scripts del sistema, especialmente aquellos relacionados con formateo y calidad de código, instala las dependencias adicionales:

```bash
# Instalar dependencias específicas para scripts de formateo/calidad
pip install -r requirements_formatter.txt
```

**Nota**: El archivo `requirements_formatter.txt` contiene las dependencias necesarias para:
- Scripts de formateo de código
- Herramientas de análisis de calidad
- Utilidades de Git para procesamiento de archivos

### Patrones Utilizados
- **Factory Pattern**: Para carga dinámica de scripts
- **Command Pattern**: Para ejecución de comandos
- **Strategy Pattern**: Para procesamiento de flags

## 🤝 Contribución

Para contribuir al sistema de scripts:

1. Seguir la estructura establecida
2. Documentar nuevos scripts
3. Agregar tests si es aplicable
4. Actualizar este README
5. Seguir las convenciones de código del proyecto

## 📝 Changelog

### v3.0.0 (2025-01-04) - **Documentación con Markdown**
- **📄 README.md obligatorio**: Cada script debe tener documentación en Markdown
- **🚫 Sin función `help()`**: Eliminada en favor de README.md
- **✅ Validación de contenido**: README.md debe tener contenido para ser script válido
- **📚 Mejor documentación**: Formato Markdown más rico y mantenible
- **🔍 Descubrimiento mejorado**: Solo scripts con README.md válido se consideran

**Breaking Changes v3.0**:
- **ELIMINADO**: Función `help()` en `flags.py` 
- **REQUERIDO**: Archivo `README.md` con contenido en cada script
- **CAMBIADO**: Sistema de ayuda lee desde archivos `.md`

### v2.0.0 (2025-01-04) - **Refactorización Mayor**
- **🚀 Manejo centralizado de flags**: `run.py` convierte flags a dict automáticamente
- **📚 Sistema de ayuda integrado**: `--help` global y específico por script
- **🔍 Descubrimiento automático**: Detecta scripts válidos dinámicamente
- **📖 Documentación obligatoria**: Función `help()` requerida en cada script
- **🔄 Nueva interfaz**: `flag()` recibe dict en lugar de lista
- **⚡ Separación de responsabilidades**: Argumento `<script>` no se pasa a `flags.py`
- **🛠️ Validación mejorada**: Control robusto de errores y mensajes informativos
- **✅ Corrección de linting**: Eliminación de bare `except`

### v1.0.0 (2025-01-04)
- Sistema inicial de scripts modulares
- Implementación de `structure_folder_n_files`
- Utilidades base para manejo de flags
- Documentación completa
- Validación robusta de errores

---

**Nota**: Este sistema v3.0 usa documentación en Markdown para mayor mantenibilidad. Todos los scripts deben tener un `README.md` con contenido para ser válidos.