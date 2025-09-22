"""
Skills Service - FastAPI Application
Portfolio Serverless System

Main application factory and route definitions
"""

# Setup shared imports
# Navigate: src/ → skills/ → lambda/ → server/ → shared/
from pathlib import Path
import sys
shared = Path(__file__).resolve().parents[3] / 'shared'
sys.path.insert(0, str(shared))

# Import shared utilities
from api_core import (
    # FastAPI core
    HTTPException,
    Depends,
    Query,
    # App utilities
    create_fastapi_app,
    create_success_response,
    create_error_response,
    RequestLogger,
    # Query utilities
    CommonQuery
)
from utils.logger import get_logger

from models import SkillsListResponse, SkillsCategoryResponse
from repository import SkillRepositoryWrapper
from service import SkillsService

# Get logger for this service
logger = get_logger("skills-service")

def create_app():
    """
    Create and configure FastAPI application using shared utilities.

    Returns:
        FastAPI: Configured application instance
    """
    app = create_fastapi_app(
        title="Skills Service",
        description="Portfolio Serverless System - Skills Management",
        version="1.0.0",
        service_name="skills-service",
        debug=True  # Change to False for production
    )

    # Dependency injection
    def get_repository() -> SkillRepositoryWrapper:
        return SkillRepositoryWrapper()

    def get_service(repository: SkillRepositoryWrapper = Depends(get_repository)) -> SkillsService:
        return SkillsService(repository)

    @app.get("/")
    async def root():
        """Root endpoint"""
        return create_success_response({
            "service": "skills",
            "status": "running",
            "version": "1.0.0"
        })

    @app.get("/health")
    async def health_check():
        """Health check endpoint for container orchestration"""
        return create_success_response({
            "status": "healthy",
            "service": "skills",
            "version": "1.0.0"
        })

    @app.get("/skills", response_model=SkillsListResponse)
    async def get_skills(
        category: str | None = Query(None, description="Filter by category"),
        level: str | None = Query(None, description="Filter by proficiency level"),
        featured: bool | None = Query(None, description="Filter featured skills only"),
        search: str | None = Query(None, description="Search skills by name or description"),
        skip: int = Query(0, ge=0, description="Number of skills to skip"),
        limit: int = Query(100, ge=1, le=100, description="Maximum number of skills to return"),
        service: SkillsService = Depends(get_service),
        request_logger: RequestLogger = RequestLogger
    ):
        """
        Get skills with various filtering options

        Returns:
            SkillsListResponse: List of skills matching criteria
        """
        try:
            request_logger.info(
                "Processing skills request",
                extra={
                    "category": category,
                    "level": level,
                    "featured": featured,
                    "search": search,
                    "skip": skip,
                    "limit": limit,
                    "event_type": "skills_request"
                }
            )

            # Handle different filtering options
            if search:
                result = await service.search_skills(search)
            elif featured:
                result = await service.get_featured_skills()
            elif category:
                result = await service.get_skills_by_category(category)
            elif level:
                result = await service.get_skills_by_level(level)
            else:
                result = await service.get_all_skills(skip=skip, limit=limit)

            return result

        except ValueError as e:
            request_logger.warning(
                "Skills validation error",
                extra={"error": str(e), "event_type": "validation_error"}
            )
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
        except Exception as e:
            request_logger.error(
                "Error retrieving skills",
                extra={"error": str(e), "event_type": "skills_error"},
                exc_info=True
            )
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
        return create_error_response(
            error=exc.detail,
            error_code="HTTP_ERROR",
            status_code=exc.status_code
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        """General exception handler"""
        logger.exception(
            "Unhandled exception in skills service",
            extra={
                "error": str(exc),
                "service": "skills",
                "event_type": "unhandled_exception"
            }
        )
        return create_error_response(
            error="Internal server error",
            error_code="INTERNAL_ERROR",
            status_code=500
        )

    return app