"""
AWS Lambda handler for Projects service using FastAPI + SQLModel.

This Lambda manages portfolio projects.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/01/19
"""

from functools import lru_cache
from shared.logger import logger
from mangum import Mangum

from main import app



@lru_cache(maxsize=1)
def create_handler():
    """Create cached Mangum handler for FastAPI app."""
    return Mangum(app, lifespan="auto", api_gateway_base_path="/prod")


handler_instance = create_handler()


def lambda_handler(event, context):
    """AWS Lambda entry point for Projects service."""
    logger.info(
        "Projects Lambda invocation started",
        extra={
            "request_id": context.aws_request_id,
            "function_name": context.function_name,
            "event_path": event.get("path", "unknown"),
            "http_method": event.get("httpMethod", "unknown")
        }
    )


    try:
        response = handler_instance(event, context)

        logger.info("Request processed successfully", extra={
            "status_code": response.get("statusCode", "unknown")
        })

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
