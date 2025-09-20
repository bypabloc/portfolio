# Personal Info Lambda - AWS Lambda Container with Shared Modules
FROM public.ecr.aws/lambda/python:3.12

# Install system dependencies for building packages
RUN dnf update -y && \
    dnf install -y gcc python3-devel curl && \
    dnf clean all

# Set working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Install dependencies from requirements.txt
COPY setup/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared modules as specified in shared.yml
# Copy entire shared directory structure for now (can be optimized later)
COPY ../../shared/ ./shared/

# Copy lambda function source code
COPY src/ ./

# Set environment variables for Lambda
ENV PYTHONPATH="${LAMBDA_TASK_ROOT}:${LAMBDA_TASK_ROOT}/shared:${PYTHONPATH}"
ENV LAMBDA_FUNCTION_NAME="personal-info"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/2015-03-31/functions/function/invocations -X POST \
    -H "Content-Type: application/json" \
    -d '{"httpMethod":"GET","path":"/health"}' || exit 1

# Labels for identification
LABEL function="personal-info"
LABEL description="Personal information management Lambda function"
LABEL shared_modules="database,models,repository,config,utils,exceptions"

# Set the CMD to the Lambda handler
CMD ["lambda_function.lambda_handler"]