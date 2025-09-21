# System Patterns - Portfolio Architecture & Conventions

> **Memory Bank Component**: Architectural patterns, conventions, and design decisions
> **Last Updated**: 2025-01-19
> **Architecture Version**: 1.0.0 - Serverless Microservices

## 🏗️ Core Architectural Principles

### Separation of Concerns
- **Complete Frontend/Server Separation**: Frontend consumes server via HTTP APIs only
- **Domain-Driven Design**: Clear boundaries between business domains (personal-info, experience, projects, skills)
- **Single Responsibility**: Each Lambda function handles one specific domain
- **API-First Design**: Contract definition before implementation

### Serverless-Native Patterns
- **Stateless Functions**: No shared state between Lambda invocations
- **Event-Driven Architecture**: Reactive patterns for data changes
- **Cold Start Optimization**: Connection pooling and initialization strategies
- **Pay-per-Use Economics**: Resource optimization for cost efficiency

## 📁 Project Structure & Organization

### Root Directory Structure
```
portfolio/
├── frontend/                    # Astro v5 SSG application
│   ├── src/
│   │   ├── content/            # Content Layer definitions
│   │   ├── actions/            # Astro Actions (type-safe server calls)
│   │   ├── islands/            # Server Islands components
│   │   ├── components/         # Reusable UI components
│   │   └── pages/              # Route pages
│   ├── astro.config.ts         # Astro configuration
│   └── tsconfig.json           # TypeScript strict configuration
├── server/                     # AWS Lambda microservices
│   ├── personal-info/          # Personal information service
│   ├── experience/             # Professional experience service
│   ├── projects/               # Project portfolio service
│   ├── skills/                 # Skills matrix service
│   └── shared/                 # Common utilities and types
├── docs/                       # Technical documentation
│   ├── readme.md              # Project overview
│   ├── server.md             # Server implementation guide
│   ├── frontend.md            # Frontend implementation guide
│   ├── db.md                  # Database integration guide
│   ├── docker.md              # Local development guide
│   └── testing.md             # Testing strategy guide
├── docker/                     # Local development environment
│   ├── docker-compose.yml     # Service orchestration
│   ├── nginx/                 # API Gateway simulation
│   └── postgres/              # Local database setup
├── scripts/                    # Automation and utility scripts
├── CLAUDE.md                  # Project-specific Claude instructions
├── productContext.md          # Business goals and user perspective
├── systemPatterns.md          # This file - architectural patterns
├── techContext.md             # Technology stack details
└── activeContext.md           # Current work focus
```

### Domain Service Structure
```
server/domain-name/
├── src/
│   ├── main.py                # Lambda handler entry point
│   ├── models/                # Pydantic data models
│   ├── services/              # Business logic layer
│   ├── repositories/          # Data access layer
│   └── utils/                 # Domain-specific utilities
├── tests/
│   ├── unit/                  # Unit tests
│   ├── integration/           # Integration tests
│   └── fixtures/              # Test data and mocks
├── Dockerfile                 # Local development container
├── requirements.txt           # Python dependencies
├── template.yaml              # SAM template for AWS deployment
└── pyproject.toml            # Python project configuration
```

## 🎯 Design Patterns & Conventions

### Server Patterns (Python + FastAPI)

#### Lambda Handler Pattern
```python
# Standard Lambda handler structure
from mangum import Mangum
from fastapi import FastAPI
from aws_lambda_powertools import Logger, Tracer, Metrics

app = FastAPI()
logger = Logger()
tracer = Tracer()
metrics = Metrics()

@app.get("/health")
@tracer.capture_method
def health_check():
    return {"status": "healthy", "service": "domain-name"}

handler = Mangum(app)
```

#### Repository Pattern
```python
# Data access abstraction
from abc import ABC, abstractmethod
from typing import List, Optional

class BaseRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Model]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Model]:
        pass

    @abstractmethod
    async def create(self, data: CreateModel) -> Model:
        pass
```

#### Service Layer Pattern
```python
# Business logic separation
class DomainService:
    def __init__(self, repository: DomainRepository):
        self.repository = repository

    async def get_domain_data(self, filters: FilterModel) -> List[DomainModel]:
        # Business logic here
        return await self.repository.get_filtered(filters)
```

### Frontend Patterns (Astro v5 + TypeScript)

#### Content Layer Pattern
```typescript
// src/content/config.ts
import { defineCollection, z } from 'astro:content';

const experienceCollection = defineCollection({
  type: 'data',
  schema: z.object({
    company: z.string(),
    position: z.string(),
    startDate: z.date(),
    endDate: z.date().optional(),
    description: z.string(),
    technologies: z.array(z.string())
  })
});

export const collections = {
  experience: experienceCollection
};
```

#### Astro Actions Pattern
```typescript
// src/actions/index.ts
import { defineAction } from 'astro:actions';
import { z } from 'astro:schema';

export const server = {
  getExperience: defineAction({
    input: z.object({
      limit: z.number().optional(),
      company: z.string().optional()
    }),
    handler: async (input) => {
      const response = await fetch(`${API_BASE_URL}/experience`, {
        method: 'POST',
        body: JSON.stringify(input)
      });
      return await response.json();
    }
  })
};
```

#### Server Islands Pattern
```astro
---
// src/islands/ExperienceList.astro
import { actions } from 'astro:actions';

const { experience } = await actions.getExperience({
  limit: 10
});
---

<div class="experience-container">
  {experience.map(exp => (
    <article class="experience-item">
      <h3>{exp.position} at {exp.company}</h3>
      <p>{exp.description}</p>
    </article>
  ))}
</div>
```

## 🔧 Coding Conventions & Standards

### TypeScript Standards (Frontend)
- **Strict Mode**: `"strict": true` in tsconfig.json - MANDATORY
- **No Any Types**: Zero tolerance for `any` - use proper typing
- **Explicit Return Types**: All functions must have explicit return types
- **Interface over Type**: Prefer interfaces for object shapes
- **Consistent Naming**: PascalCase for components, camelCase for variables

```typescript
// ✅ Correct TypeScript patterns
interface ExperienceData {
  readonly id: string;
  readonly company: string;
  readonly position: string;
  readonly startDate: Date;
  readonly endDate?: Date;
}

const formatExperience = (experience: ExperienceData): string => {
  // Implementation with explicit return type
  return `${experience.position} at ${experience.company}`;
};
```

### Python Standards (Server)
- **Type Hints**: All functions must have type annotations
- **Pydantic Models**: Use for all data validation and serialization
- **Async/Await**: Prefer async patterns for I/O operations
- **Error Handling**: Structured exception handling with logging
- **Snake Case**: Consistent naming convention

```python
# ✅ Correct Python patterns
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ExperienceModel(BaseModel):
    id: str
    company: str
    position: str
    start_date: datetime
    end_date: Optional[datetime] = None
    technologies: List[str]

async def get_experience_by_company(
    company: str,
    repository: ExperienceRepository
) -> List[ExperienceModel]:
    # Implementation with proper typing
    return await repository.find_by_company(company)
```

## 🧪 Testing Patterns & TDD

### Test-Driven Development (TDD) - MANDATORY
- **Red-Green-Refactor Cycle**: Write failing test → Make it pass → Refactor
- **Test First**: No production code without failing test
- **Single Assert**: One assertion per test when possible
- **Descriptive Names**: Test names should describe expected behavior

### Frontend Testing Strategy
```typescript
// Unit Tests with Vitest
import { describe, it, expect } from 'vitest';
import { formatExperience } from '../utils/formatting';

describe('formatExperience', () => {
  it('should format experience with end date', () => {
    const experience = {
      id: '1',
      company: 'TechCorp',
      position: 'Senior Developer',
      startDate: new Date('2023-01-01'),
      endDate: new Date('2024-01-01')
    };

    const result = formatExperience(experience);

    expect(result).toBe('Senior Developer at TechCorp (2023-2024)');
  });
});
```

### Server Testing Strategy
```python
# Unit Tests with pytest
import pytest
from unittest.mock import AsyncMock
from services.experience_service import ExperienceService

@pytest.mark.asyncio
async def test_get_experience_by_company():
    # Arrange
    mock_repository = AsyncMock()
    mock_repository.find_by_company.return_value = [
        ExperienceModel(id="1", company="TechCorp", position="Developer")
    ]
    service = ExperienceService(mock_repository)

    # Act
    result = await service.get_experience_by_company("TechCorp")

    # Assert
    assert len(result) == 1
    assert result[0].company == "TechCorp"
    mock_repository.find_by_company.assert_called_once_with("TechCorp")
```

## 🔗 Integration Patterns

### API Contract Design
- **RESTful Endpoints**: Standard HTTP methods and status codes
- **Consistent Response Format**: Standardized JSON structure
- **Error Handling**: Structured error responses with details
- **Versioning**: URL path versioning (/v1/, /v2/)

```python
# Standard API response format
class APIResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    timestamp: datetime
    version: str = "v1"
```

### Database Integration Patterns
- **Connection Pooling**: AsyncPG pool for Lambda efficiency
- **Query Optimization**: Use of indexes and efficient queries
- **Migration Strategy**: Version-controlled schema changes
- **Branch Strategy**: Neon branching for environment separation

### Inter-Service Communication
- **HTTP-Only**: No direct database sharing between services
- **Circuit Breaker**: Graceful degradation for service failures
- **Retry Logic**: Exponential backoff for transient failures
- **Timeout Handling**: Proper timeout configuration

## 🚀 Deployment & DevOps Patterns

### Local Development
- **Docker Compose**: Container orchestration for services
- **Hot Reload**: Live updating during development
- **Service Mocking**: Local mocks for external dependencies
- **Environment Parity**: Development matches production

### CI/CD Pipeline
- **Automated Testing**: All tests must pass before merge
- **Linting & Type Checking**: Zero tolerance for violations
- **Security Scanning**: Dependency and code security checks
- **Deployment Automation**: Infrastructure as Code with SAM

### Monitoring & Observability
- **Structured Logging**: JSON logs with correlation IDs
- **Metrics Collection**: Performance and business metrics
- **Error Tracking**: Centralized error monitoring
- **Health Checks**: Service health endpoints

## 📏 Quality Gates & Standards

### Code Quality Requirements
- **Test Coverage**: Minimum 80% across all components
- **Type Coverage**: 100% TypeScript strict mode compliance
- **Linting**: Zero ESLint/Pylint violations
- **Security**: No known vulnerabilities in dependencies

### Performance Standards
- **Cold Start**: <300ms Lambda initialization
- **API Response**: <100ms for simple queries
- **Frontend Load**: <2s for initial page load
- **Lighthouse Score**: >90 across all categories

### Documentation Requirements
- **API Documentation**: OpenAPI/Swagger for all endpoints
- **Code Comments**: JSDoc/docstrings for public interfaces
- **Architecture Decision Records**: Document significant decisions
- **Runbook Documentation**: Operations and troubleshooting guides

---

*These patterns and conventions ensure consistency, maintainability, and quality across the entire portfolio system. All team members and AI assistants should follow these established patterns when contributing to the project.*