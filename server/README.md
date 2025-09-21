# Server - AWS Lambda Functions + SQLModel

Esta carpeta contiene toda la lógica del servidor organizada en microservicios Lambda, siguiendo las mejores prácticas de **FastAPI + SQLModel + AWS Lambda** para 2025.

## 🚀 Arquitectura FastAPI + SQLModel + Lambda - 2025

### ¿Por qué FastAPI + SQLModel + Lambda?
- 🚀 **Performance**: Cold starts optimizados ~300ms con SQLModel
- 🔒 **Type Safety**: SQLModel = SQLAlchemy + Pydantic en un solo modelo
- 📚 **API Docs**: OpenAPI/Swagger generado automáticamente
- ⚡ **Async**: Soporte nativo para operaciones asíncronas con AsyncSession
- 🔧 **Lambda Integration**: Mangum adapter optimizado
- 📦 **Size**: Footprint pequeño para microservicios
- 🎯 **SQLModel Benefits**: Triple funcionalidad - Table, Pydantic Model, SQLAlchemy Model
- 🧩 **Zero Duplication**: Elimina duplicación entre modelos y schemas

## 🏗️ Estructura del Servidor

```
server/
└── lambda/                         # AWS Lambda Functions (FastAPI + SQLModel + Mangum)
    ├── personal-info/             # Información personal API
    │   ├── setup/                 # Configuración y deployment
    │   │   ├── .env              # Variables de entorno locales
    │   │   ├── Dockerfile        # Container para desarrollo
    │   │   └── requirements.txt  # FastAPI + SQLModel dependencies
    │   └── src/                  # Código fuente de la función
    │       ├── lambda_function.py   # Lambda handler con Mangum
    │       ├── main.py             # FastAPI app principal
    │       ├── models.py           # SQLModel models (Table + Pydantic)
    │       └── repository.py       # Data access layer con SQLModel
    ├── skills/                   # Gestión de habilidades API
    │   ├── setup/               # [misma estructura setup/]
    │   └── src/                 # [misma estructura src/]
    ├── experience/              # Experiencia profesional API
    │   ├── setup/               # [misma estructura setup/]
    │   └── src/                 # [misma estructura src/]
    └── projects/                # Portfolio de proyectos API
        ├── setup/               # [misma estructura setup/]
        └── src/                 # [misma estructura src/]
```

## 🎯 FastAPI + SQLModel Lambda Implementation Patterns

### 1. Lambda Handler con Mangum + SQLModel (Patrón 2025)

Cada función Lambda sigue este patrón optimizado con SQLModel:

```python
# lambda_function.py - Entry point optimizado con SQLModel
from fastapi import FastAPI
from mangum import Mangum
from aws_lambda_powertools import Logger, Tracer, Metrics
from functools import lru_cache
from contextlib import asynccontextmanager

# Import FastAPI app with SQLModel
from app.main import app
from app.database import close_db_connections

# AWS Lambda Powertools
logger = Logger()
tracer = Tracer()
metrics = Metrics()

# Cache Mangum handler (Optimización Cold Start)
@lru_cache(maxsize=1)
def create_handler():
    """Create cached Mangum handler for SQLModel app."""
    return Mangum(
        app,
        lifespan="off",  # Disable lifespan for Lambda
        api_gateway_base_path="/prod"
    )

# Initialize handler at module level
handler = create_handler()

def lambda_handler(event, context):
    """
    AWS Lambda entry point optimizado con SQLModel y observabilidad.

    Args:
        event: API Gateway event
        context: Lambda context
    Returns:
        HTTP response for API Gateway
    """
    # Log request details
    logger.info(
        "SQLModel Lambda invocation started",
        extra={
            "request_id": context.aws_request_id,
            "function_name": context.function_name,
            "event_path": event.get("path", "unknown"),
            "http_method": event.get("httpMethod", "unknown")
        }
    )

    # Add custom metrics
    metrics.add_metric(name="SQLModelLambdaInvocation", unit="Count", value=1)

    try:
        response = handler(event, context)

        # Add success metric
        metrics.add_metric(name="SuccessfulRequests", unit="Count", value=1)

        # Close DB connections if Lambda is about to timeout
        if context.get_remaining_time_in_millis() < 1000:
            import asyncio
            asyncio.run(close_db_connections())

        return response

    except Exception as e:
        logger.error(f"SQLModel Lambda invocation failed: {str(e)}", exc_info=True)
        metrics.add_metric(name="FailedRequests", unit="Count", value=1)

        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": '{"error": "Internal server error"}'
        }
```

### 2. FastAPI Application Structure con SQLModel

```python
# app/main.py - FastAPI application con SQLModel
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from aws_lambda_powertools import Logger, Tracer, Metrics
from datetime import datetime
import os

from .models import HealthResponse
from .database import create_db_and_tables, close_db_connections
from .routers import personal, experience, projects, skills

# AWS Lambda Powertools
logger = Logger()
tracer = Tracer()
metrics = Metrics()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestión del ciclo de vida de SQLModel en Lambda.

    Note: En Lambda, esto se ejecuta en la primera invocación.
    """
    # Startup - crear tablas si no existen
    logger.info("SQLModel startup: Creating database tables")
    await create_db_and_tables()
    yield
    # Shutdown - cerrar conexiones
    logger.info("SQLModel shutdown: Closing database connections")
    await close_db_connections()

# FastAPI app configuration con SQLModel
app = FastAPI(
    title="Portfolio API with SQLModel",
    description="FastAPI + SQLModel + Lambda server for modern portfolio system",
    version="1.0.0",
    docs_url="/docs" if os.getenv("ENVIRONMENT") == "dev" else None,
    redoc_url="/redoc" if os.getenv("ENVIRONMENT") == "dev" else None,
    lifespan=lifespan  # SQLModel lifecycle management
)

# CORS middleware for Astro frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with SQLModel
app.include_router(personal.router, prefix="/api/v1", tags=["personal"])
app.include_router(experience.router, prefix="/api/v1", tags=["experience"])
app.include_router(projects.router, prefix="/api/v1", tags=["projects"])
app.include_router(skills.router, prefix="/api/v1", tags=["skills"])

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for SQLModel Lambda function."""
    return HealthResponse(
        status="healthy",
        service="portfolio-sqlmodel-api",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
        database="SQLModel + AsyncPG"
    )
```

### 3. SQLModel Models - Triple Funcionalidad (Table + Pydantic + SQLAlchemy)

```python
# app/models.py - SQLModel models con triple funcionalidad
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr, HttpUrl
from typing import List, Optional
from datetime import datetime, date

# Base models para esquemas compartidos
class PersonalInfoBase(SQLModel):
    """Base schema para PersonalInfo - compartido entre entrada y salida."""
    name: str = Field(index=True, max_length=100)
    title: str = Field(max_length=150)
    email: EmailStr = Field(unique=True, index=True)
    phone: Optional[str] = Field(default=None, max_length=20)
    location: Optional[str] = Field(default=None, max_length=100)
    linkedin: Optional[HttpUrl] = None
    github: Optional[HttpUrl] = None
    summary: Optional[str] = Field(default=None, max_length=1000)

# SQLModel que funciona como tabla Y como schema de API
class PersonalInfo(PersonalInfoBase, table=True):
    """
    Modelo SQLModel para información personal.

    Triple funcionalidad:
    - SQLAlchemy Table: Define la tabla en la BD
    - Pydantic Model: Validación automática de datos
    - API Schema: Usado directamente en FastAPI responses

    :Authors:
        - Pablo Contreras

    :Created:
        - 2025/09/20
    """
    __tablename__ = "personal_info"

    id: Optional[int] = Field(default=None, primary_key=True)
    is_active: bool = Field(default=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)

# Schemas para API requests/responses específicos
class PersonalInfoCreate(PersonalInfoBase):
    """Schema para crear información personal."""
    pass

class PersonalInfoUpdate(SQLModel):
    """Schema para actualizar información personal."""
    name: Optional[str] = Field(default=None, max_length=100)
    title: Optional[str] = Field(default=None, max_length=150)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, max_length=20)
    location: Optional[str] = Field(default=None, max_length=100)
    linkedin: Optional[HttpUrl] = None
    github: Optional[HttpUrl] = None
    summary: Optional[str] = Field(default=None, max_length=1000)

class PersonalInfoPublic(PersonalInfoBase):
    """Schema público para respuestas API (sin campos internos)."""
    id: int
    created_at: datetime

# Modelo de Skills con SQLModel
class SkillBase(SQLModel):
    """Base schema para Skills."""
    name: str = Field(index=True, max_length=100)
    category: str = Field(index=True, max_length=50)
    level: int = Field(ge=1, le=5, description="Skill level from 1 to 5")
    years_experience: Optional[int] = Field(default=None, ge=0)

class Skill(SkillBase, table=True):
    """SQLModel para habilidades técnicas."""
    __tablename__ = "skills"

    id: Optional[int] = Field(default=None, primary_key=True)
    description: Optional[str] = Field(default=None, max_length=500)
    is_featured: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Health Response (solo Pydantic - no necesita tabla)
class HealthResponse(SQLModel):
    """Health check response model."""
    status: str
    service: str
    timestamp: str
    version: str
    database: Optional[str] = None
```

### 4. SQLModel Database Connection Optimizada para Lambda

```python
# app/database.py - SQLModel + AsyncSession optimizado para Lambda
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from typing import Optional, AsyncGenerator, Annotated
from fastapi import Depends
from aws_lambda_powertools import Logger
import os

logger = Logger()

# Database URL configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/portfolio")

# Async engine optimizado para Lambda
async_engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL debugging
    pool_size=3,        # Low for Lambda memory limits
    max_overflow=0,     # No overflow connections
    pool_pre_ping=True, # Verify connections before use
    pool_recycle=300,   # Recycle connections every 5 minutes
    pool_timeout=30,    # Timeout for getting connection
)

# Session factory optimizada para Lambda
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Important for Lambda
    autoflush=False,
    autocommit=False
)

class LambdaOptimizedDatabase:
    """
    SQLModel database manager optimizado para AWS Lambda.

    Singleton pattern para reutilizar conexiones entre invocaciones.

    :Authors:
        - Pablo Contreras

    :Created:
        - 2025/09/20
    """
    _engine: Optional[AsyncSession] = None

    @classmethod
    async def get_engine(cls):
        """Get or create async engine (singleton para Lambda)."""
        if cls._engine is None:
            cls._engine = async_engine
        return cls._engine

    @classmethod
    async def get_session(cls) -> AsyncSession:
        """Get SQLModel session optimizada para Lambda."""
        engine = await cls.get_engine()
        return AsyncSessionLocal()

    @classmethod
    async def close_connections(cls):
        """Close connections (llamar en cleanup de Lambda)."""
        if cls._engine:
            await cls._engine.dispose()
            cls._engine = None

# FastAPI dependency para SQLModel AsyncSession
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency para obtener SQLModel AsyncSession.

    Yields:
        AsyncSession: SQLModel async session para operaciones de BD
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Type annotation para dependency injection
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

async def create_db_and_tables():
    """Crear todas las tablas SQLModel en la base de datos."""
    async with async_engine.begin() as conn:
        # Import all models to ensure they're registered
        from .models import PersonalInfo, Skill

        # Create all tables
        await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("SQLModel tables created successfully")

async def close_db_connections():
    """Cerrar todas las conexiones de base de datos."""
    await async_engine.dispose()
    logger.info("SQLModel database connections closed")
```

### 5. SQLModel API Routes Implementation

```python
# app/routers/personal.py - API routes con SQLModel + AsyncSession
from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import select
from aws_lambda_powertools import Logger
from typing import Optional, List

from ..models import (
    PersonalInfo,
    PersonalInfoCreate,
    PersonalInfoUpdate,
    PersonalInfoPublic
)
from ..database import SessionDep
from ..services.personal_service import PersonalInfoService

router = APIRouter()
logger = Logger()

@router.get("/personal-info", response_model=PersonalInfoPublic)
async def get_personal_info(session: SessionDep):
    """
    Get active personal information using SQLModel.

    Returns:
        PersonalInfoPublic: Public personal information data
    """
    try:
        # Use SQLModel select syntax
        statement = select(PersonalInfo).where(
            PersonalInfo.is_active == True
        ).order_by(PersonalInfo.updated_at.desc())

        result = await session.exec(statement)
        personal_info = result.first()

        if not personal_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Personal info not found"
            )

        return PersonalInfoPublic.model_validate(personal_info)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting personal info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/personal-info", response_model=PersonalInfoPublic)
async def create_personal_info(
    personal_data: PersonalInfoCreate,
    session: SessionDep
):
    """Create new personal information using SQLModel."""
    try:
        # Deactivate existing personal info
        statement = select(PersonalInfo).where(PersonalInfo.is_active == True)
        result = await session.exec(statement)
        existing_info = result.all()

        for info in existing_info:
            info.is_active = False
            session.add(info)

        # Create new personal info
        db_personal_info = PersonalInfo.model_validate(personal_data)
        db_personal_info.is_active = True

        session.add(db_personal_info)
        await session.commit()
        await session.refresh(db_personal_info)

        return PersonalInfoPublic.model_validate(db_personal_info)

    except Exception as e:
        await session.rollback()
        logger.error(f"Error creating personal info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating personal information"
        )

@router.patch("/personal-info/{info_id}", response_model=PersonalInfoPublic)
async def update_personal_info(
    info_id: int,
    update_data: PersonalInfoUpdate,
    session: SessionDep
):
    """Update personal information using SQLModel."""
    try:
        # Get existing personal info
        statement = select(PersonalInfo).where(PersonalInfo.id == info_id)
        result = await session.exec(statement)
        personal_info = result.first()

        if not personal_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Personal info not found"
            )

        # Update only provided fields
        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(personal_info, field, value)

        # Update timestamp
        from datetime import datetime
        personal_info.updated_at = datetime.utcnow()

        session.add(personal_info)
        await session.commit()
        await session.refresh(personal_info)

        return PersonalInfoPublic.model_validate(personal_info)

    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        logger.error(f"Error updating personal info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating personal information"
        )

# Service Layer Pattern con SQLModel
@router.get("/personal-info/service", response_model=PersonalInfoPublic)
async def get_personal_info_with_service(session: SessionDep):
    """Get personal info using service layer pattern."""
    service = PersonalInfoService(session)
    personal_info = await service.get_active_personal_info()

    if not personal_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personal info not found"
        )

    return PersonalInfoPublic.model_validate(personal_info)
```

## 📦 Dependencies & Requirements

### Core FastAPI Lambda Stack

```txt
# requirements.txt - FastAPI Lambda dependencies
fastapi==0.104.1
mangum==0.17.0
pydantic[email]==2.5.0
asyncpg==0.29.0
aws-lambda-powertools[all]==2.28.0
python-multipart==0.0.6

# Development dependencies
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.25.2
black==23.11.0
ruff==0.1.6
mypy==1.7.1
```

## 🎯 Convenciones de Nomenclatura

### Para Lambda Functions (`server/lambda/`)
- **Nombres cortos y descriptivos**: `personal-info`, `skills`, `projects`, `experience`
- **NO usar sufijo "-lambda"**: Ya está implícito por estar en la carpeta `lambda/`
- **Usar guiones para separar palabras**: `personal-info` en lugar de `personal_info`
- **Funciones específicas por dominio**: Cada función maneja un área específica del negocio

#### Ejemplos ✅ Correctos:
```
server/lambda/personal-info/    # ✅ Información personal
server/lambda/skills/          # ✅ Gestión de habilidades
server/lambda/projects/        # ✅ Portfolio de proyectos
server/lambda/experience/      # ✅ Experiencia laboral
```

#### Ejemplos ❌ Incorrectos:
```
server/lambda/personal-info-lambda/  # ❌ Redundante
server/lambda/personalInfo/          # ❌ camelCase no recomendado
server/lambda/personal_info/         # ❌ snake_case en carpetas
```


## 📁 Estructura Estándar de FastAPI Lambda Function

Cada función Lambda sigue esta estructura estándar con separación setup/src:

```
server/lambda/[nombre-funcion]/
├── setup/                      # Configuración y deployment
│   ├── .env                   # Variables de entorno para desarrollo local
│   ├── Dockerfile             # Container para desarrollo local
│   └── requirements.txt       # FastAPI + SQLModel dependencies
└── src/                       # Código fuente de la función
    ├── lambda_function.py     # Entry point con Mangum handler
    ├── main.py                # FastAPI app principal
    ├── models.py              # SQLModel models (Table + Pydantic)
    └── repository.py          # Data access layer con SQLModel
```

### Archivos de Configuración en `setup/`:

#### `.env` - Variables de entorno locales
```bash
# Database connection
DATABASE_URL=postgresql://postgres:password@localhost:5432/portfolio_db
DB_HOST=localhost
DB_PORT=5432
DB_NAME=portfolio_db
DB_USER=postgres
DB_PASSWORD=password

# FastAPI configuration
FASTAPI_DEBUG=true
LOG_LEVEL=debug

# AWS Lambda configuration (for local testing)
AWS_LAMBDA_FUNCTION_NAME=service-name
AWS_REGION=us-east-1

# CORS configuration
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:4321"]
```



## 🚀 Desarrollo Local

### Estructura de Desarrollo con setup/ y src/

Cada función Lambda tiene ahora una estructura clara:
- **`setup/`**: Contiene toda la configuración (Docker, requirements, env, layers)
- **`src/`**: Contiene únicamente el código fuente de la función

### Construir todas las funciones FastAPI:
```bash
# Desde la raíz del proyecto - construir toda la infraestructura
python scripts/run.py setup --action=up --services=server --env=local --verbose

# Con Docker Compose (usando archivos setup/)
docker-compose -f server/setup/docker-compose.yml up --build -d
```

### Construir función específica:
```bash
# Solo personal-info (usando su setup/Dockerfile)
cd server/lambda/personal-info
docker build -f setup/Dockerfile -t personal-info-lambda .

# Solo skills (usando su setup/Dockerfile)
cd server/lambda/skills
docker build -f setup/Dockerfile -t skills-lambda .
```


### Acceder a documentación FastAPI (desarrollo):
```bash
# Swagger UI (FastAPI docs automáticas)
http://localhost:8001/docs    # personal-info function
http://localhost:8002/docs    # skills function

# ReDoc (documentación alternativa)
http://localhost:8001/redoc   # personal-info function
http://localhost:8002/redoc   # skills function

# Health check endpoints
http://localhost:8001/health  # personal-info health
http://localhost:8002/health  # skills health
```

## 🧪 Testing con TDD - Red-Green-Refactor

### FastAPI Testing Stack
- **pytest**: Test framework con async support
- **pytest-asyncio**: Async test support
- **httpx**: Async HTTP client para API testing
- **moto**: AWS services mocking
- **pytest-cov**: Coverage reporting

### TDD Pattern Implementation

```python
# tests/test_personal_routes.py - TDD con FastAPI
import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
from app.main import app

class TestPersonalInfoRoutes:
    """TDD tests para personal info routes."""

    @pytest.mark.asyncio
    async def test_red_personal_info_no_data(self):
        """RED: Test should fail when no personal info exists."""
        with patch('app.database.OptimizedDatabase.execute_one', return_value=None):
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get("/api/personal-info")

        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["error"]

    @pytest.mark.asyncio
    async def test_green_personal_info_basic_data(self):
        """GREEN: Basic personal info retrieval."""
        mock_data = {
            "name": "Pablo Contreras",
            "title": "Python Developer",
            "email": "pablo@bypabloc.dev",
            "phone": None,
            "location": None,
            "linkedin": None,
            "github": None,
            "summary": None
        }

        with patch('app.database.OptimizedDatabase.execute_one', return_value=mock_data):
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get("/api/personal-info")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Pablo Contreras"
        assert data["email"] == "pablo@bypabloc.dev"

    @pytest.mark.asyncio
    async def test_refactor_personal_info_validation(self):
        """REFACTOR: Personal info with Pydantic validation."""
        mock_data = {
            "name": "Pablo Contreras",
            "title": "Python Developer",
            "email": "pablo@bypabloc.dev",
            "phone": "+1234567890",
            "location": "Santiago, Chile",
            "linkedin": "https://linkedin.com/in/bypabloc",
            "github": "https://github.com/bypabloc",
            "summary": "Expert Python developer specializing in serverless"
        }

        with patch('app.database.OptimizedDatabase.execute_one', return_value=mock_data):
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get("/api/personal-info")

        assert response.status_code == 200
        data = response.json()

        # Verify Pydantic validation and proper types
        assert data["name"] == "Pablo Contreras"
        assert data["email"] == "pablo@bypabloc.dev"
        assert data["linkedin"] == "https://linkedin.com/in/bypabloc"
        assert len(data["summary"]) > 10  # Has meaningful content
```

### Ejecutar tests:
```bash
# Tests unitarios con coverage
cd server/lambda/personal-info
python -m pytest tests/ -v --cov=app --cov-report=term

# Tests específicos (TDD)
python -m pytest tests/test_personal_routes.py::TestPersonalInfoRoutes::test_red_personal_info_no_data -v

# Tests de integración Lambda
python -m pytest tests/test_lambda_integration.py -v

# All tests con coverage report HTML
python -m pytest tests/ --cov=app --cov-report=html
```

## 🗄️ Integración con Base de Datos

Las funciones Lambda integran directamente con la base de datos usando SQLModel y AsyncPG:

```python
# Integración directa en FastAPI routes
from sqlmodel import select
from .models import PersonalInfo
from .database import SessionDep

# En routes
@router.get("/personal-info")
async def get_personal_info(session: SessionDep):
    statement = select(PersonalInfo).where(PersonalInfo.is_active == True)
    result = await session.exec(statement)
    personal_info = result.first()

    return personal_info if personal_info else None
```

## 🎯 Performance Optimizations (2025)

### 1. Cold Start Optimization
- **Cached handlers**: `@lru_cache` para Mangum handler
- **Module-level initialization**: Handler inicializado fuera de la función
- **Connection pooling**: AsyncPG pool reutilizado entre invocaciones
- **JIT disabled**: PostgreSQL JIT desactivado para conexiones rápidas

### 2. Response Caching
```python
from functools import lru_cache
import hashlib

class ResponseCache:
    """In-memory response cache para Lambda."""
    _cache: Dict[str, Any] = {}

    @classmethod
    def get_cache_key(cls, path: str, query_params: Dict = None) -> str:
        content = f"{path}:{json.dumps(query_params or {}, sort_keys=True)}"
        return hashlib.md5(content.encode()).hexdigest()

    @classmethod
    def get(cls, key: str) -> Optional[Any]:
        return cls._cache.get(key)

    @classmethod
    def set(cls, key: str, value: Any, ttl: int = 300):
        cls._cache[key] = value
        # Keep cache size manageable
        if len(cls._cache) > 100:
            old_keys = list(cls._cache.keys())[:20]
            for old_key in old_keys:
                del cls._cache[old_key]
```

## 🌐 Integración con Astro Frontend

### Astro Content Layer + FastAPI
```typescript
// src/lib/api-client.ts - Cliente optimizado para FastAPI
class PortfolioApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl.replace(/\/$/, '');
  }

  private async request<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      headers: { 'Content-Type': 'application/json' },
      signal: AbortSignal.timeout(10000), // Timeout para build-time
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.status}`);
    }

    return response.json();
  }

  async getPersonalInfo() {
    return this.request<PersonalInfo>('/api/personal-info');
  }

  async getSkills() {
    return this.request<Skill[]>('/api/skills');
  }
}

export const apiClient = new PortfolioApiClient(
  import.meta.env.PUBLIC_API_URL || 'https://api.portfolio.com'
);
```

## 📋 Checklist para Nueva FastAPI Lambda Function (Estructura 2025)

### Estructura setup/ (Configuración)
- [ ] Crear carpeta `setup/` con archivos de configuración
- [ ] Crear `setup/.env` con variables de entorno de desarrollo
- [ ] Configurar `setup/Dockerfile` para desarrollo local
- [ ] Definir `setup/requirements.txt` con FastAPI + SQLModel dependencies
- [ ] Configurar `setup/layers.yml` con dependencias de capas AWS

### Estructura src/ (Código fuente)
- [ ] Crear carpeta `src/` con código fuente de la función
- [ ] Implementar `src/lambda_function.py` con Mangum handler
- [ ] Configurar `src/main.py` con FastAPI app
- [ ] Definir modelos SQLModel en `src/models.py` (Table + Pydantic)
- [ ] Implementar repository pattern en `src/repository.py`

### Integración y Testing
- [ ] Configurar CORS para integración con frontend Astro
- [ ] Verificar documentación OpenAPI en `/docs`
- [ ] Implementar TDD tests con pytest + httpx
- [ ] Probar con scripts de setup Docker

### Ejemplo de Estructura Completa
```
server/lambda/nueva-funcion/
├── setup/
│   ├── .env                    # Variables desarrollo local
│   ├── Dockerfile              # Container desarrollo
│   ├── layers.yml              # Configuración capas AWS
│   └── requirements.txt        # Dependencies FastAPI + SQLModel
└── src/
    ├── lambda_function.py      # Entry point con Mangum
    ├── main.py                 # FastAPI app principal
    ├── models.py               # SQLModel models
    └── repository.py           # Data access layer
```


## 🌟 Ventajas de la Nueva Estructura Estándar (2025)

### 📁 Separación Clara setup/ vs src/
- **Configuración aislada**: Todo en `setup/` - Docker, env vars, dependencies
- **Código limpio**: Solo lógica de negocio en `src/`
- **Deployment simplificado**: Configuración separada facilita CI/CD
- **Desarrollo local**: Environment vars y Docker centralizados

### 🔄 Beneficios para Desarrollo en Equipo
- **Estructura consistente**: Todas las lambdas siguen el mismo patrón
- **Onboarding rápido**: Nuevos desarrolladores encuentran todo en su lugar
- **Debugging facilitado**: Configuración vs código claramente separados
- **Mantenimiento**: Cambios de configuración no afectan código fuente

### 🚀 Performance Benefits (FastAPI + SQLModel + Lambda)
- **Cold starts optimizados**: ~300ms para serverless con SQLModel
- **Async/await nativo**: Para operaciones I/O intensivas
- **Connection pooling**: Optimizado para Lambda lifecycle
- **Response caching**: Para datos que cambian poco
- **SQLModel triple benefit**: Table + Pydantic + SQLAlchemy en uno

### 🔒 Type Safety Benefits
- **SQLModel validation**: Automática en requests/responses + database
- **Type hints end-to-end**: Desde database hasta API con SQLModel
- **Auto-generated OpenAPI**: Con validación completa
- **Runtime validation**: Con error messages claros
- **Zero duplication**: Un modelo para tabla, API schema y validación

### 📚 Developer Experience Benefits
- **OpenAPI/Swagger docs**: Generados automáticamente
- **Interactive API testing**: Con Swagger UI integrado
- **Modern Python syntax**: Con decorators y type hints
- **Excellent debugging**: Con detailed error messages
- **Standardized structure**: Predecible ubicación de archivos

### 🔧 Lambda Integration Benefits
- **Mangum adapter**: Optimizado para AWS Lambda
- **AWS Lambda Powertools**: Integration nativa
- **CloudWatch logging**: Automatizado con structured logs
- **API Gateway integration**: Seamless con CORS y auth
- **Direct database integration**: SQLModel con AsyncPG para máximo rendimiento

---

**FastAPI + Lambda es la combinación ideal para APIs modernas serverless que requieren performance, type safety y developer experience optimizados para 2025.**