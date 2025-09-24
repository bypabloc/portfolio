# Database Admin Service - HTTP interface for PostgreSQL management
# Provides REST API endpoints for database administration through API Gateway

FROM python:3.12-alpine

# Install system dependencies
RUN apk add --no-cache \
    postgresql-client \
    curl \
    && rm -rf /var/cache/apk/*

# Set working directory
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn==0.24.0 \
    asyncpg==0.29.0 \
    pydantic==2.5.0 \
    python-multipart==0.0.6

# Create app directory structure
RUN mkdir -p /app/src

# Create the FastAPI application for database administration
RUN cat > /app/src/main.py << 'EOF'
"""
Database Admin Service - HTTP interface for PostgreSQL management
Provides REST API endpoints for secure database access through API Gateway
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
from contextlib import asynccontextmanager

import asyncpg
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel


# Configuration from environment variables
DB_HOST = os.getenv("DB_HOST", "portfolio-db")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "portfolio_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "portfolio_password")

ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "portfolio_admin")

# Security
security = HTTPBasic()

# Global connection pool
pool: Optional[asyncpg.Pool] = None


# Pydantic models
class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: str
    database_connected: bool


class QueryRequest(BaseModel):
    sql: str


class QueryResponse(BaseModel):
    success: bool
    rows: List[Dict[str, Any]]
    row_count: int
    execution_time_ms: float


class DatabaseInfo(BaseModel):
    version: str
    current_database: str
    current_user: str
    total_tables: int
    connection_count: int


class TableInfo(BaseModel):
    table_name: str
    table_schema: str
    table_type: str


class TablesResponse(BaseModel):
    success: bool
    tables: List[TableInfo]
    total_count: int


# Database connection management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage database connection pool lifecycle."""
    global pool
    try:
        # Create connection pool
        pool = await asyncpg.create_pool(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            min_size=2,
            max_size=10
        )
        print(f"Database pool created successfully")
        yield
    except Exception as e:
        print(f"Error creating database pool: {e}")
        yield
    finally:
        if pool:
            await pool.close()
            print("Database pool closed")


# FastAPI app
app = FastAPI(
    title="Portfolio Database Admin API",
    description="HTTP interface for PostgreSQL database administration",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Authentication dependency
def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != ADMIN_USER or credentials.password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials


# Helper functions
async def execute_query(sql: str) -> tuple[List[Dict[str, Any]], float]:
    """Execute SQL query and return results with execution time."""
    if not pool:
        raise HTTPException(status_code=500, detail="Database pool not available")

    start_time = asyncio.get_event_loop().time()

    async with pool.acquire() as connection:
        try:
            rows = await connection.fetch(sql)
            execution_time = (asyncio.get_event_loop().time() - start_time) * 1000

            # Convert asyncpg.Record to dict
            result = [dict(row) for row in rows]
            return result, execution_time
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"SQL execution error: {str(e)}")


# API Endpoints
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    database_connected = False

    if pool:
        try:
            async with pool.acquire() as connection:
                await connection.fetchval("SELECT 1")
                database_connected = True
        except:
            pass

    return HealthResponse(
        status="healthy" if database_connected else "degraded",
        service="portfolio-db-admin",
        timestamp=datetime.utcnow().isoformat(),
        database_connected=database_connected
    )


@app.get("/info", response_model=DatabaseInfo)
async def get_database_info(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    """Get database information."""
    if not pool:
        raise HTTPException(status_code=500, detail="Database pool not available")

    async with pool.acquire() as connection:
        try:
            version = await connection.fetchval("SELECT version()")
            current_db = await connection.fetchval("SELECT current_database()")
            current_user = await connection.fetchval("SELECT current_user")
            table_count = await connection.fetchval(
                "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public'"
            )
            connection_count = await connection.fetchval(
                "SELECT count(*) FROM pg_stat_activity WHERE state = 'active'"
            )

            return DatabaseInfo(
                version=version,
                current_database=current_db,
                current_user=current_user,
                total_tables=table_count,
                connection_count=connection_count
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/tables", response_model=TablesResponse)
async def list_tables(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    """List all tables in the database."""
    sql = """
    SELECT table_name, table_schema, table_type
    FROM information_schema.tables
    WHERE table_schema = 'public'
    ORDER BY table_name
    """

    try:
        rows, _ = await execute_query(sql)
        tables = [TableInfo(**row) for row in rows]

        return TablesResponse(
            success=True,
            tables=tables,
            total_count=len(tables)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing tables: {str(e)}")


@app.get("/tables/{table_name}/schema")
async def get_table_schema(
    table_name: str,
    credentials: HTTPBasicCredentials = Depends(verify_credentials)
):
    """Get schema information for a specific table."""
    sql = """
    SELECT column_name, data_type, is_nullable, column_default
    FROM information_schema.columns
    WHERE table_name = $1 AND table_schema = 'public'
    ORDER BY ordinal_position
    """

    try:
        rows, execution_time = await execute_query(sql.replace('$1', f"'{table_name}'"))

        return {
            "success": True,
            "table_name": table_name,
            "columns": rows,
            "execution_time_ms": execution_time
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting table schema: {str(e)}")


@app.post("/query", response_model=QueryResponse)
async def execute_sql_query(
    query_request: QueryRequest,
    credentials: HTTPBasicCredentials = Depends(verify_credentials)
):
    """Execute a custom SQL query."""
    try:
        rows, execution_time = await execute_query(query_request.sql)

        return QueryResponse(
            success=True,
            rows=rows,
            row_count=len(rows),
            execution_time_ms=execution_time
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Root endpoint for web interface
@app.get("/")
async def admin_interface(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    """Simple web interface for database administration."""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Portfolio Database Admin</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .container {{ max-width: 800px; }}
            .endpoint {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
            .method {{ color: #28a745; font-weight: bold; }}
            code {{ background: #f8f9fa; padding: 2px 5px; border-radius: 3px; }}
            textarea {{ width: 100%; height: 100px; }}
            button {{ padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }}
            .result {{ margin-top: 10px; padding: 10px; background: #f8f9fa; border-radius: 5px; white-space: pre-wrap; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🗄️ Portfolio Database Admin</h1>
            <p><strong>Database:</strong> {DB_NAME} @ {DB_HOST}:{DB_PORT}</p>

            <div class="endpoint">
                <h3><span class="method">GET</span> /health</h3>
                <p>Check database connection health</p>
                <button onclick="fetch('/health').then(r=>r.json()).then(d=>document.getElementById('health-result').textContent=JSON.stringify(d,null,2))">Test Health</button>
                <div id="health-result" class="result"></div>
            </div>

            <div class="endpoint">
                <h3><span class="method">GET</span> /info</h3>
                <p>Get database information</p>
                <button onclick="fetch('/info').then(r=>r.json()).then(d=>document.getElementById('info-result').textContent=JSON.stringify(d,null,2))">Get Info</button>
                <div id="info-result" class="result"></div>
            </div>

            <div class="endpoint">
                <h3><span class="method">GET</span> /tables</h3>
                <p>List all tables</p>
                <button onclick="fetch('/tables').then(r=>r.json()).then(d=>document.getElementById('tables-result').textContent=JSON.stringify(d,null,2))">List Tables</button>
                <div id="tables-result" class="result"></div>
            </div>

            <div class="endpoint">
                <h3><span class="method">POST</span> /query</h3>
                <p>Execute custom SQL query</p>
                <textarea id="sql-input" placeholder="SELECT version();"></textarea><br>
                <button onclick="executeQuery()">Execute Query</button>
                <div id="query-result" class="result"></div>
            </div>

            <script>
                function executeQuery() {{
                    const sql = document.getElementById('sql-input').value;
                    fetch('/query', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{sql: sql}})
                    }})
                    .then(r => r.json())
                    .then(d => document.getElementById('query-result').textContent = JSON.stringify(d, null, 2))
                    .catch(e => document.getElementById('query-result').textContent = 'Error: ' + e.message);
                }}
            </script>
        </div>
    </body>
    </html>
    """

    from fastapi.responses import HTMLResponse
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
EOF

# Create startup script
RUN cat > /app/start.sh << 'EOF'
#!/bin/sh
echo "Starting Portfolio Database Admin Service..."
echo "Database: $DB_HOST:$DB_PORT/$DB_NAME"
echo "Admin credentials: $ADMIN_USER:$ADMIN_PASSWORD"

# Wait for database to be ready
echo "Waiting for database to be ready..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
    echo "Database not ready, waiting..."
    sleep 2
done

echo "Database is ready! Starting FastAPI server..."
cd /app/src && python -m uvicorn main:app --host 0.0.0.0 --port 8080 --log-level info
EOF

RUN chmod +x /app/start.sh

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Start the application
CMD ["/app/start.sh"]