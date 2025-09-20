# Database - Neon PostgreSQL 17 Serverless

> **Fecha de creación**: Enero 2025
> **Última actualización**: Enero 2025
> **Stack**: Neon PostgreSQL 17 + Database Branching
> **Cloud Provider**: Neon.tech (Serverless PostgreSQL)

---

## 🎯 Resumen Ejecutivo de Base de Datos

Este documento proporciona la guía completa para implementar y gestionar la **base de datos PostgreSQL 17 serverless** usando **Neon.tech**, optimizada para arquitecturas modernas y serverless.

La implementación está diseñada para **máximo rendimiento en entornos serverless**, con **branching de base de datos** tipo Git y **auto-scaling automático**.

### Características Principales
- ✅ **PostgreSQL 17**: Última versión disponible con mejoras de performance
- ✅ **Serverless Auto-scaling**: Escala automáticamente según demanda
- ✅ **Database Branching**: Workflow tipo Git para diferentes entornos
- ✅ **Connection Pooling**: Optimizado para aplicaciones serverless
- ✅ **Instant Provisioning**: Creación instantánea de bases de datos y branches
- ✅ **Monitoring & Observability**: Métricas de performance y uso integradas

---

## 🏗️ Arquitectura de Base de Datos

### Stack Tecnológico
```yaml
Database Service: Neon PostgreSQL 17.x
  - Type: Serverless PostgreSQL-as-a-Service
  - Features: Auto-scaling, branching, instant provisioning
  - Regions: Multi-region support con read replicas
  - Storage: Separación de compute y storage
  - Compute: Auto-suspend durante inactividad

Branching System: Git-like Database Workflow
  - Main Branch: Producción
  - Dev Branches: Desarrollo y testing
  - Feature Branches: Nuevas características
  - Point-in-time: Recovery y snapshots

Connection Management: Neon Proxy
  - Pooling: Connection pooling automático
  - Load Balancing: Distribución de carga
  - Security: TLS encryption y autenticación
  - Compatibility: Compatible con todas las librerías PostgreSQL

Monitoring: Neon Console + Metrics
  - Performance: Query performance insights
  - Usage: Connection count, storage, compute metrics
  - Billing: Uso detallado por branch y operación
  - Alerts: Notificaciones automáticas
```

---

## 📊 Schema de Base de Datos

### Tablas Principales

#### Personal Information
```sql
-- Información personal del portfolio
CREATE TABLE personal_info (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(50),
    location VARCHAR(255),
    bio TEXT,
    linkedin_url VARCHAR(500),
    github_url VARCHAR(500),
    website_url VARCHAR(500),
    profile_image_url VARCHAR(500),
    resume_url VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Professional Experience
```sql
-- Experiencia profesional
CREATE TABLE experience (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company VARCHAR(255) NOT NULL,
    position VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    start_date DATE NOT NULL,
    end_date DATE,
    is_current BOOLEAN DEFAULT FALSE,
    description TEXT,
    achievements TEXT[],
    technologies VARCHAR(100)[],
    company_url VARCHAR(500),
    logo_url VARCHAR(500),
    order_index INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Projects Portfolio
```sql
-- Portfolio de proyectos
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    detailed_description TEXT,
    status VARCHAR(50) DEFAULT 'completed',
    start_date DATE,
    end_date DATE,
    technologies VARCHAR(100)[] NOT NULL,
    github_url VARCHAR(500),
    demo_url VARCHAR(500),
    image_url VARCHAR(500),
    images TEXT[],
    category VARCHAR(100),
    featured BOOLEAN DEFAULT FALSE,
    order_index INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Skills Matrix
```sql
-- Matriz de habilidades técnicas
CREATE TABLE skills (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL UNIQUE,
    category VARCHAR(100) NOT NULL,
    proficiency_level INTEGER CHECK (proficiency_level >= 1 AND proficiency_level <= 5),
    years_experience DECIMAL(3,1),
    description TEXT,
    icon_url VARCHAR(500),
    is_featured BOOLEAN DEFAULT FALSE,
    order_index INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Relationship Tables
```sql
-- Relación proyectos-habilidades (Many-to-Many)
CREATE TABLE project_skills (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    skill_id UUID REFERENCES skills(id) ON DELETE CASCADE,
    usage_level VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(project_id, skill_id)
);

-- Relación experiencia-habilidades (Many-to-Many)
CREATE TABLE experience_skills (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    experience_id UUID REFERENCES experience(id) ON DELETE CASCADE,
    skill_id UUID REFERENCES skills(id) ON DELETE CASCADE,
    usage_level VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(experience_id, skill_id)
);
```

---

## 🌿 Database Branching Strategy

### Estructura de Branches
```
main (producción)
├── staging (pre-producción)
├── development (desarrollo)
└── feature/
    ├── feature/new-skills-table
    ├── feature/projects-optimization
    └── feature/experience-refactor
```

### Workflow de Desarrollo
```bash
# 1. Crear branch de feature desde main
neon branches create feature/new-endpoint --parent main

# 2. Desarrollar y probar en feature branch
# Connection string específico del branch
postgresql://user:pass@ep-xxx.neon.tech/dbname?sslmode=require&branch=feature/new-endpoint

# 3. Testing y validación
# Ejecutar tests contra el feature branch

# 4. Merge a development
neon branches merge feature/new-endpoint development

# 5. Testing en staging
neon branches merge development staging

# 6. Deploy a producción
neon branches merge staging main
```

---

## 🚀 Setup y Configuración

### 1. Crear Proyecto en Neon
```bash
# Instalar Neon CLI
npm install -g neon-cli

# Autenticarse
neon auth

# Crear nuevo proyecto
neon projects create portfolio-db --region us-east-1

# Crear branches iniciales
neon branches create development --parent main
neon branches create staging --parent main
```

### 2. Variables de Entorno por Branch
```bash
# Producción (main branch)
DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/portfolio_db?sslmode=require

# Staging
DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/portfolio_db?sslmode=require&branch=staging

# Development
DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/portfolio_db?sslmode=require&branch=development
```

### 3. Configuración de Schema
```bash
# Ejecutar schema en main branch
psql $DATABASE_URL -f schema.sql

# Poblar con datos de prueba en development
psql $DATABASE_URL_DEV -f seed-data.sql
```

---

## 📈 Performance y Optimización

### Indexes Recomendados
```sql
-- Performance indexes
CREATE INDEX idx_experience_dates ON experience(start_date DESC, end_date DESC);
CREATE INDEX idx_experience_current ON experience(is_current) WHERE is_current = TRUE;
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_featured ON projects(featured) WHERE featured = TRUE;
CREATE INDEX idx_skills_category ON skills(category);
CREATE INDEX idx_skills_proficiency ON skills(proficiency_level DESC);

-- Full-text search indexes (si se necesita)
CREATE INDEX idx_projects_search ON projects USING GIN (to_tsvector('english', title || ' ' || description));
CREATE INDEX idx_experience_search ON experience USING GIN (to_tsvector('english', company || ' ' || position));
```

### Query Optimization Tips
- Usar `LIMIT` en queries que no necesiten todos los resultados
- Implementar paginación para listas grandes
- Usar indexes compuestos para queries con múltiples WHERE conditions
- Evitar N+1 queries usando JOINs apropiados

---

## 🔍 Monitoring y Observabilidad

### Métricas Importantes
- **Connection Count**: Número de conexiones activas
- **Query Performance**: Tiempo de ejecución de queries
- **Storage Usage**: Uso de almacenamiento por branch
- **Compute Time**: Tiempo de compute utilizado

### Alertas Recomendadas
- Connection count > 80% del límite
- Query duration > 1000ms
- Error rate > 5%
- Storage usage > 90% del plan

---

## 🔐 Seguridad y Backup

### Configuraciones de Seguridad
```sql
-- Configurar SSL obligatorio
ALTER SYSTEM SET ssl = on;
ALTER SYSTEM SET ssl_prefer_server_ciphers = on;

-- Configurar timeouts
ALTER SYSTEM SET statement_timeout = '30s';
ALTER SYSTEM SET idle_in_transaction_session_timeout = '10min';
```

### Backup Strategy
- **Point-in-time Recovery**: Automático con Neon (retención configurable)
- **Branch Snapshots**: Crear branches para backups importantes
- **Schema Versioning**: Mantener schema.sql en control de versiones

---

## 🛠️ Maintenance y Troubleshooting

### Comandos Útiles de Neon CLI
```bash
# Ver estado de branches
neon branches list

# Información de proyecto
neon projects show

# Métricas de uso
neon consumption

# Logs de conexión
neon logs

# Reset de password
neon users reset-password
```

### Troubleshooting Común
- **Connection timeout**: Verificar connection string y región
- **SSL errors**: Asegurar que sslmode=require esté configurado
- **Performance lenta**: Revisar indexes y queries en Neon Console
- **Límite de conexiones**: Implementar connection pooling

---

## 📚 Referencias y Documentación

### Enlaces Útiles
- [Neon Documentation](https://neon.tech/docs/)
- [PostgreSQL 17 Release Notes](https://www.postgresql.org/docs/17/release-17.html)
- [Neon CLI Reference](https://neon.tech/docs/reference/cli)
- [PostgreSQL 17 Features](https://www.postgresql.org/docs/17/)

### Mejores Prácticas
- Usar branches para cada feature/environment
- Mantener schema.sql actualizado en control de versiones
- Implementar monitoring proactivo
- Usar connection pooling para aplicaciones serverless
- Revisar métricas de performance regularmente

---

**Database**: PostgreSQL 17 con Neon.tech
**Branching**: Git-like workflow para máxima flexibilidad
**Performance**: Optimizado para cargas de trabajo serverless
**Monitoring**: Observabilidad completa con Neon Console