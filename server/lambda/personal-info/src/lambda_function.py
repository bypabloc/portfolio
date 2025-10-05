"""
AWS Lambda handler for Personal Info service using FastAPI + SQLModel.

This Lambda manages users and user attributes with EAV pattern support.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/01/19
"""

from functools import lru_cache
from mangum import Mangum

# Import FastAPI app using shared models
from main import app

# Custom logger
from shared.logger import logger



@lru_cache(maxsize=1)
def create_handler():
    """
    Create cached Mangum handler for FastAPI app.

    Returns:
        Mangum: Configured AWS Lambda handler
    """
    return Mangum(
        app,
        lifespan="auto"
    )


# Initialize handler at module level (cold start optimization)
handler_instance = create_handler()


def lambda_handler(event, context):
    """
    AWS Lambda entry point for Personal Info service.

    Args:
        event: API Gateway event
        context: Lambda context

    Returns:
        HTTP response for API Gateway
    """
    # Log request details
    logger.info(
        "Personal Info Lambda invocation started",
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
