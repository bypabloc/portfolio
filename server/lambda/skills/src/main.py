"""
FastAPI application for Skills service.

Uses shared SQLModel models for skills management.

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
from routers import skills



@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage FastAPI application lifecycle."""
    logger.info("Skills Lambda starting up")
    yield
    logger.info("Skills Lambda shutting down")


app = FastAPI(
    title="Skills API",
    description="Manages technical and soft skills",
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

app.include_router(skills.router, prefix="/api/v1", tags=["skills"])


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for Lambda function."""
    return HealthResponse(
        status="healthy",
        service="skills-api",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
        database="SQLModel + AsyncPG"
    )
