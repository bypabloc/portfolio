# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## ⚠️ MANDATORY FIRST STEP

**ALWAYS read `docs/readme.md` FIRST** before working on any task in this repository. This file contains:
- Complete project overview and architecture summary
- Important warnings for AI assistants
- Required reading order for technical documentation
- Technology stack details and implementation guidelines

The `docs/readme.md` file is the entry point that explains the entire project structure and directs you to the specific documentation files you need to read for each component.

## 🧠 Memory Bank System

This repository includes a **Memory Bank system** for persistent context management across Claude Code sessions. The memory bank is located in the `memory-bank/` directory and consists of:

### Memory Bank Files (Complete 6-File System)

- **`memory-bank/projectbrief.md`** - Foundation document defining project purpose, scope, and success criteria
- **`memory-bank/productContext.md`** - Business goals, user perspective, and project objectives
- **`memory-bank/systemPatterns.md`** - Architectural patterns, conventions, and design decisions
- **`memory-bank/techContext.md`** - Technology stack, tools, configurations, and technical specifications
- **`memory-bank/activeContext.md`** - Current work focus, active tasks, and session tracking
- **`memory-bank/progress.md`** - Historical progress tracking, metrics, and milestone management

### Memory Bank Hierarchy

The memory bank follows this information flow pattern:

```
projectbrief.md → productContext.md ↘
                → systemPatterns.md → activeContext.md → progress.md
                → techContext.md   ↗
```

**Reading Priority**: `projectbrief.md` (foundation) → context files → `activeContext.md` (current work) → `progress.md` (historical tracking)

**Important**: Always read the memory bank files to understand:

- Current project context and business objectives
- Established architectural patterns and coding conventions
- Technology stack versions and configurations
- Active tasks and development focus

**Update `memory-bank/activeContext.md`** at the end of each development session to maintain continuity.

## Project Overview

This is a **documentation repository** for a modern serverless portfolio system architecture. The repository contains comprehensive implementation guides rather than actual code. The project documents a full-stack serverless portfolio system with:

- **Frontend**: Astro v5 with TypeScript (SSG)
- **Backend**: AWS Lambda + FastAPI + Python 3.12
- **Database**: Neon PostgreSQL (serverless)
- **Infrastructure**: Docker Compose for local development
- **Testing**: TDD with Vitest + pytest

## Architecture Philosophy

The documented system follows a **complete separation** between frontend and backend:

- Frontend (Astro v5) consumes backend APIs via HTTP
- Backend (FastAPI Lambda functions) are completely independent microservices
- Database (Neon PostgreSQL) uses Git-like branching for environments
- Local development replicates production architecture via Docker

## Key Documentation Files

### Technical Implementation Guides (`docs/` directory)

The `docs/` directory contains comprehensive implementation guides:

1. **`docs/readme.md`** - Project overview and mandatory entry point
   - Complete architecture summary and warnings for AI assistants
   - Technology stack overview and quick start guide
   - Reading order recommendations for all documentation

2. **`docs/backend.md`** (~42k) - FastAPI + AWS Lambda implementation
   - Mangum adapter for Lambda integration
   - Pydantic models for type safety
   - AsyncPG optimized for serverless
   - Cold start optimizations (~300ms)

3. **`docs/db.md`** (~24k) - Neon PostgreSQL integration
   - Database branching workflow (main/staging/dev/feature)
   - Connection pooling for Lambda lifecycle
   - Schema design for portfolio data

4. **`docs/docker.md`** (~23k) - Local development environment
   - Individual containers per Lambda function
   - SAM Local for API Gateway simulation
   - Multi-environment configurations

5. **`docs/frontend.md`** (~47k) - Astro v5 complete implementation
   - Content Layer for data loading
   - Server Islands for dynamic content
   - Astro Actions for type-safe backend calls
   - Strict TypeScript enforcement

6. **`docs/testing.md`** (~36k) - TDD strategy and implementation
   - Red-Green-Refactor cycles
   - Vitest + Container API for frontend
   - pytest + moto + LocalStack for backend
   - Contract testing between services

### Memory Bank Context Files (`memory-bank/` directory)

Complete 6-file context management system for persistent memory across Claude Code sessions:

1. **`memory-bank/projectbrief.md`** - Foundation document
   - Executive summary and core problem statement
   - Project scope, boundaries, and success criteria
   - Architecture philosophy and implementation strategy

2. **`memory-bank/productContext.md`** - Business and product perspective
   - Project purpose, goals, and user experience requirements
   - Success metrics and business objectives
   - Development roadmap and phase planning

3. **`memory-bank/systemPatterns.md`** - Architecture and conventions
   - Coding standards and design patterns
   - Project structure and file organization
   - Testing patterns and quality gates

4. **`memory-bank/techContext.md`** - Technology stack specifications
   - Complete technology versions and configurations
   - Development commands and tool setup
   - Deployment and infrastructure details

5. **`memory-bank/activeContext.md`** - Current work tracking
   - Active tasks and sprint goals
   - Progress tracking and session notes
   - Immediate priorities and blockers

6. **`memory-bank/progress.md`** - Historical tracking and metrics
   - Timeline, milestones, and completed phases
   - Quality metrics trends and architectural decisions
   - Risk tracking and lessons learned

## Development Approach

### TDD Requirements

- **Mandatory Red-Green-Refactor cycle** for all features
- **TypeScript strict mode** required for frontend
- **80%+ test coverage** for all components
- **Contract testing** between frontend and backend APIs

### Technology Stack Commands

**Frontend Development (when implemented):**

```bash
npm create astro@latest portfolio-astro
npm install
npm run dev                 # Development server
npm run build              # Production build
npm run test               # Vitest unit tests
npm run test:e2e          # Playwright E2E tests
npx astro check           # TypeScript validation
```

**Backend Development (when implemented):**

```bash
python -m venv venv && source venv/bin/activate
pip install fastapi mangum aws-lambda-powertools asyncpg
pytest --cov=src --cov-report=html    # Run tests with coverage
sam build && sam local start-api      # Local API Gateway
sam deploy --guided                   # AWS deployment
```

**Docker Development Environment:**

```bash
docker-compose up --build -d                                    # Start all services
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up  # Development mode
docker-compose -f docker-compose.yml -f docker-compose.test.yml up # Testing mode
```

### Database Operations (Neon)

```bash
# Create feature branch for development
neon branches create --name feature-new-endpoint --parent main

# Get connection string for specific branch
neon connection-string feature-new-endpoint

# Merge branch after testing
neon branches merge feature-new-endpoint main
```

## Critical Implementation Notes

### TypeScript Enforcement

- **Zero tolerance** for `any` types
- **Strict mode** required in tsconfig.json
- **Explicit typing** for all functions and variables
- **Pydantic models** for Python type safety

### Testing Strategy

- **Unit tests**: Individual component/function testing
- **Integration tests**: API contract validation
- **E2E tests**: Complete user workflow testing
- **Property-based testing**: Data model validation

### AWS Lambda Optimizations

- **Cold start mitigation**: Connection pooling and caching
- **Mangum adapter**: FastAPI to Lambda integration
- **AWS Powertools**: Structured logging and metrics
- **Environment separation**: dev/staging/prod via branches

## Working with This Repository

### Documentation Reading Order

When implementing the documented architecture, follow this reading sequence:

1. **ALWAYS read `docs/readme.md` first** - Mandatory entry point for understanding the project
2. **Review Memory Bank context** - Read `memory-bank/` files for current project state and conventions
3. **Read specific technical guides** - Choose from `docs/` files based on your current work focus
4. **Update Memory Bank** - Maintain `memory-bank/activeContext.md` with progress and decisions

### Development Workflow

1. **Context Setup**: Read memory bank files to understand current project state
2. **Technical Research**: Reference specific `docs/` files for implementation details
3. **Follow TDD practices**: Implement Red-Green-Refactor cycles as documented
4. **Use documented patterns**: Don't deviate from established architecture
5. **Test everything**: Maintain documented coverage requirements (>80%)
6. **Environment parity**: Local development must match production architecture
7. **Update context**: Record decisions and progress in `memory-bank/activeContext.md`

### File Reference Guide

**For High-Level Context**: Start with `memory-bank/` files
**For Implementation Details**: Use `docs/` files
**For Current Work**: Always check `memory-bank/activeContext.md`
**For Quick Reference**: Use `CLAUDE.md` (this file)

**CRITICAL**: The `docs/readme.md` file contains specific instructions for AI assistants and must be read before any work begins. The memory bank system provides persistent context across sessions.

The documentation is designed to be implementation-agnostic but follows modern 2025 best practices for serverless development with strict type safety and comprehensive testing.

## Importaciones

@./docs/readme.md
@./scripts/README.md
@./memory-bank/projectbrief.md
@./memory-bank/productContext.md
@./memory-bank/systemPatterns.md
@./memory-bank/techContext.md
@./memory-bank/activeContext.md
@./memory-bank/progress.md
