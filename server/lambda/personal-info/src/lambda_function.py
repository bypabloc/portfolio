"""
Personal Info Lambda Function
Portfolio Serverless System - Personal Information Service

FastAPI + AWS Lambda handler with Mangum adapter
Handles personal information CRUD operations
"""

import json
import logging
from typing import Dict, Any

from mangum import Mangum
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.metrics import MetricUnit

import main

# Initialize AWS Lambda Powertools
logger = Logger(service="personal-info")
tracer = Tracer(service="personal-info")
metrics = Metrics(namespace="portfolio-system", service="personal-info")

# Create FastAPI application
app = main.create_app()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Lambda Powertools middleware
@app.middleware("http")
async def add_correlation_id(request, call_next):
    """Add correlation ID for tracing"""
    correlation_id = request.headers.get("x-correlation-id", "unknown")
    logger.set_correlation_id(correlation_id)

    response = await call_next(request)
    response.headers["x-correlation-id"] = correlation_id
    return response

# Health check endpoint
@app.get("/health")
@tracer.capture_method
async def health_check():
    """Health check endpoint for container orchestration"""
    metrics.add_metric(name="HealthCheck", unit=MetricUnit.Count, value=1)

    return {
        "status": "healthy",
        "service": "personal-info",
        "version": "1.0.0"
    }

# Lambda handler using Mangum
handler = Mangum(app, lifespan="off")

@tracer.capture_lambda_handler
@logger.inject_lambda_context
@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler function

    Args:
        event: AWS Lambda event
        context: AWS Lambda context

    Returns:
        HTTP response from FastAPI application
    """
    try:
        # Log the incoming event
        logger.info(
            "Processing request",
            extra={
                "event_type": event.get("httpMethod", "unknown"),
                "path": event.get("path", "unknown"),
                "request_id": context.aws_request_id if context else "local"
            }
        )

        # Add cold start metric
        if hasattr(context, 'get_remaining_time_in_millis'):
            metrics.add_metric(
                name="ColdStart",
                unit=MetricUnit.Count,
                value=1
            )

        # Process the request through Mangum
        response = handler(event, context)

        # Log successful response
        logger.info(
            "Request processed successfully",
            extra={
                "status_code": response.get("statusCode", 200),
                "request_id": context.aws_request_id if context else "local"
            }
        )

        return response

    except Exception as e:
        # Log error with full context
        logger.error(
            "Error processing request",
            exc_info=True,
            extra={
                "error": str(e),
                "event": json.dumps(event),
                "request_id": context.aws_request_id if context else "local"
            }
        )

        # Add error metric
        metrics.add_metric(name="Errors", unit=MetricUnit.Count, value=1)

        # Return error response
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "x-correlation-id": event.get("headers", {}).get("x-correlation-id", "unknown")
            },
            "body": json.dumps({
                "error": "Internal server error",
                "message": "An unexpected error occurred",
                "request_id": context.aws_request_id if context else "local"
            })
        }