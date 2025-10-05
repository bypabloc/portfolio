"""
Users Lambda Function - Entry Point

Consumes shared code from server/shared/ for models, database, etc.

:Authors:
    - Pablo Contreras

:Created:
    - 2025-01-19
"""

from mangum import Mangum
from shared.logger import logger
from functools import lru_cache

# Import FastAPI app
from main import app


# ============================================================================
# Mangum Handler (Cached for Cold Start Optimization)
# ============================================================================

@lru_cache(maxsize=1)
def create_handler():
    """
    Create cached Mangum handler.

    Cached to avoid recreating handler on every invocation (warm starts).
    """
    return Mangum(
        app,
        lifespan="auto",  # Let Mangum handle lifespan
        api_gateway_base_path="/",
    )


# Initialize handler at module level (cold start optimization)
handler_instance = create_handler()


# ============================================================================
# Lambda Handler Entry Point
# ============================================================================

def lambda_handler(event, context):
    """
    AWS Lambda handler for Users service.

    Args:
        event: API Gateway event
        context: Lambda context

    Returns:
        HTTP response for API Gateway
    """
    # Log invocation
    logger.info(
        "Users Lambda invocation started",
        extra={
            "request_id": context.aws_request_id,
            "function_name": context.function_name,
            "event_path": event.get("path", "unknown"),
            "http_method": event.get("httpMethod", "unknown")
        }
    )

    try:
        # Invoke Mangum handler
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
                "Access-Control-Allow-Origin": "*",
            },
            "body": '{"error": "Internal server error"}',
        }
