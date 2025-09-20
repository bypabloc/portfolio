"""
Personal Info Service - FastAPI Application
Portfolio Serverless System

Main application factory and route definitions
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
import logging

from models import PersonalInfoResponse, PersonalInfoUpdate, ContactInfoResponse
from repository import PersonalInfoRepositoryWrapper
from service import PersonalInfoService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """
    Create and configure FastAPI application

    Returns:
        FastAPI: Configured application instance
    """
    app = FastAPI(
        title="Personal Info Service",
        description="Portfolio Serverless System - Personal Information Management",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Dependency injection
    def get_repository() -> PersonalInfoRepositoryWrapper:
        return PersonalInfoRepositoryWrapper()

    def get_service(repository: PersonalInfoRepositoryWrapper = Depends(get_repository)) -> PersonalInfoService:
        return PersonalInfoService(repository)

    @app.get("/", response_model=Dict[str, str])
    async def root():
        """Root endpoint"""
        return {
            "service": "personal-info",
            "status": "running",
            "version": "1.0.0"
        }

    @app.get("/health", response_model=Dict[str, str])
    async def health_check():
        """Health check endpoint for container orchestration"""
        return {
            "status": "healthy",
            "service": "personal-info",
            "version": "1.0.0"
        }

    @app.get("/personal-info", response_model=PersonalInfoResponse)
    async def get_personal_info(
        service: PersonalInfoService = Depends(get_service)
    ):
        """
        Get personal information

        Returns:
            PersonalInfoResponse: Personal information data
        """
        try:
            personal_info = await service.get_personal_info()
            if not personal_info:
                raise HTTPException(
                    status_code=404,
                    detail="Personal information not found"
                )
            return personal_info

        except Exception as e:
            logger.error(f"Error retrieving personal info: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Internal server error"
            )

    @app.put("/personal-info", response_model=PersonalInfoResponse)
    async def update_personal_info(
        update_data: PersonalInfoUpdate,
        service: PersonalInfoService = Depends(get_service)
    ):
        """
        Update personal information

        Args:
            update_data: Personal information update data

        Returns:
            PersonalInfoResponse: Updated personal information
        """
        try:
            updated_info = await service.update_personal_info(update_data)
            return updated_info

        except Exception as e:
            logger.error(f"Error updating personal info: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Internal server error"
            )

    @app.get("/personal-info/contact", response_model=ContactInfoResponse)
    async def get_contact_info(
        service: PersonalInfoService = Depends(get_service)
    ):
        """
        Get contact information only

        Returns:
            ContactInfoResponse: Contact information (email, phone, social links)
        """
        try:
            contact_info = await service.get_contact_info()
            return contact_info

        except Exception as e:
            logger.error(f"Error retrieving contact info: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Internal server error"
            )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        """Custom HTTP exception handler"""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail,
                "status_code": exc.status_code,
                "service": "personal-info"
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        """General exception handler"""
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "status_code": 500,
                "service": "personal-info"
            }
        )

    return app