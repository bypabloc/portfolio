# Neon Database + FastAPI Lambda Integration Guide - 2025

> **Comprehensive guide for Neon serverless PostgreSQL with FastAPI + AWS Lambda integration, optimized connections, and serverless best practices.**

## 🚀 What is Neon for FastAPI Lambda?

Neon is a **serverless PostgreSQL platform** perfectly suited for FastAPI + AWS Lambda due to its:
- ✅ **Serverless architecture** - Scales with your Lambda functions
- ✅ **Database branching** - Git-like workflow for development
- ✅ **Scale-to-zero compatibility** - Matches Lambda's scaling pattern
- ✅ **Connection optimization** - Works well with Lambda's stateless nature
- ✅ **Instant wake-up** - Fast cold starts for database connections
- ✅ **AsyncPG compatibility** - Perfect for FastAPI async operations

---

## 📋 Quick Start Guide for FastAPI Lambda Development

### 1. Account Setup & Lambda-Optimized Database

1. **Sign up**: Visit [neon.tech](https://neon.tech) and create free account
2. **Free tier for serverless development**:
   - 3GB storage (perfect for portfolio/CV data)
   - 191.9 compute hours/month (ideal for Lambda workloads)
   - 20 projects (separate environments)
   - Unlimited database branches (feature development)

3. **FastAPI Lambda-optimized structure** after signup:
   ```
   Project
   ├── production (primary branch) → Live FastAPI Lambda functions
   ├── staging (child branch) → Pre-production testing
   └── development (child branch) → Local FastAPI development
   ```

### 2. FastAPI Lambda Connection Configuration

**Connection string format optimized for AsyncPG + Lambda:**
```bash
postgresql://[user]:[password]@[host]/[database]?sslmode=require&connect_timeout=10&command_timeout=30
```

**Environment variables for FastAPI Lambda deployment:**
```env
# Primary connection (stored in AWS Systems Manager Parameter Store)
DATABASE_URL="postgresql://alex:AbC123dEf@ep-cool-darkness-123456.us-east-2.aws.neon.tech/dbname?sslmode=require&connect_timeout=10&command_timeout=30"

# Alternative: Separate components for flexibility
PGHOST="ep-cool-darkness-123456.us-east-2.aws.neon.tech"
PGDATABASE="neondb"
PGUSER="alex"
PGPASSWORD="AbC123dEf"
PGPORT="5432"
PGSSLMODE="require"
```

**SAM template environment configuration:**
```yaml
# template.yaml
Globals:
  Function:
    Environment:
      Variables:
        DATABASE_URL: !Ref DatabaseUrl
        ENVIRONMENT: !Ref Environment
        POWERTOOLS_SERVICE_NAME: portfolio-api

Parameters:
  DatabaseUrl:
    Type: String
    Description: Neon.tech database connection string
    NoEcho: true
  Environment:
    Type: String
    Default: dev
    AllowedValues: [dev, staging, prod]
```

### 3. FastAPI Database Integration

**AsyncPG Database Manager for FastAPI Lambda:**
```python
# app/database.py
import asyncpg
import os
from typing import Optional, Dict, Any, List
from aws_lambda_powertools import Logger
from functools import lru_cache

logger = Logger()

class NeonDatabase:
    """Async database connection manager optimized for FastAPI Lambda + Neon."""

    def __init__(self):
        self.connection_string = os.getenv("DATABASE_URL")
        if not self.connection_string:
            raise ValueError("DATABASE_URL environment variable is required")

    async def get_connection(self):
        """Get optimized database connection for FastAPI Lambda + Neon."""
        try:
            connection = await asyncpg.connect(
                self.connection_string,
                command_timeout=30,
                server_settings={
                    'application_name': 'portfolio-fastapi-lambda',
                    'jit': 'off',  # Disable JIT for faster Neon connection
                    'shared_preload_libraries': ''  # Optimize for Neon
                }
            )
            return connection
        except Exception as e:
            logger.error(f"Neon database connection error: {str(e)}")
            raise

    async def execute_query(self, query: str, *args) -> List[Dict[str, Any]]:
        """Execute query with Neon-optimized error handling."""
        async with await self.get_connection() as conn:
            try:
                result = await conn.fetch(query, *args)
                return [dict(row) for row in result]
            except Exception as e:
                logger.error(f"Neon query execution error: {str(e)}", extra={"query": query})
                raise

    async def execute_one(self, query: str, *args) -> Optional[Dict[str, Any]]:
        """Execute query returning single row from Neon."""
        async with await self.get_connection() as conn:
            try:
                result = await conn.fetchrow(query, *args)
                return dict(result) if result else None
            except Exception as e:
                logger.error(f"Neon query execution error: {str(e)}", extra={"query": query})
                raise

    async def execute_transaction(self, queries: List[tuple]) -> bool:
        """Execute multiple queries in transaction for Neon consistency."""
        async with await self.get_connection() as conn:
            async with conn.transaction():
                try:
                    for query, args in queries:
                        await conn.execute(query, *args)
                    return True
                except Exception as e:
                    logger.error(f"Neon transaction error: {str(e)}")
                    raise

# Dependency for FastAPI
@lru_cache()
def get_neon_database():
    """FastAPI dependency for Neon database connection."""
    return NeonDatabase()
```

### 4. FastAPI Routes with Neon Integration

**Personal Info Route with Neon AsyncPG:**
```python
# app/routers/personal.py
from fastapi import APIRouter, HTTPException, Depends
from aws_lambda_powertools import Logger
from typing import Optional

from ..models import PersonalInfo, PersonalInfoUpdate
from ..database import get_neon_database, NeonDatabase

router = APIRouter()
logger = Logger()

@router.get("/personal-info", response_model=PersonalInfo)
async def get_personal_info(db: NeonDatabase = Depends(get_neon_database)):
    """Get personal information from Neon database."""
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

        logger.info("Personal info retrieved from Neon successfully")
        return PersonalInfo(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting personal info from Neon: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/experience", response_model=List[Experience])
async def get_experience(db: NeonDatabase = Depends(get_neon_database)):
    """Get work experience from Neon with technology aggregation."""
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

        logger.info(f"Retrieved {len(results)} experience records from Neon")
        return [Experience(**result) for result in results]
    except Exception as e:
        logger.error(f"Error getting experience from Neon: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/personal-info", response_model=PersonalInfo)
async def update_personal_info(
    update_data: PersonalInfoUpdate,
    db: NeonDatabase = Depends(get_neon_database)
):
    """Update personal information in Neon with optimistic concurrency."""
    try:
        # Build dynamic update query for Neon
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

        logger.info("Personal info updated in Neon successfully")
        return PersonalInfo(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating personal info in Neon: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

### 5. Database Schema for Portfolio System

**Core Tables optimized for Neon + FastAPI:**
```sql
-- Personal Information
CREATE TABLE personal_info (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(50),
    location VARCHAR(255),
    linkedin VARCHAR(255),
    github VARCHAR(255),
    summary TEXT,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Work Experience
CREATE TABLE experience (
    id SERIAL PRIMARY KEY,
    company VARCHAR(255) NOT NULL,
    position VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    description TEXT,
    location VARCHAR(255),
    company_url VARCHAR(255),
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT end_after_start CHECK (end_date IS NULL OR end_date >= start_date)
);

-- Technologies
CREATE TABLE technologies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50) NOT NULL,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Experience-Technologies Many-to-Many
CREATE TABLE experience_technologies (
    experience_id INTEGER REFERENCES experience(id) ON DELETE CASCADE,
    technology_id INTEGER REFERENCES technologies(id) ON DELETE CASCADE,
    PRIMARY KEY (experience_id, technology_id)
);

-- Projects
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    github_url VARCHAR(255),
    demo_url VARCHAR(255),
    featured BOOLEAN DEFAULT false,
    start_date DATE,
    end_date DATE,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Project-Technologies Many-to-Many
CREATE TABLE project_technologies (
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    technology_id INTEGER REFERENCES technologies(id) ON DELETE CASCADE,
    PRIMARY KEY (project_id, technology_id)
);

-- Skills
CREATE TABLE skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    level INTEGER NOT NULL CHECK (level >= 1 AND level <= 5),
    years_experience INTEGER,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for FastAPI query optimization
CREATE INDEX idx_personal_info_active ON personal_info(active);
CREATE INDEX idx_experience_active_start ON experience(active, start_date DESC);
CREATE INDEX idx_projects_featured_active ON projects(featured, active);
CREATE INDEX idx_technologies_category ON technologies(category);
CREATE INDEX idx_skills_category_level ON skills(category, level DESC);
```

### 6. Database Branching Workflow for FastAPI Development

**Development Workflow with Neon Branches:**
```bash
# 1. Create feature branch for new FastAPI endpoint
neon branches create --name feature-new-endpoint --parent main

# 2. Get connection string for development
neon connection-string feature-new-endpoint

# 3. Update local .env for FastAPI development
export DATABASE_URL="postgresql://user:pass@host/db?sslmode=require&branch=feature-new-endpoint"

# 4. Run FastAPI locally with feature branch
uvicorn app.main:app --reload

# 5. Test FastAPI endpoints against feature branch
curl http://localhost:8000/api/personal-info

# 6. Run database migrations on feature branch
python migrate.py --branch feature-new-endpoint

# 7. Deploy FastAPI Lambda with staging branch
sam deploy --parameter-overrides DatabaseUrl=$STAGING_DATABASE_URL

# 8. Merge to production after testing
neon branches merge feature-new-endpoint main
```

### 7. Connection Optimization for FastAPI Lambda

**Optimized Connection Pool for Lambda:**
```python
# app/database.py - Advanced connection management
import asyncpg
import asyncio
from typing import Optional
from functools import lru_cache

class OptimizedNeonDatabase:
    """Production-ready Neon connection manager for FastAPI Lambda."""

    _connection_pool: Optional[asyncpg.Pool] = None

    @classmethod
    async def get_pool(cls) -> asyncpg.Pool:
        """Get or create optimized connection pool for Neon + Lambda."""
        if cls._connection_pool is None or cls._connection_pool.is_closed():
            cls._connection_pool = await asyncpg.create_pool(
                os.getenv("DATABASE_URL"),
                min_size=1,  # Minimal for Lambda
                max_size=3,  # Conservative for Lambda concurrency
                command_timeout=30,
                server_settings={
                    'application_name': 'portfolio-fastapi-lambda',
                    'jit': 'off',  # Faster connections with Neon
                    'shared_preload_libraries': '',
                    'timezone': 'UTC'
                },
                # Neon-specific optimizations
                init=cls._init_connection
            )
        return cls._connection_pool

    @staticmethod
    async def _init_connection(conn):
        """Initialize connection with Neon-specific settings."""
        await conn.execute("SET TIME ZONE 'UTC'")
        await conn.execute("SET statement_timeout = '30s'")

    @classmethod
    async def execute_query(cls, query: str, *args):
        """Execute query with connection pooling for Neon."""
        pool = await cls.get_pool()
        async with pool.acquire() as connection:
            result = await connection.fetch(query, *args)
            return [dict(row) for row in result]

    @classmethod
    async def execute_one(cls, query: str, *args):
        """Execute single-row query with connection pooling."""
        pool = await cls.get_pool()
        async with pool.acquire() as connection:
            result = await connection.fetchrow(query, *args)
            return dict(result) if result else None

    @classmethod
    async def close_pool(cls):
        """Close connection pool gracefully."""
        if cls._connection_pool and not cls._connection_pool.is_closed():
            await cls._connection_pool.close()
```

### 8. Monitoring and Observability

**Neon Database Monitoring for FastAPI Lambda:**
```python
# app/monitoring.py
from aws_lambda_powertools import Logger, Metrics
from aws_lambda_powertools.metrics import MetricUnit
import time
from functools import wraps

logger = Logger()
metrics = Metrics()

def monitor_neon_operations(operation_name: str):
    """Decorator to monitor Neon database operations."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()

            try:
                result = await func(*args, **kwargs)

                # Success metrics
                duration = (time.time() - start_time) * 1000  # ms
                metrics.add_metric(name="NeonOperationDuration", unit=MetricUnit.Milliseconds, value=duration)
                metrics.add_metric(name="NeonOperationSuccess", unit=MetricUnit.Count, value=1)

                logger.info(
                    f"Neon operation successful: {operation_name}",
                    extra={
                        "operation": operation_name,
                        "duration_ms": duration,
                        "status": "success"
                    }
                )

                return result

            except Exception as e:
                # Error metrics
                duration = (time.time() - start_time) * 1000
                metrics.add_metric(name="NeonOperationError", unit=MetricUnit.Count, value=1)

                logger.error(
                    f"Neon operation failed: {operation_name}",
                    extra={
                        "operation": operation_name,
                        "duration_ms": duration,
                        "error": str(e),
                        "status": "error"
                    }
                )
                raise

        return wrapper
    return decorator

# Usage in database operations
@monitor_neon_operations("get_personal_info")
async def get_personal_info_monitored(db: NeonDatabase):
    """Get personal info with monitoring."""
    return await db.execute_one("""
        SELECT * FROM personal_info WHERE active = true
        ORDER BY updated_at DESC LIMIT 1
    """)
```

---

## 🧪 Testing with Neon Database Branching

### Database Testing Strategy

**Test Database Setup with Neon Branches:**
```python
# tests/conftest.py
import pytest
import asyncpg
import os
from app.database import NeonDatabase

@pytest.fixture(scope="session")
async def test_neon_database():
    """Create test database connection using Neon test branch."""
    test_db_url = os.getenv("TEST_DATABASE_URL")  # Neon test branch
    if not test_db_url:
        pytest.skip("TEST_DATABASE_URL not configured for Neon testing")

    # Override database URL for testing
    original_url = os.getenv("DATABASE_URL")
    os.environ["DATABASE_URL"] = test_db_url

    db = NeonDatabase()

    # Setup test schema
    await setup_test_schema(db)

    yield db

    # Cleanup
    await cleanup_test_data(db)
    if original_url:
        os.environ["DATABASE_URL"] = original_url

async def setup_test_schema(db: NeonDatabase):
    """Setup test schema in Neon test branch."""
    schema_queries = [
        """
        CREATE TABLE IF NOT EXISTS personal_info (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            title VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            active BOOLEAN DEFAULT true,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )
        """,
        "CREATE INDEX IF NOT EXISTS idx_personal_info_active ON personal_info(active)"
    ]

    for query in schema_queries:
        await db.execute_query(query)

async def cleanup_test_data(db: NeonDatabase):
    """Clean up test data from Neon test branch."""
    cleanup_queries = [
        "DELETE FROM personal_info WHERE email LIKE '%test%'",
        "DELETE FROM experience WHERE company LIKE '%Test%'"
    ]

    for query in cleanup_queries:
        await db.execute_query(query)
```

### TDD Database Testing

**Database TDD Tests with Neon:**
```python
# tests/test_neon_integration.py
import pytest
from httpx import AsyncClient
from app.main import app

class TestNeonDatabaseIntegration:
    """TDD tests for Neon database integration with FastAPI."""

    @pytest.mark.asyncio
    async def test_red_personal_info_empty_neon_database(self, test_neon_database):
        """RED: Test should fail when Neon database is empty."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/personal-info")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_green_personal_info_basic_neon_data(self, test_neon_database):
        """GREEN: Basic personal info retrieval from Neon."""
        # Insert test data into Neon test branch
        await test_neon_database.execute_query("""
            INSERT INTO personal_info (name, title, email, active)
            VALUES ($1, $2, $3, $4)
        """, "John Doe", "Developer", "john@test.com", True)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/personal-info")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "John Doe"
        assert data["email"] == "john@test.com"

    @pytest.mark.asyncio
    async def test_refactor_personal_info_neon_performance(self, test_neon_database):
        """REFACTOR: Test Neon query performance and optimization."""
        import time

        # Insert multiple records for performance testing
        for i in range(10):
            await test_neon_database.execute_query("""
                INSERT INTO personal_info (name, title, email, active)
                VALUES ($1, $2, $3, $4)
            """, f"User {i}", "Developer", f"user{i}@test.com", True)

        start_time = time.time()

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/personal-info")

        query_time = (time.time() - start_time) * 1000  # ms

        assert response.status_code == 200
        assert query_time < 100  # Should be fast with Neon + proper indexing

        # Verify we get the most recent record (ORDER BY updated_at DESC)
        data = response.json()
        assert "User 9" in data["name"]  # Last inserted record
```

---

## 🎯 Neon Best Practices for FastAPI Lambda

### 1. Connection Management
- Use **connection pooling** with min_size=1, max_size=3 for Lambda
- Set **command_timeout=30** for Neon compatibility
- Disable **JIT** for faster Lambda cold starts
- Use **async context managers** for automatic connection cleanup

### 2. Database Branching Strategy
- **main branch**: Production FastAPI Lambda functions
- **staging branch**: Pre-production testing and integration
- **feature branches**: Individual FastAPI endpoint development
- **test branches**: Automated testing with isolated data

### 3. Query Optimization
- Use **proper indexes** for FastAPI query patterns
- Implement **pagination** for large result sets
- Use **LIMIT** clauses to prevent large data transfers
- Leverage **array_agg** for one-to-many relationships

### 4. Error Handling
- Implement **retry logic** for transient Neon connection issues
- Use **structured logging** with AWS Lambda Powertools
- Monitor **connection pool metrics** for optimization
- Handle **graceful degradation** when Neon is unavailable

### 5. Security Best Practices
- Store **connection strings** in AWS Systems Manager Parameter Store
- Use **SSL/TLS encryption** (sslmode=require)
- Implement **connection string rotation** for production
- Apply **principle of least privilege** for database users

### 6. Performance Monitoring
- Track **query execution times** with CloudWatch metrics
- Monitor **connection pool utilization**
- Set up **alerting** for slow queries (>1000ms)
- Use **Neon console** for query performance analysis

---

**Neon + FastAPI + Lambda** provides a powerful serverless database solution that scales automatically, reduces costs through pay-per-use pricing, and offers excellent developer experience with database branching and instant provisioning for modern portfolio applications.