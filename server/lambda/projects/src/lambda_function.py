"""
Projects Lambda Function - Portfolio Serverless System
Handles project portfolio management and retrieval for the portfolio API
"""

import json
import logging
from typing import Dict, Any

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for projects service.

    Args:
        event: Lambda event data
        context: Lambda context object

    Returns:
        API Gateway compatible response
    """
    try:
        logger.info(f"Projects Lambda invoked with event: {json.dumps(event)}")

        # Extract HTTP method and path
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/projects')

        if http_method == 'GET':
            return get_projects(event)
        elif http_method == 'POST':
            return create_project(event)
        elif http_method == 'PUT':
            return update_project(event)
        elif http_method == 'DELETE':
            return delete_project(event)
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
        logger.error(f"Error in projects lambda: {str(e)}", exc_info=True)
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

def get_projects(event: Dict[str, Any]) -> Dict[str, Any]:
    """Get projects list or specific project."""
    # TODO: Implement projects retrieval
    projects = [
        {
            'id': '1',
            'name': 'portfolio-serverless',
            'title': 'Serverless Portfolio System',
            'description': 'Modern serverless portfolio built with Astro v5, AWS Lambda, FastAPI, and Neon PostgreSQL.',
            'status': 'in_progress',
            'technologies': ['Astro', 'TypeScript', 'Python', 'FastAPI', 'AWS Lambda', 'PostgreSQL'],
            'category': 'fullstack',
            'featured': True,
            'github_url': 'https://github.com/bypabloc/portfolio-serverless',
            'demo_url': 'https://bypabloc.dev'
        },
        {
            'id': '2',
            'name': 'fintech-dashboard',
            'title': 'FinTech Analytics Dashboard',
            'description': 'Real-time financial data visualization dashboard with advanced analytics.',
            'status': 'completed',
            'technologies': ['Vue.js', 'Python', 'FastAPI', 'PostgreSQL', 'Chart.js'],
            'category': 'frontend',
            'featured': True
        }
    ]

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'projects': projects,
            'total': len(projects)
        })
    }

def create_project(event: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new project."""
    # TODO: Implement project creation
    return {
        'statusCode': 201,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'message': 'Project created successfully',
            'project': {'id': 'new-id'}
        })
    }

def update_project(event: Dict[str, Any]) -> Dict[str, Any]:
    """Update an existing project."""
    # TODO: Implement project update
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'message': 'Project updated successfully'
        })
    }

def delete_project(event: Dict[str, Any]) -> Dict[str, Any]:
    """Delete a project."""
    # TODO: Implement project deletion
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'message': 'Project deleted successfully'
        })
    }