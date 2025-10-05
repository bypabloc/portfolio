"""
FastAPI application for Projects service.

Uses shared SQLModel models for projects.

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

from shared.models import HealthResponse
from routers import projects



@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage FastAPI application lifecycle."""
    logger.info("Projects Lambda starting up")
    yield
    logger.info("Projects Lambda shutting down")


app = FastAPI(
    title="Projects API",
    description="Manages portfolio projects",
    version="1.0.0",
    docs_url="/docs" if os.getenv("ENVIRONMENT") == "dev" else None,
    redoc_url="/redoc" if os.getenv("ENVIRONMENT") == "dev" else None,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router, prefix="/api/v1", tags=["projects"])


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for Lambda function."""
    return HealthResponse(
        status="healthy",
        service="projects-api",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
        database="SQLModel + AsyncPG"
    )
