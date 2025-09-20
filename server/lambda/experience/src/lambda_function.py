"""
Experience Lambda Function - Portfolio Serverless System
Handles professional experience management and retrieval for the portfolio API
"""

import json
import logging
from typing import Dict, Any

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for experience service.

    Args:
        event: Lambda event data
        context: Lambda context object

    Returns:
        API Gateway compatible response
    """
    try:
        logger.info(f"Experience Lambda invoked with event: {json.dumps(event)}")

        # Extract HTTP method and path
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/experience')

        if http_method == 'GET':
            return get_experience(event)
        elif http_method == 'POST':
            return create_experience(event)
        elif http_method == 'PUT':
            return update_experience(event)
        elif http_method == 'DELETE':
            return delete_experience(event)
        else:
            return {
                'statusCode': 405,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Method not allowed',
                    'method': http_method
                })
            }

    except Exception as e:
        logger.error(f"Error in experience lambda: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }

def get_experience(event: Dict[str, Any]) -> Dict[str, Any]:
    """Get experience list or specific experience."""
    # TODO: Implement experience retrieval
    experience = [
        {
            'id': '1',
            'company': 'Destacame',
            'position': 'Senior Full-Stack Developer',
            'location': 'Santiago, Chile',
            'start_date': '2021-03-01',
            'end_date': None,
            'is_current': True,
            'description': 'Lead development of fintech applications using modern serverless architectures.',
            'achievements': [
                'Reduced application load time by 60% through serverless optimization',
                'Implemented microservices architecture serving 100k+ daily transactions'
            ],
            'technologies': ['Vue.js', 'Python', 'AWS Lambda', 'PostgreSQL']
        }
    ]

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'experience': experience,
            'total': len(experience)
        })
    }

def create_experience(event: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new experience."""
    # TODO: Implement experience creation
    return {
        'statusCode': 201,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'message': 'Experience created successfully',
            'experience': {'id': 'new-id'}
        })
    }

def update_experience(event: Dict[str, Any]) -> Dict[str, Any]:
    """Update an existing experience."""
    # TODO: Implement experience update
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'message': 'Experience updated successfully'
        })
    }

def delete_experience(event: Dict[str, Any]) -> Dict[str, Any]:
    """Delete an experience."""
    # TODO: Implement experience deletion
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'message': 'Experience deleted successfully'
        })
    }