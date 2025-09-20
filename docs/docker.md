# Docker Compose for FastAPI Lambda Microservices - 2025

> **Comprehensive Docker Compose setup for FastAPI + AWS Lambda microservices with local development environment and SAM CLI integration.**

## 🚀 Executive Summary

This guide provides production-ready Docker Compose configurations for individual FastAPI Lambda functions in a microservices architecture. Each Lambda function is containerized separately for optimal development, testing, and deployment to AWS Lambda with API Gateway integration.

**Key Technologies**: Docker Compose, FastAPI, AWS Lambda, SAM CLI, Neon PostgreSQL, API Gateway Local

---

## 📋 Project Structure for Lambda Microservices

```
portfolio-fastapi-lambdas/
├── services/
│   ├── personal-info/
│   │   ├── app/
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   ├── template.yaml
│   │   └── requirements.txt
│   ├── experience/
│   │   ├── app/
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   ├── template.yaml
│   │   └── requirements.txt
│   ├── projects/
│   │   ├── app/
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   ├── template.yaml
│   │   └── requirements.txt
│   └── skills/
│       ├── app/
│       ├── tests/
│       ├── Dockerfile
│       ├── docker-compose.yml
│       ├── template.yaml
│       └── requirements.txt
├── shared/
│   ├── database/
│   ├── models/
│   └── utils/
├── docker-compose.yml          # Main compose file
├── docker-compose.dev.yml      # Development overrides
├── docker-compose.test.yml     # Testing environment
└── scripts/
    ├── start-dev.sh
    ├── run-tests.sh
    └── deploy-all.sh
```

---

## 🎯 Individual Lambda Service Configuration

### 1. Personal Info Service

**services/personal-info/Dockerfile:**
```dockerfile
# FastAPI Lambda Container for Personal Info Service
FROM public.ecr.aws/lambda/python:3.12

# Service metadata
LABEL service="personal-info"
LABEL version="1.0.0"
LABEL description="FastAPI Lambda for personal information management"

# Install system dependencies
RUN microdnf update -y && \
    microdnf install -y gcc postgresql-devel && \
    microdnf clean all

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ${LAMBDA_TASK_ROOT}/app/
COPY lambda_handler.py ${LAMBDA_TASK_ROOT}/

# Set the Lambda handler
CMD ["lambda_handler.lambda_handler"]
```

**services/personal-info/docker-compose.yml:**
```yaml
version: '3.8'

services:
  personal-info-api:
    build: .
    container_name: personal-info-lambda
    ports:
      - "9000:8080"  # Lambda Runtime Interface Emulator
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - ENVIRONMENT=development
      - LOG_LEVEL=DEBUG
      - POWERTOOLS_SERVICE_NAME=personal-info
      - AWS_LAMBDA_FUNCTION_NAME=personal-info-dev
    volumes:
      - ./app:/var/task/app:ro
      - ./tests:/var/task/tests:ro
    networks:
      - portfolio-network
    depends_on:
      - neon-postgres
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/2015-03-31/functions/function/invocations"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Local PostgreSQL for development (simulates Neon)
  neon-postgres:
    image: postgres:15-alpine
    container_name: neon-dev-db
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: portfolio_dev
      POSTGRES_USER: dev_user
      POSTGRES_PASSWORD: dev_password
      POSTGRES_HOST_AUTH_METHOD: trust
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./sql/init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - portfolio-network

  # SAM Local API Gateway simulation
  sam-local:
    image: public.ecr.aws/sam/cli:latest
    container_name: sam-local-api
    ports:
      - "3000:3000"
    volumes:
      - .:/var/opt/mount
      - /var/run/docker.sock:/var/run/docker.sock
    working_dir: /var/opt/mount
    command: sam local start-api --host 0.0.0.0 --port 3000 --warm-containers LAZY
    networks:
      - portfolio-network
    depends_on:
      - personal-info-api

networks:
  portfolio-network:
    driver: bridge

volumes:
  postgres_data:
```

### 2. Experience Service

**services/experience/docker-compose.yml:**
```yaml
version: '3.8'

services:
  experience-api:
    build: .
    container_name: experience-lambda
    ports:
      - "9001:8080"  # Different port for each service
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - ENVIRONMENT=development
      - LOG_LEVEL=DEBUG
      - POWERTOOLS_SERVICE_NAME=experience
      - AWS_LAMBDA_FUNCTION_NAME=experience-dev
    volumes:
      - ./app:/var/task/app:ro
      - ./tests:/var/task/tests:ro
    networks:
      - portfolio-network
    depends_on:
      - neon-postgres
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/2015-03-31/functions/function/invocations"]
      interval: 30s
      timeout: 10s
      retries: 3

  neon-postgres:
    image: postgres:15-alpine
    container_name: neon-dev-db
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: portfolio_dev
      POSTGRES_USER: dev_user
      POSTGRES_PASSWORD: dev_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./sql/init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - portfolio-network

networks:
  portfolio-network:
    external: true  # Use shared network

volumes:
  postgres_data:
```

### 3. Projects Service

**services/projects/docker-compose.yml:**
```yaml
version: '3.8'

services:
  projects-api:
    build: .
    container_name: projects-lambda
    ports:
      - "9002:8080"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - ENVIRONMENT=development
      - LOG_LEVEL=DEBUG
      - POWERTOOLS_SERVICE_NAME=projects
      - AWS_LAMBDA_FUNCTION_NAME=projects-dev
    volumes:
      - ./app:/var/task/app:ro
      - ./tests:/var/task/tests:ro
    networks:
      - portfolio-network
    depends_on:
      - neon-postgres

  neon-postgres:
    image: postgres:15-alpine
    container_name: neon-dev-db
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: portfolio_dev
      POSTGRES_USER: dev_user
      POSTGRES_PASSWORD: dev_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - portfolio-network

networks:
  portfolio-network:
    external: true

volumes:
  postgres_data:
```

### 4. Skills Service

**services/skills/docker-compose.yml:**
```yaml
version: '3.8'

services:
  skills-api:
    build: .
    container_name: skills-lambda
    ports:
      - "9003:8080"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - ENVIRONMENT=development
      - LOG_LEVEL=DEBUG
      - POWERTOOLS_SERVICE_NAME=skills
      - AWS_LAMBDA_FUNCTION_NAME=skills-dev
    volumes:
      - ./app:/var/task/app:ro
      - ./tests:/var/task/tests:ro
    networks:
      - portfolio-network
    depends_on:
      - neon-postgres

  neon-postgres:
    image: postgres:15-alpine
    container_name: neon-dev-db
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: portfolio_dev
      POSTGRES_USER: dev_user
      POSTGRES_PASSWORD: dev_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - portfolio-network

networks:
  portfolio-network:
    external: true

volumes:
  postgres_data:
```

---

## 🔧 Main Docker Compose Configuration

**docker-compose.yml (Root):**
```yaml
version: '3.8'

services:
  # Shared PostgreSQL Database (simulates Neon)
  neon-postgres:
    image: postgres:15-alpine
    container_name: neon-dev-db
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: portfolio_dev
      POSTGRES_USER: dev_user
      POSTGRES_PASSWORD: dev_password
      POSTGRES_HOST_AUTH_METHOD: trust
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./shared/sql/schema.sql:/docker-entrypoint-initdb.d/01-schema.sql
      - ./shared/sql/seed.sql:/docker-entrypoint-initdb.d/02-seed.sql
    networks:
      - portfolio-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U dev_user -d portfolio_dev"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Personal Info Lambda Service
  personal-info-service:
    build: ./services/personal-info
    container_name: personal-info-lambda
    ports:
      - "9000:8080"
    environment:
      - DATABASE_URL=postgresql://dev_user:dev_password@neon-postgres:5432/portfolio_dev
      - ENVIRONMENT=development
      - LOG_LEVEL=DEBUG
      - POWERTOOLS_SERVICE_NAME=personal-info
    volumes:
      - ./services/personal-info/app:/var/task/app:ro
      - ./shared:/var/task/shared:ro
    networks:
      - portfolio-network
    depends_on:
      neon-postgres:
        condition: service_healthy

  # Experience Lambda Service
  experience-service:
    build: ./services/experience
    container_name: experience-lambda
    ports:
      - "9001:8080"
    environment:
      - DATABASE_URL=postgresql://dev_user:dev_password@neon-postgres:5432/portfolio_dev
      - ENVIRONMENT=development
      - LOG_LEVEL=DEBUG
      - POWERTOOLS_SERVICE_NAME=experience
    volumes:
      - ./services/experience/app:/var/task/app:ro
      - ./shared:/var/task/shared:ro
    networks:
      - portfolio-network
    depends_on:
      neon-postgres:
        condition: service_healthy

  # Projects Lambda Service
  projects-service:
    build: ./services/projects
    container_name: projects-lambda
    ports:
      - "9002:8080"
    environment:
      - DATABASE_URL=postgresql://dev_user:dev_password@neon-postgres:5432/portfolio_dev
      - ENVIRONMENT=development
      - LOG_LEVEL=DEBUG
      - POWERTOOLS_SERVICE_NAME=projects
    volumes:
      - ./services/projects/app:/var/task/app:ro
      - ./shared:/var/task/shared:ro
    networks:
      - portfolio-network
    depends_on:
      neon-postgres:
        condition: service_healthy

  # Skills Lambda Service
  skills-service:
    build: ./services/skills
    container_name: skills-lambda
    ports:
      - "9003:8080"
    environment:
      - DATABASE_URL=postgresql://dev_user:dev_password@neon-postgres:5432/portfolio_dev
      - ENVIRONMENT=development
      - LOG_LEVEL=DEBUG
      - POWERTOOLS_SERVICE_NAME=skills
    volumes:
      - ./services/skills/app:/var/task/app:ro
      - ./shared:/var/task/shared:ro
    networks:
      - portfolio-network
    depends_on:
      neon-postgres:
        condition: service_healthy

  # API Gateway Local (SAM CLI)
  api-gateway:
    image: public.ecr.aws/sam/cli:latest
    container_name: sam-local-api
    ports:
      - "3000:3000"
    volumes:
      - .:/var/opt/mount
      - /var/run/docker.sock:/var/run/docker.sock
    working_dir: /var/opt/mount
    command: >
      sh -c "
        sam local start-api
        --host 0.0.0.0
        --port 3000
        --warm-containers LAZY
        --container-host host.docker.internal
      "
    networks:
      - portfolio-network
    depends_on:
      - personal-info-service
      - experience-service
      - projects-service
      - skills-service

  # Redis for caching (optional)
  redis-cache:
    image: redis:7-alpine
    container_name: redis-cache
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - portfolio-network
    command: redis-server --appendonly yes

  # Nginx API Gateway Proxy
  nginx-proxy:
    image: nginx:alpine
    container_name: nginx-api-proxy
    ports:
      - "8080:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    networks:
      - portfolio-network
    depends_on:
      - personal-info-service
      - experience-service
      - projects-service
      - skills-service

networks:
  portfolio-network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
```

---

## 🛠️ Development Environment Configuration

**docker-compose.dev.yml:**
```yaml
version: '3.8'

# Development overrides
services:
  personal-info-service:
    environment:
      - LOG_LEVEL=DEBUG
      - ENVIRONMENT=development
      - FASTAPI_RELOAD=true
    volumes:
      - ./services/personal-info:/var/task:rw  # Read-write for development
    command: >
      sh -c "
        pip install watchdog &&
        uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
      "

  experience-service:
    environment:
      - LOG_LEVEL=DEBUG
      - ENVIRONMENT=development
      - FASTAPI_RELOAD=true
    volumes:
      - ./services/experience:/var/task:rw
    command: >
      sh -c "
        pip install watchdog &&
        uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
      "

  projects-service:
    environment:
      - LOG_LEVEL=DEBUG
      - ENVIRONMENT=development
      - FASTAPI_RELOAD=true
    volumes:
      - ./services/projects:/var/task:rw
    command: >
      sh -c "
        pip install watchdog &&
        uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
      "

  skills-service:
    environment:
      - LOG_LEVEL=DEBUG
      - ENVIRONMENT=development
      - FASTAPI_RELOAD=true
    volumes:
      - ./services/skills:/var/task:rw
    command: >
      sh -c "
        pip install watchdog &&
        uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
      "

  # Development tools
  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: pgadmin-dev
    ports:
      - "5050:80"
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@portfolio.dev
      PGADMIN_DEFAULT_PASSWORD: password
      PGADMIN_CONFIG_SERVER_MODE: 'False'
    volumes:
      - pgadmin_data:/var/lib/pgadmin
    networks:
      - portfolio-network

volumes:
  pgadmin_data:
```

**docker-compose.test.yml:**
```yaml
version: '3.8'

# Testing environment
services:
  neon-postgres:
    environment:
      POSTGRES_DB: portfolio_test
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_password

  personal-info-service:
    environment:
      - DATABASE_URL=postgresql://test_user:test_password@neon-postgres:5432/portfolio_test
      - ENVIRONMENT=test
      - LOG_LEVEL=ERROR
    command: >
      sh -c "
        python -m pytest tests/ -v --cov=app --cov-report=html
      "

  experience-service:
    environment:
      - DATABASE_URL=postgresql://test_user:test_password@neon-postgres:5432/portfolio_test
      - ENVIRONMENT=test
      - LOG_LEVEL=ERROR
    command: >
      sh -c "
        python -m pytest tests/ -v --cov=app --cov-report=html
      "

  projects-service:
    environment:
      - DATABASE_URL=postgresql://test_user:test_password@neon-postgres:5432/portfolio_test
      - ENVIRONMENT=test
      - LOG_LEVEL=ERROR
    command: >
      sh -c "
        python -m pytest tests/ -v --cov=app --cov-report=html
      "

  skills-service:
    environment:
      - DATABASE_URL=postgresql://test_user:test_password@neon-postgres:5432/portfolio_test
      - ENVIRONMENT=test
      - LOG_LEVEL=ERROR
    command: >
      sh -c "
        python -m pytest tests/ -v --cov=app --cov-report=html
      "
```

---

## 🌐 Nginx Configuration for API Gateway

**nginx/nginx.conf:**
```nginx
events {
    worker_connections 1024;
}

http {
    upstream personal_info_backend {
        server personal-info-service:8080;
    }

    upstream experience_backend {
        server experience-service:8080;
    }

    upstream projects_backend {
        server projects-service:8080;
    }

    upstream skills_backend {
        server skills-service:8080;
    }

    server {
        listen 80;
        server_name localhost;

        # Health check endpoint
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }

        # Personal Info API
        location /api/personal-info {
            proxy_pass http://personal_info_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Experience API
        location /api/experience {
            proxy_pass http://experience_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Projects API
        location /api/projects {
            proxy_pass http://projects_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Skills API
        location /api/skills {
            proxy_pass http://skills_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # CORS headers
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
        add_header Access-Control-Allow-Headers "Content-Type, Authorization";
    }
}
```

---

## 📜 Management Scripts

**scripts/start-dev.sh:**
```bash
#!/bin/bash
set -e

echo "🚀 Starting Portfolio FastAPI Lambda Development Environment"

# Create network if it doesn't exist
docker network create portfolio-network 2>/dev/null || true

# Start all services in development mode
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d

echo "✅ Services started!"
echo ""
echo "📋 Available Services:"
echo "  🌐 API Gateway (Nginx): http://localhost:8080"
echo "  🔧 SAM Local API: http://localhost:3000"
echo "  👤 Personal Info: http://localhost:9000"
echo "  💼 Experience: http://localhost:9001"
echo "  🚀 Projects: http://localhost:9002"
echo "  🎯 Skills: http://localhost:9003"
echo "  🗄️  PostgreSQL: localhost:5432"
echo "  📊 PgAdmin: http://localhost:5050"
echo ""
echo "🧪 To run tests: ./scripts/run-tests.sh"
echo "🛑 To stop: docker-compose down"
```

**scripts/run-tests.sh:**
```bash
#!/bin/bash
set -e

echo "🧪 Running FastAPI Lambda Tests"

# Create network if it doesn't exist
docker network create portfolio-network 2>/dev/null || true

# Run tests for all services
docker-compose -f docker-compose.yml -f docker-compose.test.yml up --build --abort-on-container-exit

# Get exit codes
PERSONAL_INFO_EXIT=$(docker-compose -f docker-compose.yml -f docker-compose.test.yml ps -q personal-info-service | xargs docker inspect --format='{{.State.ExitCode}}')
EXPERIENCE_EXIT=$(docker-compose -f docker-compose.yml -f docker-compose.test.yml ps -q experience-service | xargs docker inspect --format='{{.State.ExitCode}}')
PROJECTS_EXIT=$(docker-compose -f docker-compose.yml -f docker-compose.test.yml ps -q projects-service | xargs docker inspect --format='{{.State.ExitCode}}')
SKILLS_EXIT=$(docker-compose -f docker-compose.yml -f docker-compose.test.yml ps -q skills-service | xargs docker inspect --format='{{.State.ExitCode}}')

# Cleanup
docker-compose -f docker-compose.yml -f docker-compose.test.yml down

# Check results
if [ "$PERSONAL_INFO_EXIT" = "0" ] && [ "$EXPERIENCE_EXIT" = "0" ] && [ "$PROJECTS_EXIT" = "0" ] && [ "$SKILLS_EXIT" = "0" ]; then
    echo "✅ All tests passed!"
    exit 0
else
    echo "❌ Some tests failed"
    echo "  Personal Info: $PERSONAL_INFO_EXIT"
    echo "  Experience: $EXPERIENCE_EXIT"
    echo "  Projects: $PROJECTS_EXIT"
    echo "  Skills: $SKILLS_EXIT"
    exit 1
fi
```

**scripts/deploy-all.sh:**
```bash
#!/bin/bash
set -e

echo "🚀 Deploying All FastAPI Lambda Services"

ENVIRONMENT=${1:-dev}
REGION=${2:-us-east-1}

# Deploy each service
SERVICES=("personal-info" "experience" "projects" "skills")

for service in "${SERVICES[@]}"; do
    echo "📦 Deploying $service service..."

    cd "services/$service"

    # Build and deploy with SAM
    sam build --use-container
    sam deploy \
        --stack-name "portfolio-$service-$ENVIRONMENT" \
        --region "$REGION" \
        --capabilities CAPABILITY_IAM \
        --parameter-overrides \
            Environment="$ENVIRONMENT" \
            DatabaseUrl="$DATABASE_URL"

    cd "../.."

    echo "✅ $service deployed successfully"
done

echo "🎉 All services deployed!"
```

---

## 🎯 Usage Examples

### Development Workflow:

```bash
# 1. Start development environment
./scripts/start-dev.sh

# 2. Test individual service
curl http://localhost:9000/2015-03-31/functions/function/invocations \
  -d '{"httpMethod":"GET","path":"/api/personal-info"}'

# 3. Test via API Gateway
curl http://localhost:8080/api/personal-info

# 4. Run tests
./scripts/run-tests.sh

# 5. Deploy to AWS
./scripts/deploy-all.sh dev us-east-1
```

### Individual Service Development:

```bash
# Work on specific service
cd services/personal-info
docker-compose up --build

# Test service directly
curl http://localhost:9000/2015-03-31/functions/function/invocations \
  -d '{"httpMethod":"GET","path":"/health"}'
```

---

## 🌟 Key Benefits

### **🔧 Development Benefits:**
1. **Isolated services** - Each Lambda function in separate container
2. **Hot reload** - FastAPI development with file watching
3. **Local API Gateway** - SAM CLI simulation of AWS API Gateway
4. **Database simulation** - PostgreSQL container simulating Neon
5. **Network isolation** - Docker network for service communication

### **🧪 Testing Benefits:**
1. **Service isolation** - Independent testing of each Lambda
2. **Integration testing** - Full stack testing with database
3. **Performance testing** - Load testing individual services
4. **CI/CD ready** - Docker-based testing pipeline
5. **Coverage reporting** - pytest with coverage for each service

### **🚀 Deployment Benefits:**
1. **Container-based deployment** - Direct deployment to AWS Lambda
2. **Environment parity** - Development matches production
3. **Microservices architecture** - Independent scaling and deployment
4. **SAM integration** - Infrastructure as code with SAM templates
5. **Multi-environment support** - dev/staging/prod configurations

---

**Docker Compose + FastAPI + Lambda** provides a complete local development environment that mirrors AWS Lambda production architecture, enabling efficient development, testing, and deployment of microservices-based portfolio system.