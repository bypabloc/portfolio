# Portfolio Project Documentation

> **⚠️ IMPORTANTE PARA IAs**: Si eres una Inteligencia Artificial y estás leyendo este README, DEBES leer cada uno de los archivos .md individuales en esta carpeta `docs/` para obtener la información completa y detallada. Este README es solo un resumen inicial. Los archivos específicos contienen toda la información técnica necesaria para implementar correctamente el proyecto.

## 📋 Resumen del Proyecto

Este proyecto consiste en un **portfolio/CV moderno y serverless** implementado con arquitectura de separación completa entre frontend y backend:

- **Frontend**: Astro v5 con TypeScript (SSG optimizado)
- **Backend**: AWS Lambda + FastAPI + Python 3.12
- **Base de Datos**: Neon PostgreSQL (serverless)
- **Containerización**: Docker Compose para desarrollo local
- **Testing**: TDD completo con Vitest + pytest
- **Infraestructura**: AWS Lambda + API Gateway + SAM CLI

---

## 📚 Documentación Técnica

### 1. `backend.md` - FastAPI + AWS Lambda Backend
**Enfoque**: Implementación completa del backend serverless

**Contenido Principal**:
- ✅ Configuración FastAPI + Lambda con Mangum adapter
- ✅ Modelos Pydantic para validación tipo-safe
- ✅ Conexión optimizada a Neon PostgreSQL con AsyncPG
- ✅ Implementación de rutas API (personal-info, experience, projects, skills)
- ✅ AWS Lambda Powertools para observabilidad
- ✅ Optimizaciones de cold start (~300ms)
- ✅ Deployment con SAM CLI y API Gateway
- ✅ Integración con Astro frontend via HTTP APIs

**Arquitectura**: Microservicios serverless con FastAPI como framework principal, optimizado para AWS Lambda execution.

### 2. `db.md` - Neon Database Integration
**Enfoque**: Base de datos serverless PostgreSQL optimizada para Lambda

**Contenido Principal**:
- ✅ Configuración de Neon.tech para desarrollo serverless
- ✅ Schema completo para sistema de portfolio (personal_info, experience, projects, skills)
- ✅ Conexiones AsyncPG optimizadas para Lambda lifecycle
- ✅ Database branching workflow (main/staging/development/feature branches)
- ✅ Query optimization con indexes apropiados
- ✅ Connection pooling strategy para serverless
- ✅ Monitoring y observability para operaciones de BD
- ✅ Testing strategy con branches de testing

**Arquitectura**: Neon PostgreSQL como database-as-a-service con branching similar a Git para diferentes entornos.

### 3. `docker.md` - Docker Compose para Microservicios
**Enfoque**: Entorno de desarrollo local containerizado

**Contenido Principal**:
- ✅ Configuración Docker Compose para servicios independientes
- ✅ Contenedores separados por dominio (personal-info, experience, projects, skills)
- ✅ Simulación local de AWS Lambda Runtime con RIE
- ✅ PostgreSQL local simulando Neon para desarrollo
- ✅ SAM Local para API Gateway simulation
- ✅ Nginx como proxy para routing de microservicios
- ✅ Scripts de automatización (start-dev.sh, run-tests.sh, deploy-all.sh)
- ✅ Configuraciones específicas para desarrollo, testing y producción

**Arquitectura**: Microservicios containerizados con desarrollo local que replica la arquitectura de producción.

### 4. `frontend.md` - Astro v5 Complete Guide
**Enfoque**: Frontend moderno con las nuevas características de Astro v5

**Contenido Principal**:
- ✅ **Content Layer**: Carga de datos desde cualquier fuente con type-safety
- ✅ **Server Islands**: Mezcla de contenido estático y dinámico
- ✅ **Astro Actions**: Funciones backend type-safe desde el frontend
- ✅ Configuración TypeScript estricta obligatoria
- ✅ Integración completa con APIs Lambda via HTTP
- ✅ Optimizaciones de performance (imágenes, bundling, CSS)
- ✅ Testing con Vitest + Container API + Playwright
- ✅ Deployment a AWS CloudFront + S3 con configuración serverless

**Arquitectura**: SSG (Static Site Generation) con capacidades híbridas via Server Islands, consumiendo APIs serverless.

### 5. `testing.md` - Complete Testing & TDD Guide
**Enfoque**: Estrategia completa de testing con TDD

**Contenido Principal**:
- ✅ **Frontend Testing**: Vitest + Container API + Playwright + MSW
- ✅ **Backend Testing**: pytest + moto + LocalStack + SAM CLI
- ✅ **TDD Implementation**: Red-Green-Refactor cycle completo
- ✅ **Integration Testing**: Contract testing entre Astro y Lambda APIs
- ✅ **E2E Testing**: Workflows completos usuario final
- ✅ **API Mocking**: MSW para frontend, moto para AWS services
- ✅ **Local Testing**: SAM Local + LocalStack para development
- ✅ **CI/CD Pipeline**: Testing automatizado con coverage reporting

**Arquitectura**: Testing piramid completa con separación clara entre unit, integration y e2e testing.

---

## 🎯 Stack Tecnológico Completo

### Frontend
```typescript
- Astro v5 (SSG + Server Islands)
- TypeScript 5.3+ (strict mode obligatorio)
- Content Layer para data loading
- Astro Actions para backend functions
- Vitest + Playwright para testing
```

### Backend
```python
- AWS Lambda + FastAPI + Python 3.12
- Pydantic para validación tipo-safe
- AWS Lambda Powertools para observabilidad
- AsyncPG para conexiones PostgreSQL optimizadas
- pytest + moto para testing
```

### Database
```sql
- Neon PostgreSQL (serverless)
- Database branching (Git-like workflow)
- AsyncPG connection pooling
- Schema optimizado para portfolio data
```

### Infrastructure
```yaml
- AWS Lambda + API Gateway + SAM CLI
- Docker Compose para desarrollo local
- GitHub Actions para CI/CD
- AWS CloudFront + S3 para frontend deployment
```

### Testing
```yaml
- TDD Red-Green-Refactor obligatorio
- Frontend: Vitest + Container API + Playwright
- Backend: pytest + moto + LocalStack
- Integration: Contract testing + E2E workflows
```

---

## 🚀 Quick Start

1. **Leer documentación específica**:
   ```bash
   # ⚠️ OBLIGATORIO para IAs: Leer cada archivo individualmente
   cat docs/backend.md     # Backend FastAPI + Lambda
   cat docs/db.md          # Database Neon integration
   cat docs/docker.md      # Local development setup
   cat docs/frontend.md    # Astro v5 frontend
   cat docs/testing.md     # Testing & TDD strategies
   ```

2. **Setup desarrollo local**:
   ```bash
   # Frontend
   npm create astro@latest portfolio-astro
   cd portfolio-astro && npm install

   # Backend
   mkdir portfolio-backend && cd portfolio-backend
   python -m venv venv && source venv/bin/activate
   pip install fastapi mangum aws-lambda-powertools asyncpg

   # Database
   # Registrarse en neon.tech y obtener connection string

   # Docker
   docker-compose up --build -d
   ```

3. **Testing**:
   ```bash
   # Frontend tests
   npm run test
   npm run test:e2e

   # Backend tests
   pytest --cov=src --cov-report=html

   # Integration tests
   ./scripts/run-integration-tests.sh
   ```

---

## 📖 Orden de Lectura Recomendado

Para implementar el proyecto correctamente, se recomienda leer la documentación en este orden:

1. **`backend.md`** - Entender la arquitectura serverless base
2. **`db.md`** - Configurar la persistencia de datos
3. **`docker.md`** - Setup del entorno de desarrollo local
4. **`frontend.md`** - Implementar la interfaz con Astro v5
5. **`testing.md`** - Implementar la estrategia de testing completa

---

## ⚠️ Advertencias Importantes

### Para Desarrolladores Humanos:
- **TypeScript Strict Mode**: Obligatorio en todo el frontend
- **TDD**: Red-Green-Refactor cycle es mandatorio
- **Zero-tolerance**: Para errores de linting y tipos
- **API-First**: Diseño de contratos antes de implementación

### Para Inteligencias Artificiales:
- **DEBES leer cada archivo .md individual** para obtener información completa
- **NO asumas implementaciones** - cada archivo tiene detalles específicos
- **Respeta las convenciones** definidas en cada documento
- **Implementa TDD** siguiendo los patrones definidos en testing.md
- **Usa TypeScript estricto** como se especifica en frontend.md

---

## 📊 Métricas del Proyecto

- **Documentación**: 5 archivos técnicos (~15,000 líneas)
- **Cobertura esperada**: >80% en tests
- **Performance target**: Lighthouse score >90
- **Cold start optimizado**: ~300ms para Lambda
- **Type safety**: 100% TypeScript strict mode

---

## 🔗 Enlaces y Referencias

- [Astro v5 Official Docs](https://docs.astro.build/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [AWS Lambda Powertools](https://docs.powertools.aws.dev/lambda/python/)
- [Neon Database Docs](https://neon.tech/docs/)
- [Vitest Testing Framework](https://vitest.dev/)

---

**Fecha de creación**: Enero 2025
**Última actualización**: Enero 2025
**Versión de documentación**: 1.0.0
**Arquitectura**: Serverless Portfolio System with TDD

*Esta documentación representa un sistema completo de portfolio serverless implementado con las mejores prácticas de 2025, incluyendo TDD, TypeScript estricto, y arquitectura de microservicios.*