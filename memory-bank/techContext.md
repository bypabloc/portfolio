# Tech Context - Portfolio Technology Stack

> **Memory Bank Component**: Technology stack, tools, configurations, and technical specifications
> **Last Updated**: 2025-01-19
> **Stack Version**: 2025.1 - Modern Serverless Stack

## 🚀 Frontend Technology Stack

### Core Framework & Language
```typescript
Framework: Astro v5.x (latest)
  - Features: Content Layer, Server Islands, Astro Actions
  - Mode: SSG (Static Site Generation) with dynamic islands
  - Config: astro.config.ts with TypeScript integration

Language: TypeScript 5.3+
  - Mode: Strict mode MANDATORY
  - Target: ES2022+
  - Module: ESNext
  - Config: tsconfig.json with zero-tolerance for 'any' types

Node.js: v20.x LTS (Hydrogen)
  - Package Manager: pnpm (preferred) / npm (fallback)
  - Engine Requirements: >=20.0.0
```

### Frontend Dependencies & Tools
```json
// Core Dependencies
{
  "astro": "^5.x.x",
  "@astrojs/typescript": "^2.x.x",
  "@astrojs/tailwind": "^5.x.x",
  "@astrojs/sitemap": "^3.x.x",
  "@astrojs/rss": "^4.x.x"
}

// Development Dependencies
{
  "vitest": "^2.x.x",
  "@vitest/ui": "^2.x.x",
  "playwright": "^1.x.x",
  "@playwright/test": "^1.x.x",
  "eslint": "^9.x.x",
  "@typescript-eslint/parser": "^8.x.x",
  "prettier": "^3.x.x"
}
```

### Frontend Development Commands
```bash
# Project Setup
npm create astro@latest portfolio-astro
cd portfolio-astro && pnpm install

# Development
pnpm dev                    # Start development server (http://localhost:4321)
pnpm build                  # Production build
pnpm preview               # Preview production build
pnpm check                 # Astro diagnostics and TypeScript check

# Testing
pnpm test                  # Run unit tests with Vitest
pnpm test:ui              # Vitest UI interface
pnpm test:watch           # Watch mode for testing
pnpm test:e2e             # End-to-end tests with Playwright
pnpm test:coverage        # Coverage report

# Code Quality
pnpm lint                 # ESLint checking
pnpm lint:fix            # Auto-fix linting issues
pnpm format              # Prettier formatting
pnpm type-check          # TypeScript type checking
```

## 🐍 Backend Technology Stack

### Core Framework & Runtime
```python
Runtime: Python 3.12.x (latest stable)
  - Features: Enhanced type hints, performance improvements
  - Virtual Environment: venv (recommended) / poetry

Framework: FastAPI 0.115.x+
  - Features: Async support, automatic OpenAPI docs
  - Integration: Mangum adapter for AWS Lambda
  - Validation: Pydantic v2 for data models

AWS Integration:
  - AWS Lambda Python Runtime: python3.12
  - Deployment Tool: SAM CLI 1.x
  - Adapter: Mangum for FastAPI → Lambda integration
```

### Backend Dependencies & Libraries
```python
# Core Dependencies (requirements.txt)
fastapi==0.115.*
mangum==0.18.*
pydantic==2.8.*
asyncpg==0.29.*
aws-lambda-powertools==3.2.*

# Development Dependencies
pytest==8.3.*
pytest-asyncio==0.24.*
pytest-cov==5.0.*
moto==5.0.*
localstack==3.8.*
black==24.8.*
isort==5.13.*
mypy==1.11.*
ruff==0.6.*
```

### Backend Development Commands
```bash
# Environment Setup
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

pip install -r requirements.txt
pip install -r requirements-dev.txt

# Development
sam build                          # Build Lambda functions
sam local start-api               # Local API Gateway simulation
sam local invoke FunctionName    # Test individual functions

# Testing
pytest                            # Run all tests
pytest --cov=src                 # Run with coverage
pytest --cov=src --cov-report=html  # HTML coverage report
pytest -v tests/unit/            # Unit tests only
pytest -v tests/integration/     # Integration tests only

# Code Quality
black src/ tests/                # Format code
isort src/ tests/               # Sort imports
mypy src/                       # Type checking
ruff check src/                 # Fast linting
ruff check --fix src/          # Auto-fix issues

# AWS Deployment
sam validate                    # Validate SAM template
sam deploy --guided            # Initial deployment setup
sam deploy                     # Deploy to AWS
sam logs -n FunctionName       # View function logs
```

## 🗄️ Database Technology Stack

### Database Service
```yaml
Provider: Neon PostgreSQL
  - Type: Serverless PostgreSQL-as-a-Service
  - Version: PostgreSQL 16.x
  - Features: Database branching, auto-scaling, serverless compute

Connection Library: AsyncPG 0.29.x+
  - Features: High-performance async PostgreSQL adapter
  - Connection Pooling: Built-in connection pool management
  - Type Safety: Integration with Pydantic models

Migration Tool: Alembic 1.13.x+
  - Features: Version-controlled schema migrations
  - Integration: SQLAlchemy ORM compatibility
  - Branching: Support for Neon database branches
```

### Database Configuration
```python
# Database Connection Settings
DATABASE_CONFIG = {
    "host": "ep-xxx.neon.tech",
    "port": 5432,
    "database": "portfolio_db",
    "ssl": "require",
    "pool_size": 20,
    "max_overflow": 0,
    "pool_pre_ping": True,
    "pool_recycle": 300
}

# Neon Branch Configuration
ENVIRONMENTS = {
    "production": "main",
    "staging": "staging",
    "development": "dev",
    "feature": "feature-branch-name"
}
```

### Database Commands
```bash
# Neon CLI Setup
npm install -g neon-cli
neon auth                      # Authenticate with Neon

# Branch Management
neon branches create --name feature-new-endpoint --parent main
neon branches list            # List all branches
neon connection-string feature-new-endpoint  # Get connection string

# Local Development
docker-compose up postgres    # Local PostgreSQL for development
psql -h localhost -p 5432 -U postgres -d portfolio_db

# Migrations
alembic init migrations       # Initialize migration environment
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head         # Apply migrations
alembic downgrade -1         # Rollback one migration
```

## 🐳 Containerization & Infrastructure

### Docker Configuration
```yaml
# Docker Compose Services
version: '3.8'
services:
  personal-info:
    build: ./backend/personal-info
    ports: ["8001:8080"]
    environment:
      - DATABASE_URL=${PERSONAL_INFO_DB_URL}

  experience:
    build: ./backend/experience
    ports: ["8002:8080"]
    environment:
      - DATABASE_URL=${EXPERIENCE_DB_URL}

  projects:
    build: ./backend/projects
    ports: ["8003:8080"]
    environment:
      - DATABASE_URL=${PROJECTS_DB_URL}

  skills:
    build: ./backend/skills
    ports: ["8004:8080"]
    environment:
      - DATABASE_URL=${SKILLS_DB_URL}

  nginx:
    image: nginx:alpine
    ports: ["8080:80"]
    volumes:
      - ./docker/nginx/nginx.conf:/etc/nginx/nginx.conf

  postgres:
    image: postgres:16-alpine
    ports: ["5432:5432"]
    environment:
      - POSTGRES_DB=portfolio_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
```

### Docker Development Commands
```bash
# Development Environment
docker-compose up --build -d              # Start all services
docker-compose down                       # Stop all services
docker-compose logs -f service-name       # View logs
docker-compose restart service-name       # Restart specific service

# Development Modes
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up     # Development mode
docker-compose -f docker-compose.yml -f docker-compose.test.yml up    # Testing mode
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up    # Production simulation

# Utility Commands
docker-compose exec service-name bash     # Shell into service
docker-compose ps                        # List running services
docker system prune -a                   # Clean up Docker resources
```

## ☁️ AWS & Cloud Infrastructure

### AWS Services Stack
```yaml
Compute:
  - AWS Lambda (Python 3.12 runtime)
  - API Gateway v2 (HTTP APIs)
  - Lambda Layers for shared dependencies

Storage & Data:
  - Neon PostgreSQL (external managed service)
  - CloudWatch Logs for logging
  - S3 for static assets (if needed)

Networking:
  - API Gateway custom domains
  - Route 53 for DNS (if custom domain)
  - CloudFront for CDN (frontend deployment)

Monitoring:
  - CloudWatch Metrics and Alarms
  - AWS X-Ray for tracing
  - Lambda Powertools for observability
```

### AWS CLI & SAM Configuration
```bash
# AWS CLI Setup
aws --version                 # Verify AWS CLI v2
aws configure sso            # Configure SSO authentication
aws sso login --profile portfolio-dev

# SAM CLI Setup
sam --version                # Verify SAM CLI installation
sam init                    # Initialize new SAM project
sam build                   # Build Lambda functions
sam deploy --guided         # First-time deployment setup

# AWS Resource Management
aws lambda list-functions   # List deployed functions
aws logs describe-log-groups # List CloudWatch log groups
aws apigateway get-rest-apis # List API Gateway APIs
```

## 🧪 Testing Technology Stack

### Frontend Testing
```typescript
// Vitest Configuration (vitest.config.ts)
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'json'],
      threshold: {
        global: {
          branches: 80,
          functions: 80,
          lines: 80,
          statements: 80
        }
      }
    }
  }
});

// Playwright Configuration (playwright.config.ts)
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:4321',
    trace: 'on-first-retry'
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } }
  ]
});
```

### Backend Testing
```python
# pytest Configuration (pyproject.toml)
[tool.pytest.ini_options]
minversion = "8.0"
addopts = "-ra -q --strict-markers --strict-config"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
asyncio_mode = "auto"

# Coverage Configuration
[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/test_*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError"
]
```

## 🔧 Development Tools & IDE Configuration

### VS Code Configuration
```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",
  "typescript.preferences.strictFunctionTypes": true,
  "typescript.preferences.strictNullChecks": true,
  "eslint.workingDirectories": ["frontend"],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true,
    "source.organizeImports": true
  }
}

// .vscode/extensions.json
{
  "recommendations": [
    "astro-build.astro-vscode",
    "ms-python.python",
    "ms-python.black-formatter",
    "charliermarsh.ruff",
    "bradlc.vscode-tailwindcss",
    "esbenp.prettier-vscode"
  ]
}
```

### Git Configuration
```bash
# Git Hooks Setup (pre-commit)
pip install pre-commit
pre-commit install

# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-merge-conflict

  - repo: https://github.com/psf/black
    rev: 24.8.0
    hooks:
      - id: black

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.6.0
    hooks:
      - id: ruff
      - id: ruff-format
```

## 📊 Performance & Monitoring Stack

### Observability Tools
```python
# AWS Lambda Powertools Configuration
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.metrics import MetricUnit

logger = Logger()
tracer = Tracer()
metrics = Metrics()

# CloudWatch Custom Metrics
metrics.add_metric(name="ColdStart", unit=MetricUnit.Count, value=1)
metrics.add_metric(name="ApiLatency", unit=MetricUnit.Milliseconds, value=response_time)
```

### Performance Monitoring
```yaml
Frontend Metrics:
  - Lighthouse CI for performance auditing
  - Web Vitals tracking (LCP, FID, CLS)
  - Bundle analyzer for optimization

Backend Metrics:
  - Lambda duration and memory usage
  - Database connection metrics
  - API response time tracking
  - Error rate monitoring

Database Metrics:
  - Neon connection count
  - Query execution time
  - Database branch usage
  - Connection pool efficiency
```

## 🚀 Deployment & CI/CD Stack

### GitHub Actions Configuration
```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline
on: [push, pull_request]

jobs:
  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
      - run: pnpm install
      - run: pnpm test
      - run: pnpm build

  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements-dev.txt
      - run: pytest --cov=src
      - run: sam validate
```

### Deployment Targets
```yaml
Frontend Deployment:
  - Platform: AWS CloudFront + S3 (unified AWS stack)
  - Features: Global CDN, auto-deployment from Git, serverless distribution, unified AWS infrastructure

Backend Deployment:
  - Primary: AWS Lambda via SAM CLI
  - Staging: Separate AWS account/region
  - Production: Blue-green deployment strategy

Environment Management:
  - Development: Local Docker + LocalStack
  - Staging: AWS with Neon staging branch
  - Production: AWS with Neon main branch
```

---

*This technical context provides complete specifications for all tools, versions, and configurations used in the portfolio system. All development should strictly follow these technical standards to ensure consistency and reliability.*