"""
FastAPI application for Experience service.

Uses shared SQLModel models for works, employers, and job_types.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/01/19
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from shared.logger import logger
from datetime import datetime
import os

# Import shared models
from shared.models import HealthResponse

# Import routers
from routers import works, employers, job_types

# AWS Lambda Powertools


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage FastAPI application lifecycle.

    Note: In Lambda, this runs only on cold starts.
    """
    # Startup
    logger.info("Experience Lambda starting up")
    yield
    # Shutdown
    logger.info("Experience Lambda shutting down")


# FastAPI app configuration
app = FastAPI(
    title="Experience API",
    description="Manages professional work experience, employers, and job types",
    version="1.0.0",
    docs_url="/docs" if os.getenv("ENVIRONMENT") == "dev" else None,
    redoc_url="/redoc" if os.getenv("ENVIRONMENT") == "dev" else None,
    lifespan=lifespan
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(works.router, prefix="/api/v1", tags=["works"])
app.include_router(employers.router, prefix="/api/v1", tags=["employers"])
app.include_router(job_types.router, prefix="/api/v1", tags=["job-types"])


# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for Lambda function."""
    return HealthResponse(
        status="healthy",
        service="experience-api",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
        database="SQLModel + AsyncPG"
    )
