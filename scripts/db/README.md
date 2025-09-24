# db

**Script completo para gestión de base de datos Atlas HCL + PostgreSQL**

Maneja toda la funcionalidad de base de datos del proyecto: migraciones, seeds, tests, backups y administración completa usando Atlas HCL y PostgreSQL via Docker.

## 🎯 ¿Qué hace?

### 🔧 **Gestión de Atlas HCL**
- 📋 **Crear tablas** - Genera nuevas tablas en formato HCL
- 🚀 **Ejecutar migraciones** - Aplica cambios de schema a la base de datos
- 🌱 **Gestionar seeds** - Carga datos iniciales desde archivos HCL
- 🧪 **Ejecutar tests** - Valida integridad y funcionalidad de todas las tablas
- 📊 **Validar estructura** - Verifica consistencia entre HCL y PostgreSQL

### 🗄️ **Administración PostgreSQL**
- 🔍 **Health checks** - Verifica conectividad y estado de la base de datos
- 📈 **Métricas** - Información detallada de tablas, filas, tamaños
- 📋 **Listar contenido** - Tablas, columnas, índices, constraints
- 🔍 **Ejecutar queries** - SQL personalizado con resultados formateados
- 💾 **Backups** - Exportar e importar datos

### 🛠️ **Herramientas de Desarrollo**
- 🔄 **Migración completa** - De YAML a HCL a PostgreSQL
- 📁 **Organización modular** - Schema, catalog, relationships por separado
- 🎯 **Templates** - Generación automática de estructuras estándar
- 📊 **Reportes** - Estado completo de la base de datos

## 🚀 Flags disponibles

### **Gestión de Atlas HCL**
- `--action="migrate|seed|test|validate|create-table|backup"` - Acción principal a ejecutar
- `--table="table_name"` - Tabla específica para operaciones
- `--type="schema|catalog|relationship"` - Tipo de tabla para crear
- `--template="basic|catalog|relationship"` - Template para nueva tabla
- `--data-file="path/to/data.yaml"` - Archivo de datos para seeds
- `--force` - Forzar operación aunque existan conflictos

### **Conexión y Configuración**
- `--container="portfolio-db"` - Contenedor Docker PostgreSQL (default: portfolio-db)
- `--database="portfolio_local"` - Base de datos PostgreSQL (default: portfolio_local)
- `--user="postgres"` - Usuario PostgreSQL (default: postgres)
- `--atlas-dir="db/atlas"` - Directorio Atlas HCL (default: db/atlas)

### **Testing y Validación**
- `--test-type="basic|full|integration|performance"` - Tipo de tests a ejecutar
- `--validate-fk` - Validar foreign keys y relaciones
- `--check-data` - Verificar integridad de datos
- `--performance-test` - Ejecutar pruebas de rendimiento

### **Administración PostgreSQL (heredado de test)**
- `--endpoint="health|info|tables|query|metrics"` - Endpoint específico para admin
- `--query="SQL"` - Query SQL personalizada
- `--timeout=30` - Timeout en segundos (default: 30)
- `--verbose` - Mostrar información detallada
- `--format="table|json|csv"` - Formato de salida (default: table)

## 📋 Comandos principales

### **🚀 Migraciones Atlas**

```bash
# Migración completa (HCL → PostgreSQL)
python scripts/run.py db --action="migrate"

# Migrar solo schema principal
python scripts/run.py db --action="migrate" --type="schema"

# Migrar tabla específica
python scripts/run.py db --action="migrate" --table="users" --verbose

# Forzar migración aunque existan conflictos
python scripts/run.py db --action="migrate" --force
```

### **🌱 Seeds (Datos iniciales)**

```bash
# Ejecutar todos los seeds
python scripts/run.py db --action="seed"

# Seeds de tabla específica
python scripts/run.py db --action="seed" --table="users"

# Seeds desde archivo personalizado
python scripts/run.py db --action="seed" --data-file="custom-data.yaml"

# Seeds solo de catálogo
python scripts/run.py db --action="seed" --type="catalog" --verbose
```

### **🧪 Tests y Validación**

```bash
# Tests completos de todas las tablas
python scripts/run.py db --action="test"

# Tests básicos (existencia y estructura)
python scripts/run.py db --action="test" --test-type="basic"

# Tests de integridad y foreign keys
python scripts/run.py db --action="test" --test-type="integration" --validate-fk

# Tests de performance
python scripts/run.py db --action="test" --test-type="performance" --verbose

# Validar tabla específica
python scripts/run.py db --action="test" --table="users" --check-data
```

### **📋 Crear Nuevas Tablas**

```bash
# Crear tabla de schema principal
python scripts/run.py db --action="create-table" --table="new_table" --type="schema"

# Crear tabla de catálogo
python scripts/run.py db --action="create-table" --table="categories" --type="catalog" --template="catalog"

# Crear tabla de relación
python scripts/run.py db --action="create-table" --table="user_roles" --type="relationship" --template="relationship"

# Crear con template personalizado
python scripts/run.py db --action="create-table" --table="custom" --template="basic" --verbose
```

### **🔍 Validación y Diagnóstico**

```bash
# Validar estructura completa
python scripts/run.py db --action="validate"

# Validar consistencia HCL vs PostgreSQL
python scripts/run.py db --action="validate" --verbose

# Validar foreign keys y relaciones
python scripts/run.py db --action="validate" --validate-fk

# Diagnóstico completo con métricas
python scripts/run.py db --action="validate" --format="json" --verbose
```

### **💾 Backup y Restauración**

```bash
# Backup completo de la base de datos
python scripts/run.py db --action="backup"

# Backup de tabla específica
python scripts/run.py db --action="backup" --table="users" --verbose

# Backup con formato específico
python scripts/run.py db --action="backup" --format="json" --verbose

# Exportar estructura Atlas HCL
python scripts/run.py db --action="backup" --type="hcl-export"
```

## 🔧 Administración PostgreSQL (Comandos heredados)

### **Health Checks y Conectividad**

```bash
# Health check completo
python scripts/run.py db --endpoint="health" --verbose

# Información detallada de la base de datos
python scripts/run.py db --endpoint="info"

# Métricas de performance
python scripts/run.py db --endpoint="metrics" --verbose
```

### **Exploración de Datos**

```bash
# Listar todas las tablas
python scripts/run.py db --endpoint="tables"

# Listar tablas con detalles
python scripts/run.py db --endpoint="tables" --verbose --format="table"

# Query personalizada
python scripts/run.py db --endpoint="query" --query="SELECT version();"

# Query con formato específico
python scripts/run.py db --endpoint="query" --query="SELECT * FROM users LIMIT 5;" --format="json"
```

### **Testing de Conectividad**

```bash
# Suite completa de tests de conectividad
python scripts/run.py db --endpoint="test-all" --verbose

# Test con timeout personalizado
python scripts/run.py db --endpoint="test-all" --timeout=60
```

## 🎯 Casos de uso comunes

### **🚀 Desarrollo de Nuevas Features**

```bash
# 1. Crear nueva tabla
python scripts/run.py db --action="create-table" --table="notifications" --type="schema"

# 2. Ejecutar migración
python scripts/run.py db --action="migrate" --table="notifications"

# 3. Agregar seeds de prueba
python scripts/run.py db --action="seed" --table="notifications"

# 4. Validar funcionamiento
python scripts/run.py db --action="test" --table="notifications" --verbose
```

### **🔧 Mantenimiento y Diagnóstico**

```bash
# Diagnóstico completo del sistema
python scripts/run.py db --action="validate" --verbose

# Verificar performance de todas las tablas
python scripts/run.py db --action="test" --test-type="performance"

# Backup de seguridad antes de cambios
python scripts/run.py db --action="backup" --verbose

# Health check después de cambios
python scripts/run.py db --endpoint="health" --verbose
```

### **📊 Análisis de Datos**

```bash
# Métricas detalladas de todas las tablas
python scripts/run.py db --endpoint="metrics" --format="json" --verbose

# Análisis de tabla específica
python scripts/run.py db --endpoint="query" --query="
SELECT
  table_name,
  (xpath('//text()', query_to_xml(format('SELECT COUNT(*) FROM %I', table_name), false, true, '')))[1]::text::int as row_count,
  pg_size_pretty(pg_total_relation_size('\"' || table_name || '\"')) as size
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;" --format="table"

# Validación de integridad de datos
python scripts/run.py db --action="test" --test-type="integration" --check-data --verbose
```

### **🏗️ Migración de Estructura**

```bash
# Migración completa desde cero
python scripts/run.py db --action="migrate" --force --verbose

# Recrear solo el catálogo
python scripts/run.py db --action="migrate" --type="catalog" --force

# Validar después de migración
python scripts/run.py db --action="validate" --validate-fk --verbose

# Tests completos post-migración
python scripts/run.py db --action="test" --test-type="full" --verbose
```

## 📁 Estructura de Archivos Atlas

### **Organización Modular Generada**

```
db/atlas/
├── schema/              # Tablas principales del negocio
│   ├── users.hcl           # ✅ Usuario principal
│   ├── employers.hcl       # ✅ Empleadores
│   ├── projects.hcl        # ✅ Portfolio proyectos
│   ├── skills.hcl          # ✅ Habilidades técnicas
│   ├── works.hcl           # ✅ Experiencia laboral
│   ├── users_attributes.hcl # ✅ Atributos usuarios
│   ├── attributes_types.hcl # ✅ Tipos de atributos
│   └── job_types.hcl       # ✅ Tipos de trabajo
├── catalog/             # Tablas de catálogo/referencia
│   ├── languages.hcl       # ✅ Idiomas (ES/EN)
│   ├── networks.hcl        # ✅ Redes sociales
│   ├── interests.hcl       # ✅ Intereses profesionales
│   ├── keywords.hcl        # ✅ Palabras clave
│   ├── institutions.hcl    # ✅ Instituciones educativas
│   ├── issuers.hcl         # ✅ Emisores certificados
│   ├── publishers.hcl      # ✅ Editores/Publicadores
│   ├── awards.hcl          # 📝 Premios y reconocimientos
│   ├── certificates.hcl    # 📝 Certificaciones
│   ├── educations.hcl      # 📝 Educación formal
│   ├── publications.hcl    # 📝 Publicaciones
│   └── references.hcl      # 📝 Referencias profesionales
├── relationships/       # Tablas de relación (Many-to-Many)
│   ├── users_interests.hcl     # 📝 Usuario → Intereses
│   ├── languages_users.hcl     # 📝 Usuario → Idiomas
│   ├── networks_users.hcl      # 📝 Usuario → Redes sociales
│   ├── project_urls.hcl        # 📝 Proyectos → URLs
│   ├── skills_keywords.hcl     # 📝 Habilidades → Palabras clave
│   ├── interests_keywords.hcl  # 📝 Intereses → Palabras clave
│   ├── works_soft_skills.hcl   # 📝 Trabajos → Habilidades blandas
│   └── works_technical_skills.hcl # 📝 Trabajos → Habilidades técnicas
├── seeds/               # Datos iniciales (33 archivos)
│   ├── users.hcl           # ✅ Con datos reales
│   ├── employers.hcl       # ✅ Con datos reales
│   ├── languages.hcl       # ✅ Con datos reales
│   ├── [tabla].hcl         # 📝 Estructura preparada
│   └── all_seeds.hcl       # 🎯 Ejecutor maestro
├── tests/               # Tests de validación (34 archivos)
│   ├── users_test.hcl      # ✅ Tests funcionales
│   ├── [tabla]_test.hcl    # 📋 Tests por tabla
│   └── all_tests.hcl       # 🎯 Ejecutor maestro tests
└── templates/           # 📋 Templates para nuevas tablas
    ├── schema_template.hcl     # Template tabla schema
    ├── catalog_template.hcl    # Template tabla catálogo
    └── relationship_template.hcl # Template tabla relación
```

### **Estado Actual: 15 tablas operativas ✅**

```
📊 TABLAS EN PRODUCCIÓN:
  ├── attributes_types    (0 filas)  - Tipos de atributos
  ├── employers          (1 filas)  - Empleadores ✅ CON DATOS
  ├── institutions       (2 filas)  - Instituciones ✅ CON DATOS
  ├── interests          (3 filas)  - Intereses ✅ CON DATOS
  ├── issuers            (3 filas)  - Emisores ✅ CON DATOS
  ├── job_types          (0 filas)  - Tipos de trabajo
  ├── keywords           (3 filas)  - Palabras clave ✅ CON DATOS
  ├── languages          (2 filas)  - Idiomas ✅ CON DATOS
  ├── networks           (3 filas)  - Redes sociales ✅ CON DATOS
  ├── projects           (0 filas)  - Portfolio proyectos
  ├── publishers         (3 filas)  - Editores ✅ CON DATOS
  ├── skills             (3 filas)  - Habilidades ✅ CON DATOS
  ├── users              (1 filas)  - Usuario ✅ CON DATOS
  ├── users_attributes   (2 filas)  - Atributos usuario ✅ CON DATOS
  └── works              (0 filas)  - Experiencia laboral

📈 TOTAL: 26 filas reales + 15 tablas operativas
```

## 🔧 Configuración

### **Variables de Entorno**

```bash
# PostgreSQL Docker
DB_CONTAINER=portfolio-db
DB_DATABASE=portfolio_local
DB_USER=postgres

# Atlas HCL
ATLAS_DIR=db/atlas
ATLAS_CONFIG=db/atlas/atlas.hcl

# Configuración de conexión
DB_TIMEOUT=30
DB_MAX_RETRIES=3
```

### **Archivos de Configuración**

- `db/atlas/atlas.hcl` - Configuración principal Atlas
- `scripts/db/templates/` - Templates para nuevas tablas
- `scripts/db/config.py` - Configuración del script
- `.env.local` - Variables de entorno de desarrollo

## 🧪 Testing y QA

### **Tipos de Tests Disponibles**

1. **Basic Tests**: Existencia de tablas y estructura
2. **Integration Tests**: Foreign keys y relaciones
3. **Performance Tests**: Velocidad de consultas
4. **Data Integrity Tests**: Validación de datos
5. **Full Tests**: Suite completa de validación

### **Métricas de Calidad**

- ✅ **15/15 tablas creadas y operativas**
- ✅ **26 registros con datos reales**
- ✅ **100% tests básicos pasando**
- ✅ **Foreign keys validadas y funcionando**
- ✅ **Estructura HCL → PostgreSQL consistente**

## 📚 Referencias y Ejemplos

### **Templates Disponibles**

- **Schema Template**: Para tablas principales de negocio
- **Catalog Template**: Para tablas de referencia/catálogo
- **Relationship Template**: Para tablas Many-to-Many

### **Comandos de Diagnóstico**

```bash
# Estado completo del sistema
python scripts/run.py db --action="validate" --verbose --format="json"

# Reporte de tablas con datos
python scripts/run.py db --endpoint="metrics" --verbose

# Test completo de integridad
python scripts/run.py db --action="test" --test-type="full" --validate-fk
```

---

**Script db**: Gestión completa de Atlas HCL + PostgreSQL
**Arquitectura**: Modular, escalable, con tests integrados
**Estado**: 15 tablas operativas, 26 registros, 100% funcional
**Comandos**: 50+ operaciones disponibles para desarrollo y producción