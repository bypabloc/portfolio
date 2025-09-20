"""
Skills Service - FastAPI Application
Portfolio Serverless System

Main application factory and route definitions
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
import logging

from .models import SkillsListResponse, SkillsCategoryResponse
from .repository import SkillRepositoryWrapper
from .service import SkillsService

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
        title="Skills Service",
        description="Portfolio Serverless System - Skills Management",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Dependency injection
    def get_repository() -> SkillRepositoryWrapper:
        return SkillRepositoryWrapper()

    def get_service(repository: SkillRepositoryWrapper = Depends(get_repository)) -> SkillsService:
        return SkillsService(repository)

    @app.get("/", response_model=Dict[str, str])
    async def root():
        """Root endpoint"""
        return {
            "service": "skills",
            "status": "running",
            "version": "1.0.0"
        }

    @app.get("/skills", response_model=SkillsListResponse)
    async def get_skills(
        category: Optional[str] = Query(None, description="Filter by category"),
        level: Optional[str] = Query(None, description="Filter by proficiency level"),
        featured: Optional[bool] = Query(None, description="Filter featured skills only"),
        search: Optional[str] = Query(None, description="Search skills by name or description"),
        skip: int = Query(0, ge=0, description="Number of skills to skip"),
        limit: int = Query(100, ge=1, le=100, description="Maximum number of skills to return"),
        service: SkillsService = Depends(get_service)
    ):
        """
        Get skills with various filtering options

        Returns:
            SkillsListResponse: List of skills matching criteria
        """
        try:
            # Handle different filtering options
            if search:
                return await service.search_skills(search)
            elif featured:
                return await service.get_featured_skills()
            elif category:
                return await service.get_skills_by_category(category)
            elif level:
                return await service.get_skills_by_level(level)
            else:
                return await service.get_all_skills(skip=skip, limit=limit)

        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Error retrieving skills: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Internal server error"
            )

    @app.get("/skills/featured", response_model=SkillsListResponse)
    async def get_featured_skills(
        service: SkillsService = Depends(get_service)
    ):
        """
        Get featured skills only

        Returns:
            SkillsListResponse: Featured skills
        """
        try:
            return await service.get_featured_skills()

        except Exception as e:
            logger.error(f"Error retrieving featured skills: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Internal server error"
            )

    @app.get("/skills/categories", response_model=SkillsCategoryResponse)
    async def get_skills_by_categories(
        service: SkillsService = Depends(get_service)
    ):
        """
        Get skills grouped by category

        Returns:
            SkillsCategoryResponse: Skills grouped by category
        """
        try:
            return await service.get_skills_grouped_by_category()

        except Exception as e:
            logger.error(f"Error retrieving skills by categories: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Internal server error"
            )

    @app.get("/skills/category/{category}", response_model=SkillsListResponse)
    async def get_skills_by_category(
        category: str,
        service: SkillsService = Depends(get_service)
    ):
        """
        Get skills by specific category

        Args:
            category: Category name

        Returns:
            SkillsListResponse: Skills in the specified category
        """
        try:
            return await service.get_skills_by_category(category)

        except Exception as e:
            logger.error(f"Error retrieving skills by category: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Internal server error"
            )

    @app.get("/skills/level/{level}", response_model=SkillsListResponse)
    async def get_skills_by_level(
        level: str,
        service: SkillsService = Depends(get_service)
    ):
        """
        Get skills by proficiency level

        Args:
            level: Proficiency level (beginner, intermediate, advanced, expert)

        Returns:
            SkillsListResponse: Skills at the specified level
        """
        try:
            return await service.get_skills_by_level(level)

        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Error retrieving skills by level: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Internal server error"
            )

    @app.get("/skills/search", response_model=SkillsListResponse)
    async def search_skills(
        q: str = Query(..., min_length=2, description="Search query"),
        service: SkillsService = Depends(get_service)
    ):
        """
        Search skills by name or description

        Args:
            q: Search query (minimum 2 characters)

        Returns:
            SkillsListResponse: Skills matching the search query
        """
        try:
            return await service.search_skills(q)

        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Error searching skills: {str(e)}")
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
                "service": "skills"
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
                "service": "skills"
            }
        )

    return app