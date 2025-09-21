"""
Projects Service - FastAPI Application
Portfolio Serverless System

Simple wrapper around existing lambda_function for development
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from typing import Dict, Any
import logging
import json

from lambda_function import lambda_handler

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
        title="Projects Service",
        description="Portfolio Serverless System - Projects Management",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    @app.get("/", response_model=Dict[str, str])
    async def root():
        """Root endpoint"""
        return {
            "service": "projects",
            "status": "running",
            "version": "1.0.0"
        }

    @app.get("/health", response_model=Dict[str, str])
    async def health_check():
        """Health check endpoint for container orchestration"""
        return {
            "status": "healthy",
            "service": "projects",
            "version": "1.0.0"
        }

    @app.api_route("/projects", methods=["GET", "POST", "PUT", "DELETE"])
    @app.api_route("/projects/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
    async def projects_handler(request: Request, path: str = ""):
        """
        Route all projects requests to lambda handler
        """
        try:
            # Convert FastAPI request to lambda event format
            event = {
                "httpMethod": request.method,
                "path": str(request.url.path),
                "queryStringParameters": dict(request.query_params),
                "headers": dict(request.headers),
                "body": None
            }

            # Add body for POST/PUT requests
            if request.method in ["POST", "PUT"]:
                body = await request.body()
                event["body"] = body.decode() if body else None

            # Mock lambda context
            class MockContext:
                def __init__(self):
                    self.aws_request_id = "mock-request-id"
                    self.function_name = "projects-lambda"

            context = MockContext()

            # Call lambda handler
            response = lambda_handler(event, context)

            # Return FastAPI response
            return JSONResponse(
                content=json.loads(response.get("body", "{}")),
                status_code=response.get("statusCode", 200),
                headers=response.get("headers", {})
            )

        except Exception as e:
            logger.error(f"Error in projects handler: {str(e)}")
            return JSONResponse(
                content={
                    "error": "Internal server error",
                    "service": "projects"
                },
                status_code=500
            )

    return app