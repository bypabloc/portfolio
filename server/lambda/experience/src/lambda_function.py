"""
AWS Lambda handler for Experience service using FastAPI + SQLModel.

This Lambda manages work experience, employers, and job types.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/01/19
"""

from functools import lru_cache
from shared.logger import logger
from mangum import Mangum

# Import FastAPI app using shared models
from main import app

# AWS Lambda Powertools


@lru_cache(maxsize=1)
def create_handler():
    """
    Create cached Mangum handler for FastAPI app.

    Returns:
        Mangum: Configured AWS Lambda handler
    """
    return Mangum(
        app,
        lifespan="auto",
        api_gateway_base_path="/prod"
    )


# Initialize handler at module level (cold start optimization)
handler_instance = create_handler()


def lambda_handler(event, context):
    """
    AWS Lambda entry point for Experience service.

    Args:
        event: API Gateway event
        context: Lambda context

    Returns:
        HTTP response for API Gateway
    """
    # Log request details
    logger.info(
        "Experience Lambda invocation started",
        extra={
            "request_id": context.aws_request_id,
            "function_name": context.function_name,
            "event_path": event.get("path", "unknown"),
            "http_method": event.get("httpMethod", "unknown")
        }
    )

    # Add custom metrics

    try:
        response = handler_instance(event, context)

        # Add success metric

        return response

    except Exception as e:
        logger.error(f"Lambda invocation failed: {str(e)}", exc_info=True)

        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": '{"error": "Internal server error"}'
        }
