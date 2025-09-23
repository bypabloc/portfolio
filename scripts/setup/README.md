# setup

**Script de gestión de entornos de desarrollo para el Portfolio Serverless System**

Automatiza la gestión de contenedores para el desarrollo local, testing, desarrollo y producción del sistema de portfolio serverless basado en Astro v5 + AWS Lambda + FastAPI + Neon PostgreSQL.

🏗️ **Arquitectura**: Replica la arquitectura serverless en contenedores para desarrollo local con separación completa app/server.

## 🚀 Comandos rápidos

### Base de datos (DB)
```bash
# Levantar solo la base de datos
python scripts/run.py setup --action=up --services=db --env=local --verbose

# Ver logs de la base de datos
python scripts/run.py setup --action=logs --services=db --env=local

# Parar la base de datos
python scripts/run.py setup --action=down --services=db --env=local

# Reiniciar la base de datos
python scripts/run.py setup --action=restart --services=db --env=local

# Ver estado de la base de datos
python scripts/run.py setup --action=status --services=db --env=local
```

### Servicios específicos
```bash
# Solo website (Astro v5)
python scripts/run.py setup --action=up --services=website --env=local --verbose

# Solo server (todos los microservices)
python scripts/run.py setup --action=up --services=server --env=local --verbose

# Solo API Gateway
python scripts/run.py setup --action=up --services=gateway --env=local --verbose

# Todos los servicios
python scripts/run.py setup --action=up --services=all --env=local --verbose
```


### Gestión de entornos
```bash
# Entorno local (desarrollo)
python scripts/run.py setup --action=up --env=local --verbose

# Entorno de testing
python scripts/run.py setup --action=up --env=test --verbose

# Entorno de desarrollo
python scripts/run.py setup --action=up --env=dev --verbose

# Entorno de release/staging
python scripts/run.py setup --action=up --env=release --verbose

# Entorno de producción
python scripts/run.py setup --action=up --env=prod --verbose
```

### Operaciones comunes
```bash
# Ver estado de todos los servicios
python scripts/run.py setup --action=status --verbose

# Ver logs en tiempo real
python scripts/run.py setup --action=logs --follow-logs

# Reiniciar todo el entorno
python scripts/run.py setup --action=restart --env=local

# Bajar todo el entorno
python scripts/run.py setup --action=down --env=local

# Limpiar recursos Docker
python scripts/run.py setup --action=clean --verbose
```

## ¿Qué hace?

- 🚀 **Levanta entornos completos** con un solo comando
- 🐳 **Maneja múltiples servicios** (app, server, database, gateway)
- 🔧 **Configura variables de entorno** específicas por entorno
- 📊 **Monitorea estado** de servicios y dependencias
- 🔄 **Reinicia servicios** selectivamente o todos
- 🧹 **Limpia recursos** Docker automáticamente
- ⚡ **Hot reload** para desarrollo activo
- 🌐 **API Gateway consolidado** - Todos los microservicios en un solo puerto
- 🔒 **Gestión centralizada** - Todos los comandos Docker van a través del script

## Arquitectura de servicios

### Website (Astro v5)
- **Servicio**: `portfolio-website`
- **Puerto**: `4321` (Astro dev server)
- **Features**: Content Layer, Server Islands, Astro Actions
- **Hot reload**: Habilitado en modo development

### Server Microservices (AWS Lambda + FastAPI)
- **personal-info-lambda**: Puerto `8001` - Lambda para información personal
- **skills-lambda**: Puerto `8002` - Lambda para gestión de habilidades
- **experience-lambda**: Puerto `8003` - Lambda para experiencia profesional
- **projects-lambda**: Puerto `8004` - Lambda para portfolio de proyectos

### Database (Neon PostgreSQL replica)
- **Servicio**: `portfolio-db`
- **Puerto**: `5432`
- **Branching**: Simulado con diferentes esquemas por entorno

### API Gateway (Nginx)
- **Servicio**: `api-gateway`
- **Puerto**: `8090` (cambiado de 8080 para evitar conflictos)
- **Routing**: Consolida todos los microservicios en URLs limpias
- **URLs disponibles**:
  - `http://localhost:8090/health` - Health check del gateway
  - `http://localhost:8090/api/personal-info` - Información personal
  - `http://localhost:8090/api/skills` - Gestión de habilidades
  - `http://localhost:8090/api/experience` - Experiencia profesional
  - `http://localhost:8090/api/projects` - Portfolio de proyectos

## Entornos disponibles

### `local` - Desarrollo activo
- Hot reload habilitado para todos los servicios
- Logs detallados (debug level)
- Debug mode activado con puertos específicos
- Volúmenes de código fuente montados
- Variables de desarrollo (.env.local)

### `test` - Testing automatizado
- Contenedores optimizados para testing
- Base de datos en memoria (tmpfs)
- Sin hot reload (estabilidad)
- Test runner incluido
- Variables de test (.env.test)

### `dev` - Desarrollo estable
- Replica entorno de desarrollo remoto
- Base de datos persistente
- Profiling habilitado
- Monitoring de desarrollo
- Variables de dev branch (.env.dev)

### `release` - Pre-producción/Staging
- Configuración similar a producción
- Límites de recursos aplicados
- Monitoring habilitado
- Testing de release
- Variables de staging (.env.release)

### `prod` - Simulación de producción
- Configuración de producción completa
- Límites estrictos de recursos
- Monitoring y métricas completas
- Reinicio automático (restart: always)
- Variables de producción (.env.prod)

## Flags disponibles

**Gestión de entornos:**
- `--env="local|test|dev|release|prod"` - Entorno a levantar (default: local)
- `--services="website|server|db|gateway|all"` - Servicios específicos (default: all)

**Operaciones:**
- `--action="up|down|restart|status|logs|clean"` - Acción a ejecutar (default: up)
- `--build` - Forzar rebuild de imágenes Docker (default: false)
- `--detach` - Ejecutar en background (default: true)

**Configuración:**
- `--project-path="/path/to/project"` - Ruta del proyecto (default: auto-detect)
- `--verbose` - Mostrar información detallada (default: false)
- `--follow-logs` - Seguir logs en tiempo real después de levantar (default: false)

**Microservices específicos:**
- `--server-services="personal-info|skills|experience|projects"` - Lambda functions específicas

## Ejemplos de uso

### Desarrollo local básico
```bash
# Levantar entorno completo local
python scripts/run.py setup --env="local"

# Con información detallada
python scripts/run.py setup --env="local" --verbose

# Seguir logs después de levantar
python scripts/run.py setup --env="local" --follow-logs
```

### Gestión de servicios específicos
```bash
# Solo app (Astro)
python scripts/run.py setup --env="local" --services="website"

# Solo server microservices
python scripts/run.py setup --env="local" --services="server"

# Solo base de datos
python scripts/run.py setup --env="local" --services="db"

# Website + API Gateway
python scripts/run.py setup --env="local" --services="website,gateway"
```

### Microservices server específicos
```bash
# Solo lambda personal-info
python scripts/run.py setup --env="local" --services="server" --server-services="personal-info"

# Solo lambda skills
python scripts/run.py setup --env="local" --services="server" --server-services="skills"

# Solo lambda experience
python scripts/run.py setup --env="local" --services="server" --server-services="experience"

# Solo lambda projects
python scripts/run.py setup --env="local" --services="server" --server-services="projects"

# Múltiples lambdas específicas
python scripts/run.py setup --env="local" --services="server" --server-services="personal-info,skills,experience"

# Todos los microservices server
python scripts/run.py setup --env="local" --services="server" --server-services="all"
```


### Diferentes entornos
```bash
# Entorno de testing
python scripts/run.py setup --env="test" --verbose

# Entorno de desarrollo
python scripts/run.py setup --env="dev"

# Entorno de release/staging
python scripts/run.py setup --env="release" --verbose

# Simulación de producción
python scripts/run.py setup --env="prod" --verbose
```

### Operaciones de gestión
```bash
# Ver estado de servicios
python scripts/run.py setup --action="status" --verbose

# Ver logs de servicios
python scripts/run.py setup --action="logs" --follow-logs

# Reiniciar servicios
python scripts/run.py setup --action="restart" --env="local"

# Bajar servicios
python scripts/run.py setup --action="down" --env="local"

# Limpiar recursos Docker
python scripts/run.py setup --action="clean" --verbose
```

### Con rebuild forzado
```bash
# Rebuild completo del entorno
python scripts/run.py setup --env="local" --build --verbose

# Rebuild solo de la app
python scripts/run.py setup --env="local" --services="website" --build
```

### Para CI/CD y testing
```bash
# Levantar entorno test sin detach (para CI)
python scripts/run.py setup --env="test" --detach=false

# Entorno test con rebuild
python scripts/run.py setup --env="test" --build --verbose
```

## Estructura de archivos Docker

El script busca automáticamente los archivos de configuración Docker en estas ubicaciones:

**Ubicaciones de búsqueda:**
- `./docker-compose.yml` (raíz del proyecto)
- `./docker/docker-compose.yml` (carpeta docker tradicional)
- `./setup/docker-compose.yml` (carpeta setup - recomendada) ✅

**Estructura recomendada:**

```
portfolio/
├── setup/                              # ← Ubicación actual de archivos Docker
│   ├── docker-compose.yml              # Configuración base
│   ├── docker-compose.local.yml        # Override para local
│   ├── docker-compose.test.yml         # Override para test
│   ├── docker-compose.dev.yml          # Override para dev
│   ├── docker-compose.release.yml      # Override para release/staging
│   ├── docker-compose.prod.yml         # Override para prod
│   ├── app/
│   │   └── Dockerfile                  # Astro v5 container
│   ├── server/                         # (Obsoleto - ver server/ en root)
│   │   └── README.md                   # Referencia a nueva estructura en server/
│   ├── nginx/
│   │   ├── nginx.conf                 # API Gateway config
│   │   └── Dockerfile
│   └── postgres/
│       ├── init.sql                   # DB initialization
│       └── Dockerfile
└── .env.local                         # Variables locales
└── .env.test                          # Variables de test
└── .env.dev                           # Variables de dev
└── .env.release                       # Variables de release/staging
└── .env.prod                          # Variables de prod
```

## Variables de entorno por entorno

### Local (`.env.local`)
```bash
NODE_ENV=development
ASTRO_PORT=4321
API_GATEWAY_URL=http://localhost:8090
# Microservicios individuales (para debug directo)
PERSONAL_INFO_API_URL=http://localhost:8001
SKILLS_API_URL=http://localhost:8002
EXPERIENCE_API_URL=http://localhost:8003
PROJECTS_API_URL=http://localhost:8004
DATABASE_URL=postgresql://postgres:password@localhost:5432/portfolio_local
NEON_BRANCH=local
HOT_RELOAD=true
DEBUG_MODE=true
```

### Test (`.env.test`)
```bash
NODE_ENV=test
ASTRO_PORT=4321
API_GATEWAY_URL=http://localhost:8090
DATABASE_URL=postgresql://postgres:password@localhost:5432/portfolio_test
NEON_BRANCH=test
HOT_RELOAD=false
DEBUG_MODE=false
```

### Dev (`.env.dev`)
```bash
NODE_ENV=development
ASTRO_PORT=4321
API_GATEWAY_URL=http://localhost:8090
DATABASE_URL=postgresql://postgres:password@localhost:5432/portfolio_dev
NEON_BRANCH=dev
HOT_RELOAD=true
DEBUG_MODE=true
LOG_LEVEL=info
```

### Prod (`.env.prod`)
```bash
NODE_ENV=production
ASTRO_PORT=4321
API_GATEWAY_URL=http://localhost:8090
DATABASE_URL=postgresql://postgres:password@localhost:5432/portfolio_prod
NEON_BRANCH=main
HOT_RELOAD=false
DEBUG_MODE=false
LOG_LEVEL=warn
MONITORING_ENABLED=true
```

## Healthchecks y dependencias

El script verifica:
- ✅ **Docker daemon** está corriendo
- ✅ **docker-compose** está disponible
- ✅ **Archivos de configuración** existen
- ✅ **Variables de entorno** están configuradas
- ✅ **Puertos** están disponibles
- ✅ **Servicios** responden a healthchecks

## Logs y monitoreo

### Logs estructurados por servicio:
```bash
# ⚠️ IMPORTANTE: Usar siempre el script centralizado
# NO usar comandos docker directamente

# Ver logs de servicios específicos con el script
python scripts/run.py setup --action=logs --services=server --env=local --follow-logs
python scripts/run.py setup --action=logs --services=gateway --env=local --follow-logs
python scripts/run.py setup --action=logs --services=db --env=local --follow-logs

# Ver logs de microservicios específicos
python scripts/run.py setup --action=logs --services=server --server-services=personal-info --env=local --follow-logs
```

### Métricas de desarrollo:
- Response times de APIs
- Database connection status
- Website build status
- Memory usage por servicio

## ✅ Estado Actual Verificado (2025-09-21)

El sistema está **completamente operativo** con los siguientes servicios confirmados funcionando:

### 🎯 APIs Verificadas (Status 200)
- ✅ **API Gateway Health**: `http://localhost:8090/health`
- ✅ **Personal Info**: `http://localhost:8090/api/personal-info`
- ✅ **Skills**: `http://localhost:8090/api/skills`
- ✅ **Experience**: `http://localhost:8090/api/experience`
- ✅ **Projects**: `http://localhost:8090/api/projects`

### 🏗️ Servicios Activos
- ✅ **Base de datos**: PostgreSQL en puerto 5432 (healthy)
- ✅ **Microservicios**: 4 Lambda functions en puertos 8001-8004 (healthy)
- ✅ **API Gateway**: Nginx en puerto 8090 (healthy)
- ✅ **Red de contenedores**: Configuración limpia y funcional

### 🛠️ Correcciones Implementadas
- ✅ **Neon-proxy deshabilitado**: No es crítico para desarrollo local
- ✅ **URLs consolidadas**: Todas las APIs accesibles desde puerto 8090
- ✅ **Variables de entorno**: Actualizadas para apuntar directamente a PostgreSQL
- ✅ **Conflictos de red**: Resueltos completamente

## Casos de uso comunes

- **Desarrollo activo**: `--env="local" --follow-logs`
- **Testing local**: `--env="test" --services="server,db"`
- **Demo/presentación**: `--env="prod" --verbose`
- **Debug de API**: `--env="local" --services="server" --server-services="personal-info"` o cualquier lambda específica
- **Website only**: `--env="local" --services="website"`
- **Full stack development**: `--env="local"` (default)
- **Solo backend + API Gateway**: `--env="local" --services="server,gateway,db"` ✅ **Recomendado para desarrollo API**

## Requisitos

- **Docker**: v20+ con Docker Compose v2
- **Puertos disponibles**: 4321, 8001-8004, 8090, 5432
- **Memoria**: 2GB mínimo para entorno completo
- **Espacio disco**: 1GB para imágenes Docker

## Troubleshooting

### Puertos en uso:
```bash
# Ver qué está usando los puertos
python scripts/run.py setup --action="status" --verbose
```

### Rebuild por problemas de cache:
```bash
# Rebuild forzado con limpieza
python scripts/run.py setup --action="clean"
python scripts/run.py setup --env="local" --build
```

### Reset completo:
```bash
# ⚠️ IMPORTANTE: Usar solo el script centralizado para limpiar
# NO usar comandos docker directamente

# Limpiar todo y empezar de cero
python scripts/run.py setup --action="clean" --verbose
python scripts/run.py setup --env="local" --build --verbose
```

## Exit codes

- **0**: Operación exitosa
- **1**: Error en configuración o archivos faltantes
- **2**: Docker no disponible o falló
- **3**: Servicios no levantaron correctamente
- **4**: Healthchecks fallaron

## 🏆 Mejores Prácticas

### ⚠️ Gestión Centralizada de Docker
**IMPORTANTE**: Todos los comandos de Docker deben ejecutarse a través del script setup:

```bash
# ✅ CORRECTO - Usar el script setup
python scripts/run.py setup --action=status --verbose
python scripts/run.py setup --action=restart --env=local
python scripts/run.py setup --action=clean --verbose

# ❌ INCORRECTO - NO usar comandos Docker directos
docker ps
docker stop container_name
docker system prune
```

### 🔄 Workflow de Desarrollo Recomendado
1. **Verificar estado**: `python scripts/run.py setup --action=status --verbose`
2. **Levantar servicios**: `python scripts/run.py setup --action=up --services=server,gateway,db --env=local`
3. **Probar APIs**: Usar las URLs del API Gateway en puerto 8090
4. **Ver logs**: `python scripts/run.py setup --action=logs --follow-logs`
5. **Limpiar al terminar**: `python scripts/run.py setup --action=down --env=local`

### 🚀 ARQUITECTURA UNIFICADA - TODO EN PUERTO ${UNIFIED_PORT:-4321}
**NUEVA ESTRUCTURA**: Todos los servicios consolidados en un solo puerto

```bash
# 🎯 PUERTO ÚNICO CONFIGURADO VIA ENV
UNIFIED_PORT=4321  # Default, configurable en archivos .env

# 🎨 WEBSITE - RAÍZ DEL SISTEMA
curl http://localhost:4321/                    # Página principal (Astro v5)
curl http://localhost:4321/about               # Información personal
curl http://localhost:4321/projects            # Portfolio de proyectos

# 🚪 API GATEWAY - MICROSERVICIOS CONSOLIDADOS
curl http://localhost:4321/health              # Health check unificado
curl http://localhost:4321/api/personal-info   # API información personal
curl http://localhost:4321/api/skills          # API habilidades técnicas
curl http://localhost:4321/api/experience      # API experiencia profesional
curl http://localhost:4321/api/projects        # API portfolio de proyectos

# 📚 DOCUMENTACIÓN API INTEGRADA
curl http://localhost:4321/api/personal-info/docs   # Swagger UI personal-info
curl http://localhost:4321/api/skills/docs          # Swagger UI skills
curl http://localhost:4321/api/experience/redoc     # ReDoc experience
curl http://localhost:4321/api/projects/docs        # Swagger UI projects


# ❌ PUERTOS INDIVIDUALES YA NO DISPONIBLES
# Los puertos 8001-8004 y 8090 ya no están expuestos externamente
# Todo el acceso se hace a través del puerto unificado 4321
```

### 🐳 Troubleshooting Efectivo
1. **Siempre usar verbose**: `--verbose` para ver detalles
2. **Limpiar antes de rebuild**: `--action=clean` antes de `--build`
3. **Verificar healthchecks**: El script espera automáticamente a que los servicios estén healthy
4. **Consultar logs**: `--action=logs --follow-logs` para debug en tiempo real

---

**Última actualización**: 2025-09-21
**Estado**: Sistema completamente operativo y verificado
**Mantenedor**: Scripts de automatización centralizados