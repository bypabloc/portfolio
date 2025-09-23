#!/usr/bin/env python3
"""
Dynamic Configuration Generator for Portfolio System
Generates Docker configurations and nginx routes from service config.yml files
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class ServiceConfig:
    """Service configuration extracted from config.yml"""
    name: str
    path: str
    description: str
    methods: List[str]
    cors_enabled: bool
    health_endpoint: str


class ConfigGenerator:
    """Generates dynamic configurations for Docker and nginx from service configs"""

    def __init__(self, project_root: str, unified_port: int = 4321):
        self.project_root = Path(project_root)
        self.unified_port = unified_port
        self.services: List[ServiceConfig] = []

    def discover_services(self) -> List[ServiceConfig]:
        """Discover all Lambda services from their config.yml files"""
        services = []
        lambda_dir = self.project_root / "server" / "lambda"

        if not lambda_dir.exists():
            print(f"Lambda directory not found: {lambda_dir}")
            return services

        for service_dir in lambda_dir.iterdir():
            if service_dir.is_dir():
                config_file = service_dir / "setup" / "config.yml"
                if config_file.exists():
                    try:
                        service = self._parse_service_config(config_file)
                        services.append(service)
                        # No mostrar servicios individuales por defecto
                    except Exception as e:
                        print(f"❌ Failed to parse {config_file}: {e}")

        self.services = services
        return services

    def _parse_service_config(self, config_path: Path) -> ServiceConfig:
        """Parse a single service config.yml file"""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        lambda_config = config.get('lambda_function', {})
        api_config = config.get('api_gateway', {})
        health_config = config.get('health_check', {})

        return ServiceConfig(
            name=lambda_config.get('name', config_path.parent.parent.name),
            path=api_config.get('path', f"/{lambda_config.get('name', 'unknown')}"),
            description=lambda_config.get('description', ''),
            methods=api_config.get('methods', ['GET']),
            cors_enabled=api_config.get('cors_enabled', True),
            health_endpoint=health_config.get('endpoint', '/health')
        )

    def generate_nginx_config(self) -> str:
        """Generate nginx configuration with dynamic service routing"""
        nginx_template = f"""# Nginx Configuration for Portfolio API Gateway
# Auto-generated from service config.yml files
# DO NOT EDIT MANUALLY - Use scripts/setup/src/config_generator.py

user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {{
    worker_connections 1024;
    use epoll;
    multi_accept on;
}}

http {{
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging format
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for" '
                    'rt=$request_time uct="$upstream_connect_time" '
                    'uht="$upstream_header_time" urt="$upstream_response_time"';

    access_log /var/log/nginx/access.log main;

    # Basic settings
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1000;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        application/json
        application/javascript
        application/xml
        text/css
        text/javascript
        text/plain
        text/xml;

    # Dynamic upstream definitions
{self._generate_upstream_blocks()}

    # Website upstream (Astro v5)
    upstream website_server {{
        server portfolio-website:4321;
        keepalive 16;
    }}

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=health:10m rate=30r/s;

    # Main server block - Unified entry point for all services
    server {{
        listen 80;
        server_name localhost;

        # Add security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

        # Simplified CORS headers
        add_header Access-Control-Allow-Origin "*" always;
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
        add_header Access-Control-Allow-Headers "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization" always;

        # Health check endpoint
        location /health {{
            limit_req zone=health burst=10 nodelay;
            access_log off;
            return 200 '{{"status":"healthy","service":"unified-gateway","port":"{self.unified_port}","timestamp":"$time_iso8601"}}';
            add_header Content-Type application/json;
        }}


{self._generate_api_location_blocks()}

        # Website - Astro v5 at root path /
        location / {{
            proxy_pass http://website_server;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # Enable WebSocket support for Astro dev server
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";

            # Handle trailing slashes and static assets
            try_files $uri $uri/ @website;
        }}

        # Fallback for website routing
        location @website {{
            proxy_pass http://website_server;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }}
    }}
}}
"""
        return nginx_template

    def _generate_upstream_blocks(self) -> str:
        """Generate upstream blocks for each service"""
        blocks = []
        for service in self.services:
            block = f"""    upstream {service.name.replace('-', '_')}_server {{
        server {service.name}-lambda:8080;
        keepalive 32;
    }}"""
            blocks.append(block)
        return "\n\n".join(blocks)

    def _generate_api_location_blocks(self) -> str:
        """Generate API location blocks for each service"""
        blocks = []
        for service in self.services:
            upstream_name = service.name.replace('-', '_') + '_server'
            # Clean path for internal routing (remove leading slash for rewrite)
            internal_path = service.path.lstrip('/')

            block = f"""        # API Routes - {service.description}
        location /api{service.path} {{
            limit_req zone=api burst=20 nodelay;

            # Lambda Runtime Interface Emulator configuration
            proxy_method POST;
            proxy_pass_request_headers off;
            proxy_set_header Content-Type "application/json";

            # Strip /api prefix and create Lambda event with correct path
            set $lambda_path $uri;
            if ($uri ~ "^/api(.*)") {{
                set $lambda_path $1;
            }}

            # Create complete API Gateway v2 Lambda event
            set $lambda_event '{{"version":"2.0","routeKey":"ANY $lambda_path","rawPath":"$lambda_path","requestContext":{{"http":{{"method":"$request_method","path":"$lambda_path","protocol":"HTTP/1.1","sourceIp":"127.0.0.1"}},"stage":"prod","requestId":"nginx-proxy"}},"headers":{{}},"body":"$request_body","isBase64Encoded":false}}';
            proxy_set_body $lambda_event;

            # Proxy to Lambda Runtime Interface
            proxy_pass http://{upstream_name}/2015-03-31/functions/function/invocations;

            # Basic proxy settings
            proxy_http_version 1.1;
            proxy_set_header Connection "";
            proxy_connect_timeout 30s;
            proxy_send_timeout 30s;
            proxy_read_timeout 30s;
        }}"""
            blocks.append(block)
        return "\n\n".join(blocks)

    def generate_docker_compose_override(self, environment: str = "local") -> str:
        """Generate Docker Compose configuration with dynamic services"""
        compose_config = {
            'version': '3.8',
            'services': {
                'api-gateway': {
                    'environment': [
                        f'UNIFIED_PORT={self.unified_port}',
                        f'NGINX_ENV={environment}'
                    ],
                    'ports': [f'{self.unified_port}:80'],
                    'depends_on': [f'{service.name}-lambda' for service in self.services] + [
                        'portfolio-website'
                    ]
                }
            }
        }

        # Add each service with no external ports
        for service in self.services:
            compose_config['services'][f'{service.name}-lambda'] = {
                'environment': [
                    f'SERVICE_PATH={service.path}',
                    f'SERVICE_NAME={service.name}',
                    f'UNIFIED_PORT={self.unified_port}',
                    f'DATABASE_URL=postgresql://postgres:portfolio_password@portfolio-db:5432/portfolio_{environment}'
                ],
                'networks': ['portfolio-network']
                # No external ports - only accessible through API Gateway
            }

        return yaml.dump(compose_config, default_flow_style=False, sort_keys=False)

    def generate_service_urls_json(self) -> str:
        """Generate JSON with all service URLs for reference"""
        urls = {
            'unified_port': self.unified_port,
            'base_url': f'http://localhost:{self.unified_port}',
            'website': {
                'root': f'http://localhost:{self.unified_port}/',
                'pages': [
                    f'http://localhost:{self.unified_port}/',
                    f'http://localhost:{self.unified_port}/about',
                    f'http://localhost:{self.unified_port}/projects',
                    f'http://localhost:{self.unified_port}/skills',
                    f'http://localhost:{self.unified_port}/experience',
                    f'http://localhost:{self.unified_port}/contact'
                ]
            },
            'database_admin': f'http://localhost:{self.unified_port}/db/',
            'api_gateway': {
                'health': f'http://localhost:{self.unified_port}/health',
                'services': {}
            }
        }

        for service in self.services:
            service_urls = {
                'base': f'http://localhost:{self.unified_port}/api{service.path}',
                'health': f'http://localhost:{self.unified_port}/api{service.path}/health',
                'docs': f'http://localhost:{self.unified_port}/api{service.path}/docs',
                'redoc': f'http://localhost:{self.unified_port}/api{service.path}/redoc',
                'methods': service.methods
            }
            urls['api_gateway']['services'][service.name] = service_urls

        return json.dumps(urls, indent=2)

    def save_configurations(self, output_dir: str = None):
        """Save all generated configurations to files"""
        if output_dir is None:
            output_dir = self.project_root / "setup" / "generated"

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Generate nginx config
        nginx_config = self.generate_nginx_config()
        nginx_file = output_path / "nginx.conf"
        with open(nginx_file, 'w') as f:
            f.write(nginx_config)
        # Ocultar paths específicos, solo mostrar resumen

        # Generate docker compose override
        compose_override = self.generate_docker_compose_override()
        compose_file = output_path / "docker-compose.generated.yml"
        with open(compose_file, 'w') as f:
            f.write(compose_override)

        # Generate service URLs
        urls_json = self.generate_service_urls_json()
        urls_file = output_path / "service-urls.json"
        with open(urls_file, 'w') as f:
            f.write(urls_json)

        return {
            'nginx_config': nginx_file,
            'docker_compose': compose_file,
            'service_urls': urls_file
        }


def main():
    """Main function to generate configurations"""
    import argparse

    parser = argparse.ArgumentParser(description="Generate dynamic configurations for Portfolio system")
    parser.add_argument('--project-root', default='.', help='Project root directory')
    parser.add_argument('--port', type=int, default=4321, help='Unified port for all services')
    parser.add_argument('--output-dir', help='Output directory for generated files')
    parser.add_argument('--environment', default='local', help='Environment (local, dev, test, prod)')

    args = parser.parse_args()

    # Initialize generator
    generator = ConfigGenerator(args.project_root, args.port)

    # Discover services
    services = generator.discover_services()
    print(f"\n🔍 Discovered {len(services)} services:")
    for service in services:
        print(f"   • {service.name:<15} -> {service.path}")

    # Generate configurations
    print(f"\n🏗️ Generating configurations for port {args.port}...")
    files = generator.save_configurations(args.output_dir)

    print(f"\n✅ All configurations generated successfully!")
    print(f"🚀 Unified Port: {args.port}")
    print(f"📁 Output Directory: {Path(args.output_dir or generator.project_root / 'setup' / 'generated').absolute()}")


if __name__ == "__main__":
    main()