FROM public.ecr.aws/lambda/python:3.12

LABEL maintainer="Pablo Contreras <pablo@bypabloc.dev>"
LABEL project="Portfolio Serverless System"
LABEL service="experience-lambda"
LABEL environment="local"

# Install basic system packages for tools
RUN microdnf install -y tar gzip && microdnf clean all

WORKDIR ${LAMBDA_TASK_ROOT}

# Copy shared utilities first (better Docker layer caching)
COPY shared/ ./shared/

# Copy service-specific requirements and config
COPY lambda/experience/setup/requirements.txt .
COPY lambda/experience/setup/config.yml /var/task/config.yml

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy service source code and ensure files are in Lambda task root
COPY lambda/experience/src/ ./src/
RUN if [ -d "./src" ]; then cp ./src/* . 2>/dev/null || true; fi && rm -rf ./src


# Set Python path to include shared modules
ENV PYTHONPATH="${LAMBDA_TASK_ROOT}:${LAMBDA_TASK_ROOT}/shared:${PYTHONPATH}"

# Environment-specific configurations
ENV LOG_LEVEL=debug
ENV ENVIRONMENT=local
ENV SERVICE_NAME=experience-lambda
ENV SERVICE_VERSION=1.0.0
ENV FASTAPI_DEBUG=true

# Create useful directories for development
RUN mkdir -p /tmp/logs /tmp/cache /tmp/debug

# Expose port for local development (Lambda Runtime Interface Emulator)
EXPOSE 8080

# Health check for container orchestration
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1


# Lambda handler entry point
CMD ["lambda_function.lambda_handler"]