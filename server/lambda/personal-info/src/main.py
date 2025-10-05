"""
FastAPI application for Personal Info service.

Uses shared SQLModel models for users and user_attributes with EAV pattern.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/01/19
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os

# Import shared models
from shared.models import HealthResponse

# Import routers
from routers import users

# Custom logger
from shared.logger import logger



@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage FastAPI application lifecycle.

    Note: In Lambda, this runs only on cold starts.
    """
    # Startup
    logger.info("Personal Info Lambda starting up")
    yield
    # Shutdown
    logger.info("Personal Info Lambda shutting down")


# FastAPI app configuration
app = FastAPI(
    title="Personal Info API",
    description="Manages user information and attributes using EAV pattern",
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
app.include_router(users.router, prefix="/personal-info", tags=["users"])


# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for Lambda function."""
    return HealthResponse(
        status="healthy",
        service="personal-info-api",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
        database="SQLModel + AsyncPG"
    )
