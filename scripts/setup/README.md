# setup

**Script de gestión de entornos de desarrollo para el Portfolio Serverless System**

Automatiza la gestión de contenedores para el desarrollo local, testing, desarrollo y producción del sistema de portfolio serverless basado en Astro v5 + AWS Lambda + FastAPI + Neon PostgreSQL.

🏗️ **Arquitectura**: Replica la arquitectura serverless en contenedores para desarrollo local con separación completa frontend/backend.

## ¿Qué hace?

- 🚀 **Levanta entornos completos** con un solo comando
- 🐳 **Maneja múltiples servicios** (frontend, backend, database, proxy)
- 🔧 **Configura variables de entorno** específicas por entorno
- 📊 **Monitorea estado** de servicios y dependencias
- 🔄 **Reinicia servicios** selectivamente o todos
- 🧹 **Limpia recursos** Docker automáticamente
- ⚡ **Hot reload** para desarrollo activo

## Arquitectura de servicios

### Frontend (Astro v5)
- **Servicio**: `portfolio-frontend`
- **Puerto**: `4321` (Astro dev server)
- **Features**: Content Layer, Server Islands, Astro Actions
- **Hot reload**: Habilitado en modo development

### Backend Microservices (AWS Lambda + FastAPI)
- **personal-info**: Puerto `8001` - Información personal
- **experience**: Puerto `8002` - Experiencia profesional
- **projects**: Puerto `8003` - Portfolio de proyectos
- **skills**: Puerto `8004` - Matriz de habilidades

### Database (Neon PostgreSQL replica)
- **Servicio**: `portfolio-db`
- **Puerto**: `5432`
- **Branching**: Simulado con diferentes esquemas por entorno

### API Gateway (Nginx)
- **Servicio**: `portfolio-gateway`
- **Puerto**: `8080`
- **Routing**: Enruta requests del frontend a microservios backend

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
- `--services="frontend|backend|db|gateway|all"` - Servicios específicos (default: all)

**Operaciones:**
- `--action="up|down|restart|status|logs|clean"` - Acción a ejecutar (default: up)
- `--build` - Forzar rebuild de imágenes Docker (default: false)
- `--detach` - Ejecutar en background (default: true)

**Configuración:**
- `--project-path="/path/to/project"` - Ruta del proyecto (default: auto-detect)
- `--verbose` - Mostrar información detallada (default: false)
- `--follow-logs` - Seguir logs en tiempo real después de levantar (default: false)

**Microservices específicos:**
- `--backend-services="personal-info|experience|projects|skills"` - Microservicios backend específicos

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
# Solo frontend (Astro)
python scripts/run.py setup --env="local" --services="frontend"

# Solo backend microservices
python scripts/run.py setup --env="local" --services="backend"

# Solo base de datos
python scripts/run.py setup --env="local" --services="db"

# Frontend + API Gateway
python scripts/run.py setup --env="local" --services="frontend,gateway"
```

### Microservices backend específicos
```bash
# Solo servicio personal-info
python scripts/run.py setup --env="local" --services="backend" --backend-services="personal-info"

# Personal-info + Experience
python scripts/run.py setup --env="local" --services="backend" --backend-services="personal-info,experience"

# Todos los microservices backend
python scripts/run.py setup --env="local" --services="backend" --backend-services="all"
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

# Rebuild solo del frontend
python scripts/run.py setup --env="local" --services="frontend" --build
```

### Para CI/CD y testing
```bash
# Levantar entorno test sin detach (para CI)
python scripts/run.py setup --env="test" --detach=false

# Entorno test con rebuild
python scripts/run.py setup --env="test" --build --verbose
```

## Estructura de archivos Docker

El script espera esta estructura en el proyecto:

```
portfolio/
├── setup/
│   ├── docker-compose.yml              # Configuración base
│   ├── docker-compose.local.yml        # Override para local
│   ├── docker-compose.test.yml         # Override para test
│   ├── docker-compose.dev.yml          # Override para dev
│   ├── docker-compose.prod.yml         # Override para prod
│   ├── frontend/
│   │   └── Dockerfile                  # Astro v5 container
│   ├── backend/
│   │   ├── personal-info/
│   │   │   └── Dockerfile             # FastAPI Lambda container
│   │   ├── experience/
│   │   │   └── Dockerfile
│   │   ├── projects/
│   │   │   └── Dockerfile
│   │   └── skills/
│   │       └── Dockerfile
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
API_GATEWAY_URL=http://localhost:8080
PERSONAL_INFO_API_URL=http://localhost:8001
EXPERIENCE_API_URL=http://localhost:8002
PROJECTS_API_URL=http://localhost:8003
SKILLS_API_URL=http://localhost:8004
DATABASE_URL=postgresql://postgres:password@localhost:5432/portfolio_local
NEON_BRANCH=local
HOT_RELOAD=true
DEBUG_MODE=true
```

### Test (`.env.test`)
```bash
NODE_ENV=test
ASTRO_PORT=4321
API_GATEWAY_URL=http://localhost:8080
DATABASE_URL=postgresql://postgres:password@localhost:5432/portfolio_test
NEON_BRANCH=test
HOT_RELOAD=false
DEBUG_MODE=false
```

### Dev (`.env.dev`)
```bash
NODE_ENV=development
ASTRO_PORT=4321
API_GATEWAY_URL=http://localhost:8080
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
API_GATEWAY_URL=http://localhost:8080
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
# Ver logs de un servicio específico
docker-compose logs -f portfolio-frontend

# Ver logs de todos los backend services
docker-compose logs -f personal-info experience projects skills

# Ver logs con timestamps
docker-compose logs -f --timestamps
```

### Métricas de desarrollo:
- Response times de APIs
- Database connection status
- Frontend build status
- Memory usage por servicio

## Casos de uso comunes

- **Desarrollo activo**: `--env="local" --follow-logs`
- **Testing local**: `--env="test" --services="backend,db"`
- **Demo/presentación**: `--env="prod" --verbose`
- **Debug de API**: `--env="local" --services="backend" --backend-services="personal-info"`
- **Frontend only**: `--env="local" --services="frontend"`
- **Full stack development**: `--env="local"` (default)

## Requisitos

- **Docker**: v20+ con Docker Compose v2
- **Puertos disponibles**: 4321, 8001-8004, 8080, 5432
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
# Limpiar todo y empezar de cero
python scripts/run.py setup --action="clean" --verbose
docker system prune -f
python scripts/run.py setup --env="local" --build --verbose
```

## Exit codes

- **0**: Operación exitosa
- **1**: Error en configuración o archivos faltantes
- **2**: Docker no disponible o falló
- **3**: Servicios no levantaron correctamente
- **4**: Healthchecks fallaron