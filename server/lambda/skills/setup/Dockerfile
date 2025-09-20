# Skills Lambda - AWS Lambda Container
FROM public.ecr.aws/lambda/python:3.13

# Install AWS Lambda Runtime Interface Emulator for local development
RUN yum update -y && \
    yum install -y curl && \
    yum clean all

# Set the working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy lambda function
COPY lambda_function.py ${LAMBDA_TASK_ROOT}/

# Set environment variables for Lambda
ENV PYTHONPATH="${LAMBDA_TASK_ROOT}:${PYTHONPATH}"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/2015-03-31/functions/function/invocations -X POST \
    -H "Content-Type: application/json" \
    -d '{"httpMethod":"GET","path":"/health"}' || exit 1

# Set the CMD to the Lambda handler
CMD ["lambda_function.lambda_handler"]