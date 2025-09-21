# Setup - Docker Compose para Portfolio Serverless System

> **Propósito**: Configuración completa de contenedores Docker para desarrollo local del sistema de portfolio serverless
> **Última actualización**: Enero 2025
> **Arquitectura**: Microservicios serverless replicando AWS Lambda + Neon PostgreSQL + Astro v5
> **Node.js**: v22 LTS Alpine (última versión)
> **PostgreSQL**: v17 (última versión disponible)

---

## 🎯 Propósito de la Carpeta Setup

La carpeta `setup/` contiene **exclusivamente la configuración de Docker Compose** para replicar la arquitectura serverless completa en un entorno de desarrollo local containerizado.

### ✅ ¿Qué SÍ va aquí?
- 🐳 **Dockerfiles para desarrollo local**: Configuración de contenedores
- 🔧 **Docker Compose**: Orquestación de servicios
- 🌐 **Configuración Nginx**: API Gateway local
- 🗄️ **PostgreSQL local**: Simulación de Neon database
- 📁 **Estructura de referencia**: Solo archivos Docker, no lógica

### ❌ ¿Qué NO va aquí?
- ❌ Código de aplicación (va en `server/lambda/`)
- ❌ Lógica de negocio (va en `server/lambda/`)
- ❌ Requirements.txt (van en `server/lambda/`)
- ❌ Scripts de automatización (van en `scripts/`)
- ❌ Esquemas de DB (van en `db/`)

---

## 🏗️ Estructura Actual de Setup

### Arquitectura Completa de Directorios
```
setup/
├── docker-compose.yml              # Configuración base de servicios
├── docker-compose.local.yml        # Override para desarrollo local
├── docker-compose.test.yml         # Override para testing
├── docker-compose.dev.yml          # Override para desarrollo
├── docker-compose.prod.yml         # Override para simulación producción
├── app/                            # Frontend Astro v5
│   └── Dockerfile                  # Node.js 22 LTS Alpine
├── database/                       # PostgreSQL 17 + Neon Proxy
│   ├── Dockerfile                  # PostgreSQL 17 Alpine
│   ├── init-portfolio-db.sql       # Inicialización Docker
│   └── neon-proxy.Dockerfile       # Node.js 22 LTS + Neon proxy
├── proxy/                          # API Gateway Nginx
│   ├── Dockerfile                  # Nginx Alpine
│   ├── nginx.conf                  # Configuración proxy
│   └── conf.d/                     # Configuraciones adicionales
└── server/                         # Microservicios Lambda (Solo Dockerfiles)
    └── lambda/
        ├── personal-info/
        │   └── Dockerfile           # AWS Lambda Python 3.13
        ├── skills/
        │   └── Dockerfile           # AWS Lambda Python 3.13
        ├── experience/
        │   └── Dockerfile           # AWS Lambda Python 3.13
        └── projects/
            └── Dockerfile           # AWS Lambda Python 3.13
```

---

## 🚀 Stack Tecnológico Containerizado

### Frontend Container (Astro v5)
```yaml
Servicio: portfolio-frontend
Base Image: node:22-alpine          # ← Node.js 22 LTS (actualizado)
Puerto: 4321
Features:
  - Content Layer con type-safety
  - Server Islands para contenido dinámico
  - Astro Actions para server calls
  - Hot reload habilitado
  - TypeScript strict mode
```

### Server Containers (AWS Lambda Simulation)
```yaml
Servicios Lambda:
  personal-info-lambda:
    Base Image: public.ecr.aws/lambda/python:3.13
    Puerto: 8001
    Función: Gestión de información personal

  skills-lambda:
    Base Image: public.ecr.aws/lambda/python:3.13
    Puerto: 8002
    Función: Gestión de habilidades técnicas

  experience-lambda:
    Base Image: public.ecr.aws/lambda/python:3.13
    Puerto: 8003
    Función: Gestión de experiencia profesional

  projects-lambda:
    Base Image: public.ecr.aws/lambda/python:3.13
    Puerto: 8004
    Función: Gestión de portfolio de proyectos

Runtime:
  - Amazon Linux 2023
  - Lambda Runtime Interface Emulator
  - FastAPI framework
  - Mangum adapter (FastAPI → Lambda)
```

### Database Container (PostgreSQL 17)
```yaml
Servicio: portfolio-db
Base Image: postgres:17-alpine       # ← PostgreSQL 17 (actualizado)
Puerto: 5432
Features:
  - PostgreSQL 17 con mejoras de performance
  - Configuración optimizada para desarrollo
  - Inicialización automática con schema
  - Datos de prueba incluidos
  - Extensions: uuid-ossp, pg_trgm, btree_gin

Neon Proxy:
  Base Image: node:22-alpine          # ← Node.js 22 LTS (actualizado)
  Puerto: 5433
  Función: WebSocket compatibility con driver Neon
```

### API Gateway Container (Nginx)
```yaml
Servicio: api-gateway
Base Image: nginx:1.27-alpine
Puerto: 8080
Función:
  - Proxy reverso para microservicios
  - Load balancing entre servicios
  - CORS configuration
  - Health checks
  - Request routing basado en path
```


---

## 🌐 Arquitectura de Microservicios

### Flujo de Datos Completo
```
┌─────────────────┐    HTTP/4321    ┌─────────────────┐
│  Astro v5 App   │◄──────────────►│   User Browser  │
│  (Frontend)     │                 │                 │
└─────────┬───────┘                 └─────────────────┘
          │ API Calls
          ▼ HTTP/8080
┌─────────────────┐
│  Nginx Proxy    │ /api/personal-info → personal-info-lambda:8001
│  (API Gateway)  │ /api/skills        → skills-lambda:8002
│                 │ /api/experience    → experience-lambda:8003
│                 │ /api/projects      → projects-lambda:8004
└─────────┬───────┘
          │ Route & Load Balance
          ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ personal-info   │    │ skills-lambda   │    │ experience      │    │ projects        │
│ :8001           │    │ :8002           │    │ :8003           │    │ :8004           │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │                      │
          └──────────────────────┼──────────────────────┼──────────────────────┘
                                 │ Database Connections
                                 ▼ PostgreSQL Protocol
                   ┌─────────────────┐    ┌─────────────────┐
                   │  Neon Proxy     │    │  PostgreSQL 17  │
                   │  :5433          │◄──►│  :5432          │
                   │  (WebSocket)    │    │  (Native)       │
                   └─────────────────┘    └─────────────────┘
```

---

## 🚀 Comandos de Gestión con Scripts Python

### Sistema de Gestión Automatizada
Todos los comandos utilizan el sistema de scripts Python ubicado en `scripts/run.py setup`

### Base de Datos (PostgreSQL 17 + Neon Proxy)
```bash
# Levantar solo la base de datos
python scripts/run.py setup --action=up --services=db --env=local --verbose

# Ver logs de la base de datos en tiempo real
python scripts/run.py setup --action=logs --services=db --env=local --follow-logs

# Verificar estado y health checks
python scripts/run.py setup --action=status --services=db --env=local --verbose

# Reiniciar base de datos
python scripts/run.py setup --action=restart --services=db --env=local

# Parar base de datos
python scripts/run.py setup --action=down --services=db --env=local
```

### Funciones Lambda (Microservicios Server)
```bash
# Levantar todas las funciones Lambda
python scripts/run.py setup --action=up --services=server --env=local --verbose

# Función personal-info únicamente
python scripts/run.py setup --action=up --services=server --server-services=personal-info --env=local

# Función skills únicamente
python scripts/run.py setup --action=up --services=server --server-services=skills --env=local

# Experience + Projects específicamente
python scripts/run.py setup --action=up --services=server --server-services=experience,projects --env=local

# Todas las funciones server
python scripts/run.py setup --action=up --services=server --server-services=all --env=local
```

### Frontend (Astro v5)
```bash
# Levantar solo el frontend
python scripts/run.py setup --action=up --services=frontend --env=local --verbose

# Con hot reload habilitado para desarrollo
python scripts/run.py setup --action=up --services=frontend --env=local --follow-logs

# Rebuild con cache clearing
python scripts/run.py setup --action=up --services=frontend --env=local --build
```

### API Gateway (Nginx Proxy)
```bash
# Levantar solo el API Gateway
python scripts/run.py setup --action=up --services=gateway --env=local --verbose

# Gateway con todos los servers
python scripts/run.py setup --action=up --services=gateway,server --env=local
```


### Gestión de Entornos Completos
```bash
# Entorno completo local (todo el stack)
python scripts/run.py setup --action=up --env=local --verbose

# Entorno de testing
python scripts/run.py setup --action=up --env=test --verbose

# Entorno de desarrollo
python scripts/run.py setup --action=up --env=dev --verbose

# Simulación de producción
python scripts/run.py setup --action=up --env=prod --verbose

# Bajar todo el entorno
python scripts/run.py setup --action=down --env=local

# Estado completo del sistema
python scripts/run.py setup --action=status --env=local --verbose
```

---

## 🛠️ Configuraciones de Entorno

### Variables de Entorno por Ambiente

#### Desarrollo Local (`.env.local`)
```bash
# Frontend (Astro v5)
NODE_ENV=development
ASTRO_PORT=4321
API_BASE_URL=http://localhost:8080

# Server (Lambda Functions)
PERSONAL_INFO_API_URL=http://localhost:8001
SKILLS_API_URL=http://localhost:8002
EXPERIENCE_API_URL=http://localhost:8003
PROJECTS_API_URL=http://localhost:8004

# Database (PostgreSQL 17)
DATABASE_URL=postgresql://postgres:portfolio_password@localhost:5432/portfolio_local
NEON_DATABASE_URL=postgresql://postgres:portfolio_password@localhost:5433/portfolio_local
NEON_BRANCH=local

# Development Features
HOT_RELOAD=true
DEBUG_MODE=true
LOG_LEVEL=debug
```

#### Testing (`.env.test`)
```bash
NODE_ENV=test
DATABASE_URL=postgresql://postgres:portfolio_password@localhost:5432/portfolio_test
NEON_BRANCH=test
HOT_RELOAD=false
DEBUG_MODE=false
LOG_LEVEL=error
```

#### Producción Simulada (`.env.prod`)
```bash
NODE_ENV=production
DATABASE_URL=postgresql://postgres:portfolio_password@localhost:5432/portfolio_prod
NEON_BRANCH=main
HOT_RELOAD=false
DEBUG_MODE=false
LOG_LEVEL=warn
MONITORING_ENABLED=true
```

---

## 🔧 Configuración de Servicios Detallada

### Personal Info Lambda (Puerto 8001)
```yaml
Configuración Docker:
  Imagen Base: public.ecr.aws/lambda/python:3.13
  Runtime: Lambda Runtime Interface Emulator
  Código Fuente: server/lambda/personal-info/

Capacidades:
  - CRUD información personal
  - Validación con Pydantic
  - Conexión AsyncPG a PostgreSQL
  - Health checks automáticos
  - AWS Lambda Powertools integrado
```

### Skills Lambda (Puerto 8002)
```yaml
Configuración Docker:
  Imagen Base: public.ecr.aws/lambda/python:3.13
  Runtime: Lambda Runtime Interface Emulator
  Código Fuente: server/lambda/skills/

Capacidades:
  - Gestión de habilidades técnicas
  - Categorización y proficiency levels
  - Skills matrix con relaciones
  - Featured skills management
```

### Experience Lambda (Puerto 8003)
```yaml
Configuración Docker:
  Imagen Base: public.ecr.aws/lambda/python:3.13
  Runtime: Lambda Runtime Interface Emulator
  Código Fuente: server/lambda/experience/

Capacidades:
  - Experiencia profesional CRUD
  - Timeline de carrera
  - Tecnologías por posición
  - Achievements tracking
```

### Projects Lambda (Puerto 8004)
```yaml
Configuración Docker:
  Imagen Base: public.ecr.aws/lambda/python:3.13
  Runtime: Lambda Runtime Interface Emulator
  Código Fuente: server/lambda/projects/

Capacidades:
  - Portfolio de proyectos
  - Categorización y estado
  - Tecnologías utilizadas
  - Links a demos y repositorios
```

---

## 🌐 Configuración Nginx (API Gateway)

### Routing de Microservicios
```nginx
# proxy/nginx.conf
upstream personal_info_server {
    server personal-info-lambda:8080 max_fails=3 fail_timeout=30s;
}

upstream skills_server {
    server skills-lambda:8080 max_fails=3 fail_timeout=30s;
}

upstream experience_server {
    server experience-lambda:8080 max_fails=3 fail_timeout=30s;
}

upstream projects_server {
    server projects-lambda:8080 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    server_name localhost;

    # Health check para el gateway
    location /health {
        access_log off;
        return 200 "Portfolio API Gateway - Healthy\n";
        add_header Content-Type text/plain;
    }

    # Personal Info API
    location /api/personal-info {
        proxy_pass http://personal_info_server/2015-03-31/functions/function/invocations;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Content-Type application/json;
    }

    # Skills API
    location /api/skills {
        proxy_pass http://skills_server/2015-03-31/functions/function/invocations;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Content-Type application/json;
    }

    # Experience API
    location /api/experience {
        proxy_pass http://experience_server/2015-03-31/functions/function/invocations;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Content-Type application/json;
    }

    # Projects API
    location /api/projects {
        proxy_pass http://projects_server/2015-03-31/functions/function/invocations;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Content-Type application/json;
    }

    # CORS Support
    add_header Access-Control-Allow-Origin *;
    add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
    add_header Access-Control-Allow-Headers "Content-Type, Authorization, X-Requested-With";

    if ($request_method = 'OPTIONS') {
        return 204;
    }
}
```

---

## 📊 Health Checks y Monitoring

### Health Checks Automatizados
```yaml
Portfolio Database:
  Endpoint: pg_isready -U postgres -d portfolio_local
  Interval: 30s
  Timeout: 10s
  Retries: 3

Personal Info Lambda:
  Endpoint: curl -f http://localhost:8080/2015-03-31/functions/function/invocations
  Method: POST {"httpMethod":"GET","path":"/health"}
  Interval: 30s

Skills Lambda:
  Endpoint: curl -f http://localhost:8080/2015-03-31/functions/function/invocations
  Method: POST {"httpMethod":"GET","path":"/health"}
  Interval: 30s

API Gateway:
  Endpoint: curl -f http://localhost/health
  Interval: 30s
  Expected: "Portfolio API Gateway - Healthy"

Frontend:
  Endpoint: curl -f http://localhost:4321
  Interval: 30s
  Start Period: 60s (debido a build time)
```

### Logging Centralizado
```bash
# Ver logs de todos los servicios
python scripts/run.py setup --action=logs --env=local --follow-logs

# Logs específicos por servicio
docker-compose logs -f portfolio-frontend
docker-compose logs -f personal-info-lambda
docker-compose logs -f portfolio-db
docker-compose logs -f api-gateway

# Logs con timestamps para debugging
docker-compose logs -f --timestamps
```

---

## 🧪 Testing y QA

### Estrategia de Testing Containerizada
```bash
# Testing completo del stack
python scripts/run.py setup --action=up --env=test --build

# Testing de servicios individuales
python scripts/run.py setup --action=up --services=backend --backend-services=personal-info --env=test

# Integration testing con base de datos
python scripts/run.py setup --action=up --services=db,server --env=test

# Performance testing local
python scripts/run.py setup --action=up --env=local
# Usar herramientas como wrk, ab, o Postman para load testing
```

### Configuración de Testing
```yaml
# docker-compose.test.yml
services:
  portfolio-db:
    environment:
      POSTGRES_DB: portfolio_test
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_password
    tmpfs:
      - /var/lib/postgresql/data  # DB en memoria para velocidad

  personal-info-lambda:
    environment:
      DATABASE_URL: postgresql://test_user:test_password@portfolio-db:5432/portfolio_test
      LOG_LEVEL: error
      ENVIRONMENT: test
    command: pytest tests/ -v --cov=app --cov-report=html
```

---

## 🚀 Deployment y CI/CD

### Build & Deploy Workflow
```bash
# Build local para testing
python scripts/run.py setup --action=up --env=local --build

# Simulación de producción
python scripts/run.py setup --action=up --env=prod --build

# Limpieza completa para fresh start
python scripts/run.py setup --action=clean --verbose
docker system prune -f
python scripts/run.py setup --action=up --env=local --build
```

### Multi-Environment Support
```yaml
Local Development:
  - Hot reload habilitado
  - Debug logging
  - Development database
  - Source code mounted as volumes

Testing:
  - In-memory database
  - Error-only logging
  - Test data fixtures
  - Coverage reporting

Production Simulation:
  - Optimized images
  - Production-like settings
  - Resource limits
  - Monitoring enabled
```

---

## 🔧 Troubleshooting

### Problemas Comunes y Soluciones

#### Puertos en uso
```bash
# Verificar qué está usando los puertos
python scripts/run.py setup --action=status --verbose
netstat -tulpn | grep :4321
netstat -tulpn | grep :8080
```

#### Database connection issues
```bash
# Verificar logs de PostgreSQL
docker-compose logs portfolio-db

# Test manual de conexión
docker exec -it portfolio-db psql -U postgres -d portfolio_local -c "SELECT version();"
```

#### Lambda functions no responden
```bash
# Verificar logs individuales
docker-compose logs personal-info-lambda
docker-compose logs skills-lambda

# Test directo del Lambda Runtime Interface Emulator
curl -X POST "http://localhost:8001/2015-03-31/functions/function/invocations" \
  -d '{"httpMethod":"GET","path":"/health"}'
```

#### Rebuild completo por problemas de caché
```bash
# Limpieza completa
python scripts/run.py setup --action=clean --verbose
docker system prune -a -f
docker volume prune -f

# Rebuild desde cero
python scripts/run.py setup --action=up --env=local --build --verbose
```

---

## 📋 Estructura de Archivos Docker

### Distribución de Responsabilidades
```
setup/
├── docker-compose.yml              # Servicios base
├── docker-compose.local.yml        # Development overrides
├── docker-compose.test.yml         # Testing configuration
├── docker-compose.dev.yml          # Dev environment
├── docker-compose.prod.yml         # Production simulation
│
├── app/Dockerfile                  # Frontend: Node.js 22 + Astro v5
├── database/
│   ├── Dockerfile                  # PostgreSQL 17 Alpine
│   ├── init-portfolio-db.sql       # Schema + seed data para Docker
│   └── neon-proxy.Dockerfile       # Node.js 22 + Neon WebSocket proxy
├── proxy/
│   ├── Dockerfile                  # Nginx Alpine
│   └── nginx.conf                  # API Gateway configuration
│
└── server/                         # Solo Dockerfiles (lógica en server/)
    ├── lambda/
    │   ├── personal-info/Dockerfile # AWS Lambda Python 3.13
    │   ├── skills/Dockerfile        # AWS Lambda Python 3.13
    │   ├── experience/Dockerfile    # AWS Lambda Python 3.13
    │   └── projects/Dockerfile      # AWS Lambda Python 3.13
    └── layer/
        └── db-connection/
            ├── Dockerfile           # AWS Lambda Layer Python 3.13
            ├── requirements.txt     # Layer dependencies
            └── src/                 # Layer shared code
```

---

## 🎯 Casos de Uso Comunes

### Desarrollo Full-Stack
```bash
# Stack completo para desarrollo
python scripts/run.py setup --action=up --env=local --follow-logs

# URLs disponibles:
# Frontend: http://localhost:4321
# API Gateway: http://localhost:8080
# Direct Lambda access: http://localhost:8001-8004
# Database: localhost:5432
```

### Desarrollo Server Only
```bash
# Solo server + database
python scripts/run.py setup --action=up --services=server,db --env=local

# Desarrollo de un servicio específico
python scripts/run.py setup --action=up --services=server --server-services=personal-info --env=local
```

### Frontend Development
```bash
# Solo frontend con API Gateway mock
python scripts/run.py setup --action=up --services=frontend,gateway --env=local

# Frontend standalone (usando APIs externas)
python scripts/run.py setup --action=up --services=frontend --env=local
```

### Testing Scenarios
```bash
# Full integration testing
python scripts/run.py setup --action=up --env=test --build

# Unit testing de servicios
python scripts/run.py setup --action=up --services=backend --backend-services=skills --env=test

# Database testing
python scripts/run.py setup --action=up --services=db --env=test
```

---

## 📈 Performance y Optimización

### Optimización de Container Startup
```yaml
Health Check Configuration:
  - Database: start_period=40s (PostgreSQL initialization)
  - Lambda Functions: start_period=30s (Python runtime)
  - Frontend: start_period=60s (Astro build process)
  - API Gateway: start_period=20s (Nginx startup)

Resource Limits:
  - Development: Sin límites para debugging
  - Production simulation: CPU y memoria limitados
  - Testing: Recursos optimizados para velocidad
```

### Cold Start Optimization
```yaml
Lambda Runtime Interface Emulator:
  - Warm containers cuando sea posible
  - Connection pooling optimizado
  - Dependencias optimizadas en cada función
  - Optimized Docker images con multi-stage builds
```

---

## 📚 Referencias

### Tecnologías y Versiones
- **Node.js**: v22 LTS Alpine (última versión)
- **PostgreSQL**: v17 Alpine (última versión)
- **Python**: v3.13 (runtime AWS Lambda)
- **Nginx**: v1.27 Alpine
- **Docker Compose**: v2.x

### Enlaces Útiles
- [AWS Lambda Runtime Interface Emulator](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-api.html)
- [PostgreSQL 17 Documentation](https://www.postgresql.org/docs/17/)
- [Astro v5 Documentation](https://docs.astro.build/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

---

**Setup Directory**: Configuración completa Docker para desarrollo local
**Arquitectura**: Microservicios serverless con PostgreSQL 17 y Node.js 22
**Gestión**: Scripts Python automatizados con múltiples entornos
**Testing**: Configuración completa para TDD y integration testing