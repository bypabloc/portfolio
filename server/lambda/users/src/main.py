"""
Users Service - FastAPI Application

Consumes shared models and database from server/shared/.

:Authors:
    - Pablo Contreras

:Created:
    - 2025-01-19
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from shared.logger import logger
import os

# ============================================================================
# Import from shared/ - Only HealthResponse for health endpoint
# ============================================================================

from shared.models import HealthResponse

# Import routers
from routers import users

# ============================================================================
# Lifespan Management
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan - minimal setup for Lambda.

    Database initialization is handled by repositories on first use.
    """
    # Startup
    logger.info("Users API starting up")

    yield

    # Shutdown
    logger.info("Users API shutting down")


# ============================================================================
# FastAPI Application
# ============================================================================

app = FastAPI(
    title="Users API",
    description="User management service using shared SQLModel models",
    version="1.0.0",
    docs_url="/docs" if os.getenv("ENVIRONMENT") != "prod" else None,
    redoc_url="/redoc" if os.getenv("ENVIRONMENT") != "prod" else None,
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/v1", tags=["users"])


# ============================================================================
# Health Check
# ============================================================================

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    from datetime import datetime
    
    return HealthResponse(
        status="healthy",
        service="users-api",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
        database="PostgreSQL via shared/database"
    )
