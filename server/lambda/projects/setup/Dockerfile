# Personal Info Microservice - FastAPI + AWS Lambda simulation
# Portfolio Serverless System

FROM public.ecr.aws/lambda/python:3.13

# Install system dependencies
RUN yum update -y && \
    yum install -y gcc curl && \
    yum clean all

# Set work directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY lambda_function.py .

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser ${LAMBDA_TASK_ROOT}

# Environment variables
ENV PYTHONPATH="${LAMBDA_TASK_ROOT}/src:${PYTHONPATH}"
ENV SERVICE_NAME="personal-info"
ENV LAMBDA_RUNTIME_DIR="/var/runtime"

# For local development with RIE (Runtime Interface Emulator)
RUN curl -Lo /usr/bin/aws-lambda-rie https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie && \
    chmod +x /usr/bin/aws-lambda-rie

# Create entrypoint script
RUN echo '#!/bin/bash' > /entrypoint.sh && \
    echo 'if [ -z "${AWS_LAMBDA_RUNTIME_API}" ]; then' >> /entrypoint.sh && \
    echo '  exec /usr/bin/aws-lambda-rie python -m awslambdaric $1' >> /entrypoint.sh && \
    echo 'else' >> /entrypoint.sh && \
    echo '  exec python -m awslambdaric $1' >> /entrypoint.sh && \
    echo 'fi' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Switch to non-root user
USER appuser

# Expose port for local development
EXPOSE 8080

# Set entrypoint for Lambda function
ENTRYPOINT ["/entrypoint.sh"]
CMD ["lambda_function.lambda_handler"]