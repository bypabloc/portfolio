# FastAPI + AWS Lambda Backend Development Guide - 2025

> **Comprehensive guide for building modern, serverless backends using FastAPI + AWS Lambda that integrate perfectly with Astro frontends and Neon PostgreSQL databases.**

## 🚀 Executive Summary

The backend landscape in 2025 has converged on **FastAPI + AWS Lambda** as the optimal architecture for serverless APIs. This guide covers the complete implementation of FastAPI-based Lambda functions that serve as powerful backend APIs for modern frontend frameworks like Astro.

### Why FastAPI + Lambda in 2025

- 🚀 **Performance**: Cold starts optimizados ~300ms
- 🔒 **Type Safety**: Pydantic validation automática
- 📚 **API Docs**: OpenAPI/Swagger generado automáticamente
- ⚡ **Async**: Soporte nativo para operaciones asíncronas
- 🔧 **Lambda Integration**: Mangum adapter optimizado
- 📦 **Size**: Footprint pequeño para Lambda layers
- 🎯 **Modern**: Syntax moderna con type hints
- 🔍 **Debugging**: Mejor error handling y logging

---

## 📋 FastAPI + Lambda Architecture Overview

### 🏆 **FastAPI + Lambda - The Ideal Combination**

| Characteristic | FastAPI + Lambda | Advantage |
|----------------|------------------|-----------|
| **Cold Start** | ~300ms | Optimized for serverless |
| **Type Safety** | ✅ Native | Pydantic integration |
| **API Docs** | ✅ Auto-generated | OpenAPI/Swagger built-in |
| **Async Support** | ✅ Native | Full async/await support |
| **Lambda Size** | ~15MB | Optimized for serverless |
| **Developer Experience** | ✅ Excellent | Modern Python syntax |

---

## 🎯 FastAPI + Lambda Complete Setup

### 1. Project Structure and Installation

**Installation & Dependencies:**
```bash
mkdir portfolio-fastapi-lambda
cd portfolio-fastapi-lambda
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Core dependencies
pip install fastapi mangum pydantic asyncpg python-multipart
pip install aws-lambda-powertools[all]

# Development dependencies
pip install pytest pytest-asyncio pytest-cov black ruff mypy
```

**Project Structure:**
```
portfolio-fastapi-lambda/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── models.py            # Pydantic models
│   ├── database.py          # Database connection
│   ├── routers/             # API routes
│   │   ├── __init__.py
│   │   ├── personal.py
│   │   ├── experience.py
│   │   ├── projects.py
│   │   └── skills.py
│   └── services/            # Business logic
│       ├── __init__.py
│       └── cv_service.py
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── test_routes.py
├── lambda_handler.py        # AWS Lambda entry point
├── requirements.txt
├── template.yaml           # SAM template
└── Dockerfile             # For local development
```

### 2. Core FastAPI Application

**app/main.py - FastAPI Application:**
```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.middleware_factory import lambda_handler_decorator
import os
from typing import List, Optional
from datetime import datetime

from .models import PersonalInfo, Experience, Project, Skill, HealthResponse
from .database import get_database
from .routers import personal, experience, projects, skills

# AWS Lambda Powertools
logger = Logger()
tracer = Tracer()
metrics = Metrics()

# FastAPI app configuration
app = FastAPI(
    title="Portfolio API",
    description="FastAPI + Lambda backend for modern portfolio system",
    version="1.0.0",
    docs_url="/docs" if os.getenv("ENVIRONMENT") == "dev" else None,
    redoc_url="/redoc" if os.getenv("ENVIRONMENT") == "dev" else None,
    openapi_url="/openapi.json" if os.getenv("ENVIRONMENT") == "dev" else None
)

# CORS middleware for Astro frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(personal.router, prefix="/api", tags=["personal"])
app.include_router(experience.router, prefix="/api", tags=["experience"])
app.include_router(projects.router, prefix="/api", tags=["projects"])
app.include_router(skills.router, prefix="/api", tags=["skills"])

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for Lambda function."""
    return HealthResponse(
        status="healthy",
        service="portfolio-api",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0"
    )

# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP Exception: {exc.detail}", extra={"status_code": exc.status_code})
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "timestamp": datetime.utcnow().isoformat()
        }
    )
```

### 3. Pydantic Models for Type Safety

**app/models.py - Pydantic Models:**
```python
from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List, Optional
from datetime import date, datetime

class PersonalInfo(BaseModel):
    """Personal information model with validation."""
    name: str
    title: str
    email: EmailStr
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[HttpUrl] = None
    github: Optional[HttpUrl] = None
    summary: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat()
        }

class Experience(BaseModel):
    """Work experience model."""
    id: Optional[int] = None
    company: str
    position: str
    start_date: date
    end_date: Optional[date] = None
    description: Optional[str] = None
    location: Optional[str] = None
    technologies: List[str] = []

    class Config:
        json_encoders = {
            date: lambda v: v.isoformat()
        }

class Project(BaseModel):
    """Project model."""
    id: Optional[int] = None
    name: str
    description: str
    technologies: List[str] = []
    github_url: Optional[HttpUrl] = None
    demo_url: Optional[HttpUrl] = None
    featured: bool = False
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class Skill(BaseModel):
    """Skill model."""
    id: Optional[int] = None
    name: str
    category: str
    level: int  # 1-5 scale
    years_experience: Optional[int] = None

class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    service: str
    timestamp: str
    version: str

# Request models
class PersonalInfoUpdate(BaseModel):
    """Model for updating personal information."""
    name: Optional[str] = None
    title: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None

class ExperienceCreate(BaseModel):
    """Model for creating new experience."""
    company: str
    position: str
    start_date: date
    end_date: Optional[date] = None
    description: Optional[str] = None
    location: Optional[str] = None
    technologies: List[str] = []
```

### 4. Database Connection with AsyncPG

**app/database.py - Async Database Connection:**
```python
import asyncpg
import os
from typing import Optional
from aws_lambda_powertools import Logger
import json

logger = Logger()

class Database:
    """Async database connection manager optimized for Lambda."""

    def __init__(self):
        self.connection_string = os.getenv("DATABASE_URL")
        if not self.connection_string:
            raise ValueError("DATABASE_URL environment variable is required")

    async def get_connection(self):
        """Get optimized database connection for Lambda."""
        try:
            connection = await asyncpg.connect(
                self.connection_string,
                command_timeout=30,
                server_settings={
                    'application_name': 'portfolio-api-lambda',
                    'jit': 'off'  # Disable JIT for faster connection
                }
            )
            return connection
        except Exception as e:
            logger.error(f"Database connection error: {str(e)}")
            raise

    async def execute_query(self, query: str, *args):
        """Execute query with error handling."""
        async with await self.get_connection() as conn:
            try:
                result = await conn.fetch(query, *args)
                return [dict(row) for row in result]
            except Exception as e:
                logger.error(f"Query execution error: {str(e)}", extra={"query": query})
                raise

    async def execute_one(self, query: str, *args):
        """Execute query returning single row."""
        async with await self.get_connection() as conn:
            try:
                result = await conn.fetchrow(query, *args)
                return dict(result) if result else None
            except Exception as e:
                logger.error(f"Query execution error: {str(e)}", extra={"query": query})
                raise

# Dependency for FastAPI
async def get_database():
    """FastAPI dependency for database connection."""
    return Database()
```

### 5. API Routes Implementation

**app/routers/personal.py - Personal Info Routes:**
```python
from fastapi import APIRouter, HTTPException, Depends
from aws_lambda_powertools import Logger
from typing import Optional

from ..models import PersonalInfo, PersonalInfoUpdate
from ..database import get_database, Database

router = APIRouter()
logger = Logger()

@router.get("/personal-info", response_model=PersonalInfo)
async def get_personal_info(db: Database = Depends(get_database)):
    """Get personal information."""
    try:
        result = await db.execute_one("""
            SELECT name, title, email, phone, location, linkedin, github, summary
            FROM personal_info
            WHERE active = true
            ORDER BY updated_at DESC
            LIMIT 1
        """)

        if not result:
            raise HTTPException(status_code=404, detail="Personal info not found")

        return PersonalInfo(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting personal info: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/personal-info", response_model=PersonalInfo)
async def update_personal_info(
    update_data: PersonalInfoUpdate,
    db: Database = Depends(get_database)
):
    """Update personal information."""
    try:
        # Build dynamic update query
        update_fields = []
        values = []
        field_map = {
            "name": update_data.name,
            "title": update_data.title,
            "phone": update_data.phone,
            "location": update_data.location,
            "summary": update_data.summary
        }

        for field, value in field_map.items():
            if value is not None:
                update_fields.append(f"{field} = ${len(values) + 1}")
                values.append(value)

        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")

        query = f"""
            UPDATE personal_info
            SET {', '.join(update_fields)}, updated_at = NOW()
            WHERE active = true
            RETURNING name, title, email, phone, location, linkedin, github, summary
        """

        result = await db.execute_one(query, *values)

        if not result:
            raise HTTPException(status_code=404, detail="Personal info not found")

        return PersonalInfo(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating personal info: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

**app/routers/experience.py - Experience Routes:**
```python
from fastapi import APIRouter, HTTPException, Depends
from aws_lambda_powertools import Logger
from typing import List, Optional

from ..models import Experience, ExperienceCreate
from ..database import get_database, Database

router = APIRouter()
logger = Logger()

@router.get("/experience", response_model=List[Experience])
async def get_experience(db: Database = Depends(get_database)):
    """Get all work experience."""
    try:
        results = await db.execute_query("""
            SELECT
                e.id, e.company, e.position, e.start_date, e.end_date,
                e.description, e.location,
                COALESCE(
                    array_agg(t.name ORDER BY t.name) FILTER (WHERE t.name IS NOT NULL),
                    '{}'
                ) as technologies
            FROM experience e
            LEFT JOIN experience_technologies et ON e.id = et.experience_id
            LEFT JOIN technologies t ON et.technology_id = t.id
            WHERE e.active = true
            GROUP BY e.id, e.company, e.position, e.start_date, e.end_date, e.description, e.location
            ORDER BY e.start_date DESC
        """)

        return [Experience(**result) for result in results]
    except Exception as e:
        logger.error(f"Error getting experience: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/experience/{experience_id}", response_model=Experience)
async def get_experience_by_id(
    experience_id: int,
    db: Database = Depends(get_database)
):
    """Get specific work experience by ID."""
    try:
        result = await db.execute_one("""
            SELECT
                e.id, e.company, e.position, e.start_date, e.end_date,
                e.description, e.location,
                COALESCE(
                    array_agg(t.name ORDER BY t.name) FILTER (WHERE t.name IS NOT NULL),
                    '{}'
                ) as technologies
            FROM experience e
            LEFT JOIN experience_technologies et ON e.id = et.experience_id
            LEFT JOIN technologies t ON et.technology_id = t.id
            WHERE e.id = $1 AND e.active = true
            GROUP BY e.id, e.company, e.position, e.start_date, e.end_date, e.description, e.location
        """, experience_id)

        if not result:
            raise HTTPException(status_code=404, detail="Experience not found")

        return Experience(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting experience by ID: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

### 6. Lambda Handler with Mangum

**lambda_handler.py - AWS Lambda Entry Point:**
```python
from fastapi import FastAPI, HTTPException
from mangum import Mangum
import asyncpg
import os
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.middleware_factory import lambda_handler_decorator

# Import FastAPI app
from app.main import app

# AWS Lambda Powertools
logger = Logger()
tracer = Tracer()
metrics = Metrics()

# Configure Mangum for Lambda
handler = Mangum(
    app,
    lifespan="off",  # Disable lifespan events for Lambda
    api_gateway_base_path="/prod"  # Adjust based on your API Gateway stage
)

@lambda_handler_decorator(logger=logger, tracer=tracer, metrics=metrics)
def lambda_handler(event, context):
    """
    AWS Lambda entry point with observability.

    Args:
        event: API Gateway event
        context: Lambda context

    Returns:
        HTTP response for API Gateway
    """
    # Log request details
    logger.info(
        "Lambda invocation started",
        extra={
            "request_id": context.aws_request_id,
            "function_name": context.function_name,
            "event_path": event.get("path", "unknown"),
            "http_method": event.get("httpMethod", "unknown")
        }
    )

    # Add custom metrics
    metrics.add_metric(name="LambdaInvocation", unit="Count", value=1)

    try:
        # Process request through Mangum
        response = handler(event, context)

        # Log successful response
        logger.info(
            "Lambda invocation completed",
            extra={
                "status_code": response.get("statusCode", "unknown"),
                "request_id": context.aws_request_id
            }
        )

        # Add success metric
        metrics.add_metric(name="SuccessfulRequests", unit="Count", value=1)

        return response

    except Exception as e:
        # Log error
        logger.error(
            f"Lambda invocation failed: {str(e)}",
            exc_info=True,
            extra={"request_id": context.aws_request_id}
        )

        # Add error metric
        metrics.add_metric(name="FailedRequests", unit="Count", value=1)

        # Return error response
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": '{"error": "Internal server error", "timestamp": "' +
                   str(datetime.utcnow().isoformat()) + '"}'
        }
```

### 7. Requirements and Dependencies

**requirements.txt:**
```txt
# FastAPI and ASGI
fastapi==0.104.1
mangum==0.17.0
uvicorn[standard]==0.24.0

# Database
asyncpg==0.29.0

# Validation and serialization
pydantic[email]==2.5.0
python-multipart==0.0.6

# AWS Lambda Powertools
aws-lambda-powertools[all]==2.28.0

# Development dependencies (for local testing)
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.25.2
black==23.11.0
ruff==0.1.6
mypy==1.7.1
```

---

## 🌐 AWS Lambda + API Gateway Deployment

### 1. SAM Template Configuration

**template.yaml - AWS SAM Template:**
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Portfolio FastAPI Lambda Backend

Globals:
  Function:
    Runtime: python3.12
    Timeout: 30
    MemorySize: 512
    Environment:
      Variables:
        ENVIRONMENT: !Ref Environment
        DATABASE_URL: !Ref DatabaseUrl
        LOG_LEVEL: INFO
        POWERTOOLS_SERVICE_NAME: portfolio-api
        POWERTOOLS_METRICS_NAMESPACE: Portfolio

Parameters:
  Environment:
    Type: String
    Default: dev
    AllowedValues: [dev, staging, prod]
  DatabaseUrl:
    Type: String
    NoEcho: true
    Description: Neon PostgreSQL connection string

Resources:
  PortfolioAPI:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub '${AWS::StackName}-portfolio-api'
      CodeUri: .
      Handler: lambda_handler.lambda_handler
      Description: FastAPI Portfolio Backend
      Environment:
        Variables:
          ENVIRONMENT: !Ref Environment
          DATABASE_URL: !Ref DatabaseUrl
      Events:
        APIRoot:
          Type: Api
          Properties:
            RestApiId: !Ref PortfolioApiGateway
            Path: /
            Method: ANY
        APIProxy:
          Type: Api
          Properties:
            RestApiId: !Ref PortfolioApiGateway
            Path: /{proxy+}
            Method: ANY

  PortfolioApiGateway:
    Type: AWS::Serverless::Api
    Properties:
      Name: !Sub '${AWS::StackName}-api'
      StageName: !Ref Environment
      Cors:
        AllowOrigin: "'*'"
        AllowHeaders: "'Content-Type,X-Amz-Date,Authorization,X-Api-Key'"
        AllowMethods: "'GET,POST,PUT,DELETE,OPTIONS'"
      TracingEnabled: true
      MethodSettings:
        - ResourcePath: "/*"
          HttpMethod: "*"
          LoggingLevel: INFO
          DataTraceEnabled: true

Outputs:
  PortfolioApiUrl:
    Description: Portfolio API Gateway URL
    Value: !Sub 'https://${PortfolioApiGateway}.execute-api.${AWS::Region}.amazonaws.com/${Environment}'
    Export:
      Name: !Sub '${AWS::StackName}-ApiUrl'

  PortfolioFunctionArn:
    Description: Portfolio Lambda Function ARN
    Value: !GetAtt PortfolioAPI.Arn
    Export:
      Name: !Sub '${AWS::StackName}-FunctionArn'
```

### 2. Deployment Scripts

**deploy.sh - Deployment Script:**
```bash
#!/bin/bash
set -e

# Configuration
STACK_NAME="portfolio-api"
REGION="us-east-1"
ENVIRONMENT=${1:-dev}
S3_BUCKET="your-sam-deployment-bucket"

echo "🚀 Deploying Portfolio FastAPI Lambda to $ENVIRONMENT"

# Validate SAM template
echo "🔍 Validating SAM template..."
sam validate --template template.yaml

# Build application
echo "📦 Building Lambda function..."
sam build --use-container

# Deploy to AWS
echo "🌐 Deploying to AWS..."
sam deploy \
    --stack-name "$STACK_NAME-$ENVIRONMENT" \
    --s3-bucket "$S3_BUCKET" \
    --region "$REGION" \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides \
        Environment="$ENVIRONMENT" \
        DatabaseUrl="$DATABASE_URL" \
    --confirm-changeset

# Get API Gateway URL
API_URL=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME-$ENVIRONMENT" \
    --region "$REGION" \
    --query 'Stacks[0].Outputs[?OutputKey==`PortfolioApiUrl`].OutputValue' \
    --output text)

echo "✅ Deployment completed!"
echo "🌐 API URL: $API_URL"
echo "📚 API Docs: $API_URL/docs"
echo "🔍 Health Check: $API_URL/health"
```

---

## 🔗 Astro Integration with FastAPI Lambda APIs

### 1. Astro Content Layer Integration

**src/content/config.ts - Astro Content Configuration:**
```typescript
import { defineCollection } from 'astro:content';
import { portfolioSchema } from './portfolio-schema';

// Define collections that load from FastAPI Lambda
const personalCollection = defineCollection({
  type: 'data',
  schema: portfolioSchema.personalInfo,
});

const experienceCollection = defineCollection({
  type: 'data',
  schema: portfolioSchema.experience,
});

const projectsCollection = defineCollection({
  type: 'data',
  schema: portfolioSchema.projects,
});

export const collections = {
  personal: personalCollection,
  experience: experienceCollection,
  projects: projectsCollection,
};
```

**src/lib/api-client.ts - FastAPI Client:**
```typescript
interface ApiResponse<T> {
  data?: T;
  error?: string;
  status_code: number;
}

class PortfolioApiClient {
  private baseUrl: string;
  private apiKey?: string;

  constructor(baseUrl: string, apiKey?: string) {
    this.baseUrl = baseUrl.replace(/\/$/, '');
    this.apiKey = apiKey;
  }

  private async request<T>(endpoint: string): Promise<T> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    if (this.apiKey) {
      headers['X-API-Key'] = this.apiKey;
    }

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      headers,
      // Add timeout for build-time requests
      signal: AbortSignal.timeout(10000),
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async getPersonalInfo() {
    return this.request<PersonalInfo>('/api/personal-info');
  }

  async getExperience() {
    return this.request<Experience[]>('/api/experience');
  }

  async getProjects() {
    return this.request<Project[]>('/api/projects');
  }

  async getSkills() {
    return this.request<Skill[]>('/api/skills');
  }
}

// Export configured client
export const apiClient = new PortfolioApiClient(
  import.meta.env.PUBLIC_API_URL || 'https://api.portfolio.com',
  import.meta.env.API_KEY
);
```

### 2. Build-time Data Loading

**src/pages/index.astro - Home Page with API Data:**
```astro
---
import Layout from '../layouts/Layout.astro';
import PersonalInfo from '../components/PersonalInfo.astro';
import Experience from '../components/Experience.astro';
import { apiClient } from '../lib/api-client';

// Load data at build time from FastAPI Lambda
let personalInfo, experience, projects;

try {
  [personalInfo, experience, projects] = await Promise.all([
    apiClient.getPersonalInfo(),
    apiClient.getExperience(),
    apiClient.getProjects(),
  ]);
} catch (error) {
  console.error('Failed to load data from API:', error);
  // Fallback to empty data or cached data
  personalInfo = null;
  experience = [];
  projects = [];
}
---

<Layout title="Portfolio">
  <main>
    {personalInfo && <PersonalInfo data={personalInfo} />}
    {experience.length > 0 && <Experience data={experience} />}
    <!-- Add more components as needed -->
  </main>
</Layout>
```

---

## 🧪 Testing & TDD for FastAPI Lambda

### Testing Framework Stack

**FastAPI + Lambda Testing Tools:**
- **pytest**: Test framework with async support
- **pytest-asyncio**: Async test support
- **httpx**: Async HTTP client for API testing
- **moto**: AWS services mocking
- **testcontainers**: Database testing with containers

### Pytest Configuration for FastAPI

**pytest.ini:**
```ini
[tool:pytest]
minversion = 6.0
addopts =
    -ra
    --strict-markers
    --strict-config
    --cov=app
    --cov-report=term-missing:skip-covered
    --cov-fail-under=80
python_files = tests/*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
testpaths = tests
filterwarnings =
    error
    ignore::UserWarning
    ignore::DeprecationWarning
```

### TDD FastAPI Implementation

**tests/test_main.py - FastAPI App Tests:**
```python
import pytest
from httpx import AsyncClient
from app.main import app

class TestFastAPIApp:
    """TDD tests for FastAPI application."""

    @pytest.mark.asyncio
    async def test_red_health_endpoint_missing(self):
        """RED: Test should fail when health endpoint is not implemented."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/nonexistent-health")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_green_health_endpoint_basic(self):
        """GREEN: Basic health endpoint implementation."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "portfolio-api"

    @pytest.mark.asyncio
    async def test_refactor_health_endpoint_comprehensive(self):
        """REFACTOR: Comprehensive health endpoint with all fields."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/health")

        assert response.status_code == 200
        data = response.json()

        # Verify all required fields
        required_fields = ["status", "service", "timestamp", "version"]
        for field in required_fields:
            assert field in data
            assert data[field] is not None

        # Verify data types
        assert isinstance(data["status"], str)
        assert isinstance(data["service"], str)
        assert isinstance(data["timestamp"], str)
        assert isinstance(data["version"], str)
```

**tests/test_routes.py - API Routes Tests:**
```python
import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
from app.main import app

class TestPersonalInfoRoutes:
    """TDD tests for personal info routes."""

    @pytest.mark.asyncio
    async def test_red_personal_info_no_data(self):
        """RED: Test should fail when no personal info exists."""
        with patch('app.database.Database.execute_one', return_value=None):
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get("/api/personal-info")

        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["error"]

    @pytest.mark.asyncio
    async def test_green_personal_info_basic_data(self):
        """GREEN: Basic personal info retrieval."""
        mock_data = {
            "name": "John Doe",
            "title": "Developer",
            "email": "john@example.com",
            "phone": None,
            "location": None,
            "linkedin": None,
            "github": None,
            "summary": None
        }

        with patch('app.database.Database.execute_one', return_value=mock_data):
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get("/api/personal-info")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "John Doe"
        assert data["title"] == "Developer"
        assert data["email"] == "john@example.com"

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

        with patch('app.database.Database.execute_one', return_value=mock_data):
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get("/api/personal-info")

        assert response.status_code == 200
        data = response.json()

        # Verify all fields are present and properly typed
        assert data["name"] == "Pablo Contreras"
        assert data["title"] == "Python Developer"
        assert data["email"] == "pablo@bypabloc.dev"
        assert data["linkedin"] == "https://linkedin.com/in/bypabloc"
        assert data["github"] == "https://github.com/bypabloc"
        assert len(data["summary"]) > 10  # Has meaningful content
```

### LocalStack Integration Testing

**tests/test_lambda_integration.py - Lambda Integration Tests:**
```python
import pytest
import json
from moto import mock_lambda, mock_apigateway
import boto3
from lambda_handler import lambda_handler

@mock_lambda
@mock_apigateway
class TestLambdaIntegration:
    """Integration tests for Lambda function."""

    def test_lambda_handler_api_gateway_event(self):
        """Test Lambda handler with API Gateway event."""
        # Mock API Gateway event
        event = {
            "httpMethod": "GET",
            "path": "/health",
            "headers": {"Content-Type": "application/json"},
            "queryStringParameters": None,
            "body": None,
            "isBase64Encoded": False
        }

        # Mock Lambda context
        context = type('Context', (), {
            'aws_request_id': 'test-request-123',
            'function_name': 'test-function',
            'memory_limit_in_mb': 512
        })()

        # Execute Lambda handler
        response = lambda_handler(event, context)

        # Verify response structure
        assert response["statusCode"] == 200
        assert "application/json" in response["headers"]["Content-Type"]

        # Parse response body
        body = json.loads(response["body"])
        assert body["status"] == "healthy"
        assert body["service"] == "portfolio-api"

    def test_lambda_handler_personal_info_endpoint(self):
        """Test personal info endpoint through Lambda."""
        event = {
            "httpMethod": "GET",
            "path": "/api/personal-info",
            "headers": {"Content-Type": "application/json"},
            "queryStringParameters": None,
            "body": None,
            "isBase64Encoded": False
        }

        context = type('Context', (), {
            'aws_request_id': 'test-request-456',
            'function_name': 'test-function'
        })()

        # Mock database connection
        with patch('app.database.Database.execute_one') as mock_db:
            mock_db.return_value = {
                "name": "Test User",
                "title": "Test Developer",
                "email": "test@example.com",
                "phone": None,
                "location": None,
                "linkedin": None,
                "github": None,
                "summary": None
            }

            response = lambda_handler(event, context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["name"] == "Test User"
        assert body["email"] == "test@example.com"
```

### Test Scripts for FastAPI Lambda

**test_runner.py - Test Execution Script:**
```python
#!/usr/bin/env python3
"""
FastAPI Lambda Test Runner with comprehensive coverage.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_tests():
    """Run complete test suite for FastAPI Lambda."""

    print("🧪 Running FastAPI Lambda Test Suite")
    print("=" * 50)

    # Set environment variables for testing
    os.environ.update({
        "ENVIRONMENT": "test",
        "DATABASE_URL": "postgresql://test:test@localhost:5433/test_portfolio",
        "LOG_LEVEL": "ERROR"
    })

    # Test commands to run
    commands = [
        # Unit tests
        ["python", "-m", "pytest", "tests/", "-v", "--cov=app", "--cov-report=term"],

        # Type checking
        ["python", "-m", "mypy", "app/", "--strict"],

        # Code formatting check
        ["python", "-m", "black", "--check", "app/", "tests/"],

        # Linting
        ["python", "-m", "ruff", "check", "app/", "tests/"],

        # Integration tests (if LocalStack is running)
        ["python", "-m", "pytest", "tests/test_lambda_integration.py", "-v"],
    ]

    failed_commands = []

    for cmd in commands:
        print(f"\n🔍 Running: {' '.join(cmd)}")
        print("-" * 30)

        try:
            result = subprocess.run(cmd, check=True, capture_output=False)
            print(f"✅ {' '.join(cmd[:3])} passed")
        except subprocess.CalledProcessError as e:
            print(f"❌ {' '.join(cmd[:3])} failed with exit code {e.returncode}")
            failed_commands.append(' '.join(cmd))

    # Summary
    print("\n" + "=" * 50)
    print("🧪 Test Suite Summary")
    print("=" * 50)

    if failed_commands:
        print("❌ Some tests failed:")
        for cmd in failed_commands:
            print(f"  - {cmd}")
        sys.exit(1)
    else:
        print("✅ All tests passed!")
        print("🚀 FastAPI Lambda is ready for deployment!")

if __name__ == "__main__":
    run_tests()
```

---

## 🎯 FastAPI + Lambda Performance Optimizations

### 1. Cold Start Optimization

**Optimized Lambda Handler:**
```python
import os
from functools import lru_cache
from fastapi import FastAPI
from mangum import Mangum

# Cache FastAPI app instance
@lru_cache(maxsize=1)
def create_app() -> FastAPI:
    """Create cached FastAPI app instance."""
    from app.main import app
    return app

# Cache Mangum handler
@lru_cache(maxsize=1)
def create_handler():
    """Create cached Mangum handler."""
    app = create_app()
    return Mangum(
        app,
        lifespan="off",
        api_gateway_base_path=f"/{os.getenv('STAGE', 'prod')}"
    )

# Initialize handler at module level (outside function)
handler = create_handler()

def lambda_handler(event, context):
    """Optimized Lambda handler with caching."""
    return handler(event, context)
```

### 2. Database Connection Optimization

**Connection Pooling for Lambda:**
```python
import asyncio
from typing import Optional
import asyncpg

class OptimizedDatabase:
    """Optimized database connection for Lambda with connection reuse."""

    _connection_pool: Optional[asyncpg.Pool] = None

    @classmethod
    async def get_pool(cls) -> asyncpg.Pool:
        """Get or create connection pool."""
        if cls._connection_pool is None or cls._connection_pool.is_closed():
            cls._connection_pool = await asyncpg.create_pool(
                os.getenv("DATABASE_URL"),
                min_size=1,
                max_size=3,  # Low for Lambda
                command_timeout=30,
                server_settings={
                    'application_name': 'portfolio-lambda',
                    'jit': 'off',
                    'shared_preload_libraries': ''
                }
            )
        return cls._connection_pool

    @classmethod
    async def execute_query(cls, query: str, *args):
        """Execute query with connection pooling."""
        pool = await cls.get_pool()
        async with pool.acquire() as connection:
            result = await connection.fetch(query, *args)
            return [dict(row) for row in result]
```

### 3. Response Caching

**Lambda Response Caching:**
```python
from functools import lru_cache
import json
import hashlib
from typing import Dict, Any

class ResponseCache:
    """Simple in-memory response cache for Lambda."""

    _cache: Dict[str, Any] = {}

    @classmethod
    def get_cache_key(cls, path: str, query_params: Dict = None) -> str:
        """Generate cache key for request."""
        content = f"{path}:{json.dumps(query_params or {}, sort_keys=True)}"
        return hashlib.md5(content.encode()).hexdigest()

    @classmethod
    def get(cls, key: str) -> Optional[Any]:
        """Get cached response."""
        return cls._cache.get(key)

    @classmethod
    def set(cls, key: str, value: Any, ttl: int = 300):
        """Set cached response with TTL."""
        # Simple TTL implementation (production should use proper TTL)
        cls._cache[key] = value

        # Keep cache size manageable
        if len(cls._cache) > 100:
            # Remove oldest entries
            old_keys = list(cls._cache.keys())[:20]
            for old_key in old_keys:
                del cls._cache[old_key]

# Usage in routes
@router.get("/personal-info")
async def get_personal_info_cached(db: Database = Depends(get_database)):
    """Get personal info with caching."""
    cache_key = ResponseCache.get_cache_key("/api/personal-info")

    # Check cache first
    cached_response = ResponseCache.get(cache_key)
    if cached_response:
        return cached_response

    # Fetch from database
    result = await db.execute_one("""
        SELECT name, title, email, phone, location, linkedin, github, summary
        FROM personal_info WHERE active = true ORDER BY updated_at DESC LIMIT 1
    """)

    if not result:
        raise HTTPException(status_code=404, detail="Personal info not found")

    response = PersonalInfo(**result)

    # Cache response
    ResponseCache.set(cache_key, response, ttl=300)  # 5 minutes

    return response
```

---

## 🌟 FastAPI + Lambda - Key Advantages Summary

### 🚀 **Performance Benefits**
1. **Cold starts optimizados** ~300ms para serverless
2. **Async/await native** para operaciones I/O intensivas
3. **Optimized for serverless** con Mangum adapter
4. **Connection pooling** optimizado para Lambda lifecycle
5. **Response caching** para datos que cambian poco

### 🔒 **Type Safety Benefits**
1. **Pydantic validation** automática en requests/responses
2. **Type hints end-to-end** desde database hasta API
3. **Auto-generated OpenAPI schema** con validación
4. **IDE support completo** con autocompletado y error detection
5. **Runtime validation** con error messages claros

### 📚 **Developer Experience Benefits**
1. **OpenAPI/Swagger docs** generados automáticamente
2. **Interactive API testing** con Swagger UI integrado
3. **Modern Python syntax** con decorators y type hints
4. **Excellent debugging** con detailed error messages
5. **Hot reload** en desarrollo con uvicorn

### 🔧 **Lambda Integration Benefits**
1. **Mangum adapter** optimizado para AWS Lambda
2. **AWS Lambda Powertools** integration nativa
3. **CloudWatch logging** automatizado con structured logs
4. **X-Ray tracing** support para observabilidad
5. **API Gateway integration** seamless con CORS y auth

### 📦 **Deployment Benefits**
1. **Small footprint** ~15MB para Lambda deployment
2. **SAM CLI integration** para infrastructure as code
3. **Container support** para development y production
4. **Layer optimization** para dependency management
5. **Environment configuration** flexible para dev/staging/prod

### 🎯 **Business Benefits**
1. **Cost-effective** pay-per-execution con auto-scaling
2. **High availability** con AWS Lambda managed infrastructure
3. **Security** con IAM integration y VPC support
4. **Scalability** automática desde 0 hasta miles de requests
5. **Maintenance-free** infrastructure management

---

**FastAPI + Lambda es la combinación ideal para APIs modernas serverless que requieren performance, type safety y developer experience optimizados para 2025.**

Esta arquitectura proporciona el balance perfecto entre **simplicidad de desarrollo**, **performance en producción**, y **cost optimization** para aplicaciones serverless modernas que necesitan integrarse perfectamente con frontends estáticos como Astro.