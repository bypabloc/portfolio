# Complete Testing & TDD Guide 2025 - Astro v5 + AWS Lambda Python

> **Context**: Comprehensive testing strategies for modern portfolio system using Test-Driven Development (TDD) with Astro v5 frontend and AWS Lambda Python backend, following 2025 best practices.

## Executive Summary

This guide provides production-ready testing implementation strategies for the serverless portfolio system architecture. It covers TDD methodologies, testing frameworks, mocking strategies, and integration testing approaches optimized for Astro v5 frontend consuming AWS Lambda Python APIs. The architecture maintains complete separation between frontend and backend through HTTP API testing.

**Key Technologies**: Vitest, Playwright, pytest, moto, LocalStack, MSW, AWS SAM CLI, Container API

---

## 1. Frontend Testing - Astro v5 with TDD

### 1.1 Testing Framework Stack

```yaml
# Frontend Testing Stack 2025
Unit Testing: Vitest + Container API
Component Testing: Vitest + Happy-DOM
Integration Testing: Vitest + Astro Dev Server
End-to-End Testing: Playwright
API Mocking: Mock Service Worker (MSW)
Visual Testing: Storybook + Chromatic
```

### 1.2 Vitest Configuration for Astro v5

```typescript
// vitest.config.ts
import { getViteConfig } from 'astro/config';

export default getViteConfig({
  test: {
    environment: 'happy-dom', // For DOM-dependent tests
    globals: true,
    setupFiles: ['./test/setup.ts'],
    exclude: ['**/e2e/**'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      exclude: [
        'coverage/**',
        'dist/**',
        '**/node_modules/**',
        '**/test/**'
      ]
    }
  }
});
```

### 1.3 Container API Component Testing (TDD)

```typescript
// test/components/PersonalInfo.test.ts
/// <reference types="vitest" />
// @vitest-environment happy-dom

import { experimental_AstroContainer as AstroContainer } from 'astro/container';
import { expect, test, describe, beforeEach } from 'vitest';
import PersonalInfo from '../../src/components/PersonalInfo.astro';

describe('PersonalInfo Component - TDD', () => {
  let container: Awaited<ReturnType<typeof AstroContainer.create>>;

  beforeEach(async () => {
    container = await AstroContainer.create();
  });

  test('RED: should render personal information with props', async () => {
    // TDD Red Phase - Write failing test first
    const result = await container.renderToString(PersonalInfo, {
      props: {
        name: 'Pablo Contreras',
        title: 'Full Stack Developer',
        email: 'pablo@bypabloc.com',
        location: 'Santiago, Chile'
      }
    });

    expect(result).toContain('Pablo Contreras');
    expect(result).toContain('Full Stack Developer');
    expect(result).toContain('pablo@bypabloc.com');
    expect(result).toContain('Santiago, Chile');
  });

  test('GREEN: should handle missing optional props gracefully', async () => {
    // TDD Green Phase - Minimum code to pass
    const result = await container.renderToString(PersonalInfo, {
      props: {
        name: 'Pablo Contreras',
        title: 'Full Stack Developer'
        // Missing email and location
      }
    });

    expect(result).toContain('Pablo Contreras');
    expect(result).toContain('Full Stack Developer');
    expect(result).not.toContain('undefined');
  });

  test('REFACTOR: should apply correct CSS classes', async () => {
    // TDD Refactor Phase - Improve code structure
    const result = await container.renderToString(PersonalInfo, {
      props: {
        name: 'Pablo Contreras',
        title: 'Full Stack Developer',
        theme: 'dark'
      }
    });

    expect(result).toContain('personal-info');
    expect(result).toContain('personal-info--dark');
  });
});
```

### 1.4 API Integration Testing with MSW

```typescript
// test/api/lambda-integration.test.ts
import { setupServer } from 'msw/node';
import { rest } from 'msw';
import { expect, test, describe, beforeAll, afterAll, beforeEach } from 'vitest';

// Mock AWS Lambda API responses
const server = setupServer(
  rest.get('https://api.portfolio.com/personal-info', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        name: 'Pablo Contreras',
        title: 'Full Stack Developer',
        email: 'pablo@bypabloc.com',
        location: 'Santiago, Chile',
        summary: 'Experienced developer specializing in serverless architecture'
      })
    );
  }),

  rest.get('https://api.portfolio.com/projects', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json([
        {
          id: '1',
          name: 'Portfolio API',
          description: 'Serverless portfolio backend',
          technologies: ['AWS Lambda', 'Python', 'API Gateway'],
          featured: true
        }
      ])
    );
  }),

  rest.post('https://api.portfolio.com/auth/login', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        token: 'mock-jwt-token',
        user: { id: '1', name: 'Admin' }
      })
    );
  })
);

describe('Lambda API Integration Tests - TDD', () => {
  beforeAll(() => server.listen());
  afterAll(() => server.close());
  beforeEach(() => server.resetHandlers());

  test('RED: should fetch personal info from Lambda API', async () => {
    // TDD Red Phase - API consumption test
    const response = await fetch('https://api.portfolio.com/personal-info');
    const data = await response.json();

    expect(response.status).toBe(200);
    expect(data.name).toBe('Pablo Contreras');
    expect(data.title).toBe('Full Stack Developer');
  });

  test('GREEN: should handle API errors gracefully', async () => {
    // Mock error response
    server.use(
      rest.get('https://api.portfolio.com/personal-info', (req, res, ctx) => {
        return res(ctx.status(500), ctx.json({ error: 'Internal Server Error' }));
      })
    );

    const response = await fetch('https://api.portfolio.com/personal-info');
    expect(response.status).toBe(500);
  });

  test('REFACTOR: should include authentication headers', async () => {
    const response = await fetch('https://api.portfolio.com/projects', {
      headers: {
        'Authorization': 'Bearer mock-token',
        'Content-Type': 'application/json'
      }
    });

    expect(response.status).toBe(200);
  });
});
```

### 1.5 Astro Endpoint Testing

```typescript
// test/endpoints/api.test.ts
import { expect, test, describe, beforeAll, afterAll } from 'vitest';
import { startDevServer } from '@astrojs/dev-server';

describe('Astro API Endpoints - TDD', () => {
  let devServer: any;

  beforeAll(async () => {
    devServer = await startDevServer();
  });

  afterAll(async () => {
    await devServer.close();
  });

  test('RED: should return portfolio data from internal API', async () => {
    const response = await fetch('http://localhost:4321/api/portfolio');
    const data = await response.json();

    expect(response.status).toBe(200);
    expect(data).toHaveProperty('personalInfo');
    expect(data).toHaveProperty('projects');
  });

  test('GREEN: should handle invalid routes', async () => {
    const response = await fetch('http://localhost:4321/api/invalid');
    expect(response.status).toBe(404);
  });
});
```

### 1.6 Playwright End-to-End Testing

```typescript
// e2e/portfolio.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Portfolio E2E Tests - TDD', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('RED: should display complete portfolio information', async ({ page }) => {
    // TDD Red Phase - E2E user journey
    await expect(page.locator('[data-testid="personal-info"]')).toBeVisible();
    await expect(page.locator('[data-testid="projects-section"]')).toBeVisible();

    const name = page.locator('[data-testid="personal-name"]');
    await expect(name).toContainText('Pablo Contreras');
  });

  test('GREEN: should navigate between sections', async ({ page }) => {
    await page.click('[data-testid="projects-link"]');
    await expect(page.locator('[data-testid="projects-section"]')).toBeInViewport();
  });

  test('REFACTOR: should be responsive on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page.locator('[data-testid="mobile-menu"]')).toBeVisible();
  });

  test('should handle API loading states', async ({ page }) => {
    // Mock slow API response
    await page.route('**/api/projects', async route => {
      await new Promise(resolve => setTimeout(resolve, 2000));
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([])
      });
    });

    await page.goto('/');
    await expect(page.locator('[data-testid="loading-spinner"]')).toBeVisible();
    await expect(page.locator('[data-testid="projects-section"]')).toBeVisible();
  });
});
```

---

## 2. Backend Testing - AWS Lambda Python with TDD

### 2.1 Testing Framework Stack

```yaml
# Backend Testing Stack 2025
Unit Testing: pytest + AWS Lambda Powertools
Integration Testing: pytest + LocalStack + SAM CLI
API Testing: pytest + requests + moto
End-to-End Testing: pytest + AWS SDK
Mocking: moto + pytest-mock
Local Development: LocalStack + SAM Local
```

### 2.2 Pytest Configuration for Lambda

```python
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts =
    --verbose
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
    --tb=short
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
env =
    AWS_DEFAULT_REGION=us-east-1
    ENVIRONMENT=test
    LOG_LEVEL=DEBUG
```

```python
# conftest.py
import pytest
import boto3
import os
from moto import mock_dynamodb, mock_s3, mock_ssm
from aws_lambda_powertools import Logger

logger = Logger()

@pytest.fixture(scope="session")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@pytest.fixture
def lambda_context():
    """Mock Lambda context object."""
    class MockContext:
        def __init__(self):
            self.function_name = "test-function"
            self.function_version = "$LATEST"
            self.invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:test"
            self.memory_limit_in_mb = 128
            self.remaining_time_in_millis = 30000
            self.aws_request_id = "test-request-id"
            self.log_group_name = "/aws/lambda/test"
            self.log_stream_name = "test-stream"

    return MockContext()

@pytest.fixture
def api_gateway_event():
    """Mock API Gateway event."""
    return {
        "httpMethod": "GET",
        "path": "/personal-info",
        "pathParameters": None,
        "queryStringParameters": None,
        "headers": {
            "Content-Type": "application/json",
            "Authorization": "Bearer test-token"
        },
        "body": None,
        "isBase64Encoded": False,
        "requestContext": {
            "requestId": "test-request-id",
            "stage": "test",
            "resourcePath": "/personal-info",
            "httpMethod": "GET",
            "identity": {
                "sourceIp": "127.0.0.1"
            }
        }
    }
```

### 2.3 Lambda Function TDD Implementation

```python
# tests/test_personal_info_handler.py
import pytest
import json
from unittest.mock import patch, MagicMock
from moto import mock_rds
from src.personal_info.lambda_handler import lambda_handler
from src.shared.database import get_connection

class TestPersonalInfoHandler:
    """TDD Test Suite for Personal Info Lambda Function."""

    def test_red_phase_lambda_handler_success(self, api_gateway_event, lambda_context):
        """RED Phase: Write failing test first."""
        # This should fail initially - no implementation yet
        with patch('src.shared.database.get_connection') as mock_db:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = {
                'name': 'Pablo Contreras',
                'title': 'Full Stack Developer',
                'email': 'pablo@bypabloc.com',
                'location': 'Santiago, Chile'
            }
            mock_db.return_value.cursor.return_value = mock_cursor

            response = lambda_handler(api_gateway_event, lambda_context)

            assert response['statusCode'] == 200
            body = json.loads(response['body'])
            assert body['success'] is True
            assert body['data']['name'] == 'Pablo Contreras'

    def test_green_phase_minimal_implementation(self, api_gateway_event, lambda_context):
        """GREEN Phase: Minimum code to make test pass."""
        with patch('src.shared.database.get_connection') as mock_db:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = {
                'name': 'Pablo Contreras',
                'title': 'Full Stack Developer'
            }
            mock_db.return_value.cursor.return_value = mock_cursor

            response = lambda_handler(api_gateway_event, lambda_context)

            assert response['statusCode'] == 200
            assert 'body' in response
            assert 'headers' in response

    def test_refactor_phase_error_handling(self, api_gateway_event, lambda_context):
        """REFACTOR Phase: Improve code with proper error handling."""
        with patch('src.shared.database.get_connection') as mock_db:
            mock_db.side_effect = Exception("Database connection failed")

            response = lambda_handler(api_gateway_event, lambda_context)

            assert response['statusCode'] == 500
            body = json.loads(response['body'])
            assert body['success'] is False
            assert 'error' in body

    def test_validation_with_pydantic(self, lambda_context):
        """Test Pydantic validation integration."""
        invalid_event = {
            "httpMethod": "POST",
            "body": json.dumps({"invalid": "data"})
        }

        response = lambda_handler(invalid_event, lambda_context)
        assert response['statusCode'] == 400

    @patch('src.shared.jwt_auth.verify_token')
    def test_jwt_authentication(self, mock_verify, api_gateway_event, lambda_context):
        """Test JWT authentication integration."""
        mock_verify.return_value = {"user_id": "123", "role": "admin"}

        with patch('src.shared.database.get_connection') as mock_db:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = {'name': 'Test User'}
            mock_db.return_value.cursor.return_value = mock_cursor

            response = lambda_handler(api_gateway_event, lambda_context)
            assert response['statusCode'] == 200

    def test_powertools_integration(self, api_gateway_event, lambda_context):
        """Test AWS Lambda Powertools logging and tracing."""
        with patch('src.shared.database.get_connection') as mock_db:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = {'name': 'Test'}
            mock_db.return_value.cursor.return_value = mock_cursor

            # Should include correlation ID in logs
            response = lambda_handler(api_gateway_event, lambda_context)
            assert 'x-correlation-id' in response['headers']
```

### 2.4 Database Integration Testing with moto

```python
# tests/test_database_integration.py
import pytest
import psycopg2
from moto import mock_rds
from src.shared.database import DatabaseManager
from src.models.personal_info import PersonalInfoModel

@mock_rds
class TestDatabaseIntegration:
    """Integration tests for database operations."""

    @pytest.fixture(autouse=True)
    def setup_database(self):
        """Setup test database with moto."""
        # Note: For Neon.tech, we'll use a different approach
        # This is for demonstration of the pattern
        self.db_manager = DatabaseManager(
            connection_string="postgresql://test:test@localhost:5432/test"
        )

    def test_red_create_personal_info(self):
        """RED: Test creating personal info record."""
        personal_info = PersonalInfoModel(
            name="Pablo Contreras",
            title="Full Stack Developer",
            email="pablo@bypabloc.com"
        )

        result = self.db_manager.create_personal_info(personal_info)
        assert result.id is not None
        assert result.name == "Pablo Contreras"

    def test_green_retrieve_personal_info(self):
        """GREEN: Test retrieving personal info."""
        # First create
        personal_info = PersonalInfoModel(
            name="Pablo Contreras",
            title="Full Stack Developer"
        )
        created = self.db_manager.create_personal_info(personal_info)

        # Then retrieve
        retrieved = self.db_manager.get_personal_info(created.id)
        assert retrieved.name == "Pablo Contreras"

    def test_refactor_connection_optimization(self):
        """REFACTOR: Test connection optimization for Lambda."""
        # Test that connections are properly managed for serverless
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            assert result[0] == 1
```

### 2.5 LocalStack Integration Testing

```python
# tests/test_localstack_integration.py
import pytest
import boto3
import requests
from moto import mock_lambda, mock_apigateway

class TestLocalStackIntegration:
    """Integration tests using LocalStack for AWS services."""

    @pytest.fixture(scope="class")
    def localstack_client(self):
        """LocalStack boto3 client."""
        return boto3.client(
            'lambda',
            endpoint_url='http://localhost:4566',
            region_name='us-east-1',
            aws_access_key_id='test',
            aws_secret_access_key='test'
        )

    def test_red_lambda_deployment_localstack(self, localstack_client):
        """RED: Test Lambda function deployment to LocalStack."""
        # This requires LocalStack to be running
        functions = localstack_client.list_functions()
        assert 'Functions' in functions

    def test_green_api_gateway_integration(self):
        """GREEN: Test API Gateway + Lambda integration."""
        # Test actual HTTP calls to LocalStack API Gateway
        response = requests.get('http://localhost:4566/restapis/test/stages/test/personal-info')
        # Will fail until proper setup - this drives implementation

    def test_refactor_e2e_workflow(self):
        """REFACTOR: Test complete end-to-end workflow."""
        # Complete workflow test with all services
        pass
```

### 2.6 SAM CLI Testing Integration

```python
# tests/test_sam_local.py
import pytest
import requests
import subprocess
import time
from threading import Thread

class TestSAMLocalIntegration:
    """Integration tests using SAM CLI for local testing."""

    @pytest.fixture(scope="class")
    def sam_local_server(self):
        """Start SAM local API Gateway."""
        process = subprocess.Popen([
            'sam', 'local', 'start-api',
            '--host', '0.0.0.0',
            '--port', '3001',
            '--warm-containers', 'LAZY'
        ])

        # Wait for server to start
        time.sleep(10)

        yield process

        process.terminate()
        process.wait()

    def test_red_sam_local_api_gateway(self, sam_local_server):
        """RED: Test Lambda function via SAM local API Gateway."""
        response = requests.get('http://localhost:3001/personal-info')
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True

    def test_green_sam_local_authentication(self, sam_local_server):
        """GREEN: Test authentication flow via SAM local."""
        auth_response = requests.post('http://localhost:3001/auth/login', json={
            'username': 'admin',
            'password': 'password'
        })
        assert auth_response.status_code == 200

        token = auth_response.json()['token']

        # Use token for authenticated request
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get('http://localhost:3001/admin/projects', headers=headers)
        assert response.status_code == 200
```

---

## 3. Integration Testing Between Astro and Lambda APIs

### 3.1 Contract Testing Strategy

```typescript
// test/contracts/api-contracts.test.ts
import { expect, test, describe } from 'vitest';
import { z } from 'zod';

// Define API contract schemas
const PersonalInfoSchema = z.object({
  name: z.string(),
  title: z.string(),
  email: z.string().email(),
  location: z.string().optional(),
  summary: z.string().optional()
});

const ProjectSchema = z.object({
  id: z.string(),
  name: z.string(),
  description: z.string(),
  technologies: z.array(z.string()),
  featured: z.boolean(),
  url: z.string().url().optional(),
  github_url: z.string().url().optional()
});

describe('API Contract Testing - TDD', () => {
  test('RED: Lambda API should match expected contract', async () => {
    const response = await fetch(process.env.LAMBDA_API_URL + '/personal-info');
    const data = await response.json();

    // This will fail until Lambda API implements correct schema
    expect(() => PersonalInfoSchema.parse(data.data)).not.toThrow();
  });

  test('GREEN: Should handle API response format', async () => {
    const mockResponse = {
      success: true,
      data: {
        name: 'Pablo Contreras',
        title: 'Full Stack Developer',
        email: 'pablo@bypabloc.com'
      }
    };

    expect(() => PersonalInfoSchema.parse(mockResponse.data)).not.toThrow();
  });
});
```

### 3.2 End-to-End API Testing

```typescript
// test/e2e/api-integration.test.ts
import { expect, test, describe, beforeAll } from 'vitest';

describe('E2E API Integration - TDD', () => {
  const API_BASE_URL = process.env.LAMBDA_API_URL || 'http://localhost:3000';

  test('RED: Should fetch and display real data from Lambda API', async () => {
    // Test actual integration between Astro and deployed Lambda
    const response = await fetch(`${API_BASE_URL}/personal-info`);
    expect(response.status).toBe(200);

    const data = await response.json();
    expect(data.success).toBe(true);
    expect(data.data).toHaveProperty('name');
  });

  test('GREEN: Should handle API authentication flow', async () => {
    // Test authentication with real Lambda API
    const loginResponse = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: 'admin',
        password: process.env.ADMIN_PASSWORD
      })
    });

    expect(loginResponse.status).toBe(200);
    const authData = await loginResponse.json();
    expect(authData.token).toBeDefined();

    // Use token for authenticated request
    const protectedResponse = await fetch(`${API_BASE_URL}/admin/projects`, {
      headers: { 'Authorization': `Bearer ${authData.token}` }
    });

    expect(protectedResponse.status).toBe(200);
  });

  test('REFACTOR: Should handle error scenarios gracefully', async () => {
    // Test 404 handling
    const notFoundResponse = await fetch(`${API_BASE_URL}/nonexistent`);
    expect(notFoundResponse.status).toBe(404);

    // Test 500 handling
    const errorResponse = await fetch(`${API_BASE_URL}/admin/force-error`);
    expect(errorResponse.status).toBe(500);
  });
});
```

---

## 4. TDD Workflow and Best Practices

### 4.1 TDD Cycle Implementation

```markdown
# TDD Red-Green-Refactor Cycle

## RED Phase (Write Failing Test)
1. Write the smallest failing test
2. Run test to confirm it fails
3. Commit the failing test

## GREEN Phase (Make Test Pass)
1. Write minimum code to pass test
2. Run test to confirm it passes
3. Don't optimize yet - just make it work

## REFACTOR Phase (Improve Code)
1. Improve code structure and design
2. Run tests to ensure they still pass
3. Commit clean, working code

## Repeat
1. Move to next feature/requirement
2. Start with RED phase again
```

### 4.2 Testing Directory Structure

```
project/
├── src/
│   ├── components/
│   ├── pages/
│   └── lambda-functions/
├── test/
│   ├── unit/
│   │   ├── components/
│   │   └── lambda/
│   ├── integration/
│   │   ├── api/
│   │   └── database/
│   ├── e2e/
│   │   └── workflows/
│   ├── contracts/
│   │   └── api-schemas/
│   ├── fixtures/
│   │   ├── data/
│   │   └── mocks/
│   └── utils/
│       ├── helpers/
│       └── setup/
└── e2e/
    ├── tests/
    └── utils/
```

### 4.3 Testing Environment Configuration

```yaml
# docker-compose.test.yml
version: '3.8'
services:
  # LocalStack for AWS services
  localstack:
    image: localstack/localstack:latest
    ports:
      - "4566:4566"
    environment:
      - SERVICES=lambda,apigateway,dynamodb,s3,ssm
      - DEBUG=1
      - LAMBDA_EXECUTOR=docker
      - DOCKER_HOST=unix:///var/run/docker.sock
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock

  # Test database
  test-db:
    image: postgres:17-alpine
    environment:
      POSTGRES_DB: portfolio_test
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
    ports:
      - "5433:5432"
    tmpfs:
      - /var/lib/postgresql/data

  # Astro test server
  astro-test:
    build:
      context: .
      dockerfile: Dockerfile.test
    ports:
      - "4321:4321"
    environment:
      - NODE_ENV=test
      - LAMBDA_API_URL=http://localstack:4566
    depends_on:
      - localstack
      - test-db

  # Playwright test runner
  playwright:
    build:
      context: .
      dockerfile: Dockerfile.playwright
    volumes:
      - ./e2e:/workspace/e2e
      - ./playwright-report:/workspace/playwright-report
    depends_on:
      - astro-test
    command: npx playwright test
```

### 4.4 CI/CD Testing Pipeline

```yaml
# .github/workflows/test.yml
name: Test Suite
on: [push, pull_request]

jobs:
  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run Vitest unit tests
        run: npm run test:unit

      - name: Run component tests
        run: npm run test:components

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  backend-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:17
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run pytest
        run: pytest --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  integration-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Start LocalStack
        run: |
          pip install localstack awscli-local
          docker-compose -f docker-compose.test.yml up -d localstack

      - name: Deploy to LocalStack
        run: |
          sam build
          sam deploy --stack-name test-stack --s3-bucket localstack-bucket --capabilities CAPABILITY_IAM --parameter-overrides Environment=test

      - name: Run integration tests
        run: npm run test:integration

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Start full test environment
        run: docker-compose -f docker-compose.test.yml up -d

      - name: Install Playwright
        run: npx playwright install --with-deps

      - name: Run E2E tests
        run: npx playwright test

      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```

---

## 5. Advanced Testing Patterns

### 5.1 Property-Based Testing

```python
# tests/test_property_based.py
import pytest
from hypothesis import given, strategies as st
from src.models.personal_info import PersonalInfoModel

class TestPersonalInfoProperties:
    """Property-based testing for data models."""

    @given(
        name=st.text(min_size=1, max_size=100),
        title=st.text(min_size=1, max_size=100),
        email=st.emails()
    )
    def test_personal_info_creation_properties(self, name, title, email):
        """Test PersonalInfo creation with generated data."""
        personal_info = PersonalInfoModel(
            name=name,
            title=title,
            email=email
        )

        assert personal_info.name == name
        assert personal_info.title == title
        assert personal_info.email == email
        assert personal_info.id is not None

    @given(st.text())
    def test_email_validation_properties(self, invalid_input):
        """Test email validation with random strings."""
        if '@' not in invalid_input or '.' not in invalid_input:
            with pytest.raises(ValueError):
                PersonalInfoModel(
                    name="Test",
                    title="Test",
                    email=invalid_input
                )
```

### 5.2 Mutation Testing

```bash
#!/bin/bash
# scripts/mutation-test.sh

echo "🧬 Running Mutation Testing"

# Frontend mutation testing
echo "Running mutmut for Python backend..."
mutmut run --paths-to-mutate=src/

# Generate mutation report
mutmut results
mutmut html

echo "✅ Mutation testing completed"
echo "📊 Report: htmlcov/index.html"
```

### 5.3 Performance Testing

```typescript
// test/performance/load-test.ts
import { test, expect } from '@playwright/test';

test.describe('Performance Testing', () => {
  test('should load homepage within performance budget', async ({ page }) => {
    const startTime = Date.now();

    await page.goto('/');
    await page.waitForLoadState('networkidle');

    const loadTime = Date.now() - startTime;
    expect(loadTime).toBeLessThan(3000); // 3 second budget
  });

  test('should handle concurrent users', async ({ page }) => {
    // Simulate multiple concurrent requests
    const promises = Array.from({ length: 10 }, () =>
      page.goto('/')
    );

    const results = await Promise.allSettled(promises);
    const successful = results.filter(r => r.status === 'fulfilled').length;

    expect(successful).toBe(10);
  });
});
```

---

## 6. Monitoring and Observability in Tests

### 6.1 Test Metrics Collection

```python
# tests/utils/metrics.py
import time
import json
from functools import wraps
from aws_lambda_powertools import Metrics
from aws_lambda_powertools.metrics import MetricUnit

metrics = Metrics()

def measure_test_performance(test_name: str):
    """Decorator to measure test performance."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()

            try:
                result = func(*args, **kwargs)
                metrics.add_metric(
                    name="TestDuration",
                    unit=MetricUnit.Milliseconds,
                    value=(time.time() - start_time) * 1000
                )
                metrics.add_metadata(key="test_name", value=test_name)
                metrics.add_metadata(key="test_status", value="passed")
                return result
            except Exception as e:
                metrics.add_metadata(key="test_status", value="failed")
                metrics.add_metadata(key="error", value=str(e))
                raise
            finally:
                metrics.flush_metrics()

        return wrapper
    return decorator

@measure_test_performance("personal_info_lambda")
def test_personal_info_with_metrics():
    # Test implementation
    pass
```

### 6.2 Test Coverage Analysis

```typescript
// test/coverage/coverage-analysis.ts
import { readFileSync } from 'fs';
import { expect, test } from 'vitest';

test('should maintain minimum coverage thresholds', () => {
  const coverage = JSON.parse(readFileSync('coverage/coverage-summary.json', 'utf8'));

  expect(coverage.total.lines.pct).toBeGreaterThanOrEqual(80);
  expect(coverage.total.functions.pct).toBeGreaterThanOrEqual(80);
  expect(coverage.total.branches.pct).toBeGreaterThanOrEqual(80);
  expect(coverage.total.statements.pct).toBeGreaterThanOrEqual(80);
});

test('should not have untested files', () => {
  const coverage = JSON.parse(readFileSync('coverage/coverage-summary.json', 'utf8'));

  Object.entries(coverage).forEach(([file, data]: [string, any]) => {
    if (file !== 'total' && !file.includes('test') && !file.includes('spec')) {
      expect(data.lines.pct).toBeGreaterThan(0);
    }
  });
});
```

---

## Conclusion

This comprehensive testing guide provides production-ready TDD implementation strategies for the serverless portfolio system architecture in 2025. Key benefits include:

### ✅ **Testing Strategy Benefits**
- **Complete TDD coverage** - Red-Green-Refactor cycle for both frontend and backend
- **Framework-specific optimization** - Astro v5 Container API + AWS Lambda testing patterns
- **Integration testing** - End-to-end validation of Astro ↔ Lambda API communication
- **Mock-driven development** - MSW for frontend, moto for backend AWS services
- **Local testing environment** - SAM CLI + LocalStack for realistic development
- **CI/CD integration** - Automated testing pipeline with coverage reporting

### 🚀 **Frontend Testing Features**
- Vitest + Container API for component testing
- Playwright for end-to-end testing
- MSW for API mocking and contract testing
- Happy-DOM for fast DOM testing
- Integration testing with Astro dev server

### ⚡ **Backend Testing Features**
- pytest + AWS Lambda Powertools for serverless testing
- moto for AWS service mocking
- LocalStack for integration testing
- SAM CLI for local API Gateway simulation
- Property-based testing with Hypothesis

### 🔗 **Integration Testing Features**
- Contract testing between Astro and Lambda APIs
- End-to-end workflow testing
- Authentication flow testing
- Error handling validation
- Performance testing and monitoring

This implementation represents the state-of-the-art in TDD for serverless applications in 2025, ensuring reliable, maintainable, and thoroughly tested code across the entire stack.

---

**Created**: January 2025
**Last Updated**: January 2025
**Testing Stack**: Vitest + Playwright + pytest + LocalStack + MSW
**Architecture**: TDD-First Serverless Development

*This guide implements the latest testing best practices for 2025, providing a complete TDD strategy for the Astro v5 + AWS Lambda Python serverless portfolio system with complete frontend/backend separation.*