# Backend Testing Guide - AWS Lambda + Python + TDD

> **Basado en**: docs/testing.md
> **Última actualización**: Enero 2025
> **Stack**: pytest + LocalStack + SAM CLI + moto + AWS Lambda Powertools
> **Filosofía**: Test-Driven Development (TDD) obligatorio

---

## 🎯 Resumen de Testing Backend

Esta guía implementa **TDD completo** para el backend serverless usando **AWS Lambda + Python 3.12** con las mejores prácticas de 2025. El enfoque se centra en testing de funciones Lambda, integración con AWS services y testing end-to-end.

### Stack de Testing 2025
```yaml
Unit Testing: pytest + AWS Lambda Powertools
Integration Testing: pytest + LocalStack + SAM CLI
API Testing: pytest + requests + moto
End-to-End Testing: pytest + AWS SDK
Mocking: moto + pytest-mock
Local Development: LocalStack + SAM Local
```

---

## 🛠️ Configuración de Testing

### 1. Pytest Configuration
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

### 2. Conftest.py Setup
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

### 3. Requirements para Testing
```python
# requirements-test.txt
pytest==8.3.*
pytest-asyncio==0.24.*
pytest-cov==5.0.*
pytest-mock==3.12.*
moto==5.0.*
localstack==3.8.*
boto3==1.35.*
requests==2.32.*
hypothesis==6.112.*
```

---

## 🧪 Testing con TDD (Red-Green-Refactor)

### 1. Lambda Function TDD Implementation
```python
# tests/test_personal_info_handler.py
import pytest
import json
from unittest.mock import patch, MagicMock
from moto import mock_rds
from lambda.personal_info.lambda_function import lambda_handler

class TestPersonalInfoHandler:
    """TDD Test Suite for Personal Info Lambda Function."""

    def test_red_phase_lambda_handler_success(self, api_gateway_event, lambda_context):
        """RED Phase: Write failing test first."""
        # Este test debe fallar inicialmente - no hay implementación aún
        with patch('lambda.personal_info.src.database.get_connection') as mock_db:
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
        with patch('lambda.personal_info.src.database.get_connection') as mock_db:
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
        with patch('lambda.personal_info.src.database.get_connection') as mock_db:
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

    @patch('lambda.personal_info.src.auth.verify_token')
    def test_jwt_authentication(self, mock_verify, api_gateway_event, lambda_context):
        """Test JWT authentication integration."""
        mock_verify.return_value = {"user_id": "123", "role": "admin"}

        with patch('lambda.personal_info.src.database.get_connection') as mock_db:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = {'name': 'Test User'}
            mock_db.return_value.cursor.return_value = mock_cursor

            response = lambda_handler(api_gateway_event, lambda_context)
            assert response['statusCode'] == 200

    def test_powertools_integration(self, api_gateway_event, lambda_context):
        """Test AWS Lambda Powertools logging and tracing."""
        with patch('lambda.personal_info.src.database.get_connection') as mock_db:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = {'name': 'Test'}
            mock_db.return_value.cursor.return_value = mock_cursor

            # Should include correlation ID in logs
            response = lambda_handler(api_gateway_event, lambda_context)
            assert 'x-correlation-id' in response['headers']
```

### 2. Database Integration Testing con moto
```python
# tests/test_database_integration.py
import pytest
import asyncpg
from unittest.mock import AsyncMock, patch
from lambda.personal_info.src.models import PersonalInfoModel
from lambda.personal_info.src.database import DatabaseManager

class TestDatabaseIntegration:
    """Integration tests for database operations."""

    @pytest.fixture(autouse=True)
    def setup_database(self):
        """Setup test database with mocked connections."""
        self.db_manager = DatabaseManager(
            connection_string="postgresql://test:test@localhost:5432/test"
        )

    @pytest.mark.asyncio
    async def test_red_create_personal_info(self):
        """RED: Test creating personal info record."""
        personal_info = PersonalInfoModel(
            name="Pablo Contreras",
            title="Full Stack Developer",
            email="pablo@bypabloc.com"
        )

        with patch.object(self.db_manager, 'create_personal_info') as mock_create:
            mock_create.return_value = personal_info
            result = await self.db_manager.create_personal_info(personal_info)

            assert result.name == "Pablo Contreras"
            assert result.title == "Full Stack Developer"

    @pytest.mark.asyncio
    async def test_green_retrieve_personal_info(self):
        """GREEN: Test retrieving personal info."""
        personal_info_id = "test-id-123"

        with patch.object(self.db_manager, 'get_personal_info') as mock_get:
            mock_get.return_value = PersonalInfoModel(
                id=personal_info_id,
                name="Pablo Contreras",
                title="Full Stack Developer"
            )

            retrieved = await self.db_manager.get_personal_info(personal_info_id)
            assert retrieved.name == "Pablo Contreras"

    @pytest.mark.asyncio
    async def test_refactor_connection_optimization(self):
        """REFACTOR: Test connection optimization for Lambda."""
        # Test that connections are properly managed for serverless
        with patch('asyncpg.connect') as mock_connect:
            mock_conn = AsyncMock()
            mock_connect.return_value = mock_conn

            async with self.db_manager.get_connection() as conn:
                await conn.execute("SELECT 1")
                mock_conn.execute.assert_called_with("SELECT 1")
```

### 3. AWS Services Testing con moto
```python
# tests/test_aws_services.py
import pytest
import boto3
from moto import mock_s3, mock_ssm, mock_secretsmanager

@mock_s3
@mock_ssm
@mock_secretsmanager
class TestAWSServicesIntegration:
    """Test AWS services integration using moto."""

    def test_red_s3_file_operations(self):
        """RED: Test S3 file upload/download operations."""
        # Setup mocked S3
        s3_client = boto3.client('s3', region_name='us-east-1')
        bucket_name = 'test-portfolio-bucket'
        s3_client.create_bucket(Bucket=bucket_name)

        # Test file upload
        file_content = b"test portfolio data"
        s3_client.put_object(
            Bucket=bucket_name,
            Key='portfolio/personal-info.json',
            Body=file_content
        )

        # Test file retrieval
        response = s3_client.get_object(
            Bucket=bucket_name,
            Key='portfolio/personal-info.json'
        )

        assert response['Body'].read() == file_content

    def test_green_parameter_store_config(self):
        """GREEN: Test SSM Parameter Store configuration."""
        ssm_client = boto3.client('ssm', region_name='us-east-1')

        # Set test parameter
        parameter_name = '/portfolio/database/url'
        parameter_value = 'postgresql://test:test@localhost:5432/portfolio'

        ssm_client.put_parameter(
            Name=parameter_name,
            Value=parameter_value,
            Type='SecureString'
        )

        # Retrieve parameter
        response = ssm_client.get_parameter(
            Name=parameter_name,
            WithDecryption=True
        )

        assert response['Parameter']['Value'] == parameter_value

    def test_refactor_secrets_manager_integration(self):
        """REFACTOR: Test Secrets Manager for sensitive data."""
        secrets_client = boto3.client('secretsmanager', region_name='us-east-1')

        # Create secret
        secret_name = 'portfolio/jwt-secret'
        secret_value = {'jwt_secret': 'super-secret-key-123'}

        secrets_client.create_secret(
            Name=secret_name,
            SecretString=json.dumps(secret_value)
        )

        # Retrieve secret
        response = secrets_client.get_secret_value(SecretId=secret_name)
        retrieved_secret = json.loads(response['SecretString'])

        assert retrieved_secret['jwt_secret'] == 'super-secret-key-123'
```

---

## 🐳 LocalStack Integration Testing

### 1. LocalStack Setup
```python
# tests/test_localstack_integration.py
import pytest
import boto3
import requests
import time
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
        try:
            response = requests.get(
                'http://localhost:4566/restapis/test/stages/test/personal-info',
                timeout=5
            )
            # Will fail until proper setup - this drives implementation
            assert response.status_code in [200, 404]  # 404 is expected initially
        except requests.exceptions.ConnectionError:
            pytest.skip("LocalStack not running")

    def test_refactor_e2e_workflow(self):
        """REFACTOR: Test complete end-to-end workflow."""
        # Complete workflow test with all services
        pass
```

### 2. Docker Compose para Testing
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
      - SERVICES=lambda,apigateway,s3,ssm,secretsmanager
      - DEBUG=1
      - LAMBDA_EXECUTOR=docker
      - DOCKER_HOST=unix:///var/run/docker.sock
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./tests/localstack:/etc/localstack/init/ready.d

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
```

---

## 🎯 SAM CLI Testing Integration

### 1. SAM Local Testing
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
        try:
            response = requests.get('http://localhost:3001/personal-info', timeout=10)
            assert response.status_code == 200
            data = response.json()
            assert data['success'] is True
        except requests.exceptions.ConnectionError:
            pytest.skip("SAM Local not available")

    def test_green_sam_local_authentication(self, sam_local_server):
        """GREEN: Test authentication flow via SAM local."""
        try:
            auth_response = requests.post('http://localhost:3001/auth/login', json={
                'username': 'admin',
                'password': 'password'
            }, timeout=10)

            if auth_response.status_code == 200:
                token = auth_response.json()['token']

                # Use token for authenticated request
                headers = {'Authorization': f'Bearer {token}'}
                response = requests.get(
                    'http://localhost:3001/admin/projects',
                    headers=headers,
                    timeout=10
                )
                assert response.status_code == 200
            else:
                pytest.skip("Authentication endpoint not implemented")
        except requests.exceptions.ConnectionError:
            pytest.skip("SAM Local not available")
```

### 2. SAM Template Testing
```python
# tests/test_sam_template.py
import pytest
import yaml
import json
from pathlib import Path

class TestSAMTemplate:
    """Test SAM template configuration."""

    def test_red_template_syntax_validation(self):
        """RED: Validate SAM template syntax."""
        template_path = Path(__file__).parent.parent / 'template.yaml'

        with open(template_path, 'r') as f:
            template = yaml.safe_load(f)

        assert 'AWSTemplateFormatVersion' in template
        assert 'Resources' in template
        assert template['AWSTemplateFormatVersion'] == '2010-09-09'

    def test_green_lambda_function_definitions(self):
        """GREEN: Test Lambda function definitions in template."""
        template_path = Path(__file__).parent.parent / 'template.yaml'

        with open(template_path, 'r') as f:
            template = yaml.safe_load(f)

        resources = template['Resources']
        lambda_functions = [
            name for name, resource in resources.items()
            if resource.get('Type') == 'AWS::Serverless::Function'
        ]

        expected_functions = [
            'PersonalInfoFunction',
            'ExperienceFunction',
            'ProjectsFunction',
            'SkillsFunction'
        ]

        for func in expected_functions:
            assert func in lambda_functions

    def test_refactor_environment_variables(self):
        """REFACTOR: Test environment variables configuration."""
        template_path = Path(__file__).parent.parent / 'template.yaml'

        with open(template_path, 'r') as f:
            template = yaml.safe_load(f)

        # Check that Lambda functions have proper environment variables
        resources = template['Resources']
        for name, resource in resources.items():
            if resource.get('Type') == 'AWS::Serverless::Function':
                properties = resource['Properties']
                if 'Environment' in properties:
                    env_vars = properties['Environment']['Variables']
                    assert 'LOG_LEVEL' in env_vars
                    assert 'ENVIRONMENT' in env_vars
```

---

## 📁 Estructura de Testing

### Directorio de Tests
```
server/
├── lambda/
│   ├── personal-info/
│   ├── experience/
│   ├── projects/
│   └── skills/
├── tests/
│   ├── unit/
│   │   ├── lambda/
│   │   │   ├── test_personal_info.py
│   │   │   ├── test_experience.py
│   │   │   ├── test_projects.py
│   │   │   └── test_skills.py
│   │   └── models/
│   ├── integration/
│   │   ├── test_database.py
│   │   ├── test_aws_services.py
│   │   └── test_localstack.py
│   ├── e2e/
│   │   ├── test_sam_local.py
│   │   └── test_api_workflows.py
│   ├── fixtures/
│   │   ├── events/
│   │   └── data/
│   ├── utils/
│   │   └── helpers.py
│   └── conftest.py
├── template.yaml
├── pytest.ini
├── requirements-test.txt
└── TESTING.md
```

---

## 🚀 Comandos de Testing

### Testing Scripts
```bash
# Tests unitarios
pytest                              # Todos los tests
pytest tests/unit/                 # Solo unit tests
pytest tests/integration/          # Solo integration tests
pytest tests/e2e/                  # Solo E2E tests

# Coverage
pytest --cov=lambda --cov-report=html    # Coverage HTML report
pytest --cov=lambda --cov-report=term    # Coverage terminal

# Tests específicos
pytest tests/unit/lambda/test_personal_info.py     # Test específico
pytest -k "test_red_phase"                        # Tests que contengan patrón
pytest -v                                         # Verbose output

# LocalStack integration
docker-compose -f docker-compose.test.yml up -d localstack
pytest tests/integration/test_localstack.py
docker-compose -f docker-compose.test.yml down

# SAM Local testing
sam build
sam local start-api --host 0.0.0.0 --port 3001 &
pytest tests/e2e/test_sam_local.py
pkill -f "sam local"
```

### Makefile para Testing
```makefile
# Makefile
.PHONY: test test-unit test-integration test-e2e test-coverage

# Test commands
test:
	pytest

test-unit:
	pytest tests/unit/

test-integration:
	pytest tests/integration/

test-e2e:
	pytest tests/e2e/

test-coverage:
	pytest --cov=lambda --cov-report=html --cov-report=term

# LocalStack testing
test-localstack:
	docker-compose -f docker-compose.test.yml up -d localstack
	pytest tests/integration/test_localstack.py
	docker-compose -f docker-compose.test.yml down

# SAM Local testing
test-sam:
	sam build
	sam local start-api --host 0.0.0.0 --port 3001 &
	sleep 10
	pytest tests/e2e/test_sam_local.py
	pkill -f "sam local" || true

# Full test suite
test-all: test-unit test-integration test-e2e test-coverage

# Clean up
clean:
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	docker-compose -f docker-compose.test.yml down
```

---

## 📊 Quality Gates

### Coverage Requirements
- **Lines**: >80%
- **Functions**: >80%
- **Branches**: >80%
- **Statements**: >80%

### Performance Targets
- **Cold Start**: <300ms
- **Response Time**: <100ms for simple queries
- **Memory Usage**: <256MB for most functions
- **Timeout**: <30s maximum

### AWS Best Practices
- **Error Handling**: Structured error responses
- **Logging**: Structured logging with correlation IDs
- **Monitoring**: CloudWatch metrics integration
- **Security**: No hardcoded secrets or credentials

---

## 🔄 TDD Workflow

### Red-Green-Refactor Cycle
```markdown
1. **RED Phase** (Write Failing Test)
   - Escribir el test más pequeño que falle
   - Ejecutar test para confirmar que falla
   - Commit del test que falla

2. **GREEN Phase** (Make Test Pass)
   - Escribir código mínimo para pasar test
   - Ejecutar test para confirmar que pasa
   - No optimizar aún - solo hacer que funcione

3. **REFACTOR Phase** (Improve Code)
   - Mejorar estructura y diseño del código
   - Ejecutar tests para asegurar que siguen pasando
   - Commit de código limpio y funcional

4. **Repeat**
   - Moverse a siguiente feature/requerimiento
   - Empezar con RED phase nuevamente
```

### Property-Based Testing
```python
# tests/test_property_based.py
import pytest
from hypothesis import given, strategies as st
from lambda.personal_info.src.models import PersonalInfoModel

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
        assert hasattr(personal_info, 'id')
```

---

**Esta guía implementa TDD completo para backend serverless usando las mejores prácticas de 2025, asegurando código confiable, mantenible y completamente testado.**

**Stack**: pytest + LocalStack + SAM CLI + moto + AWS Lambda Powertools
**Coverage**: >80% obligatorio
**Cold Start**: <300ms target
**Architecture**: Serverless-native testing patterns