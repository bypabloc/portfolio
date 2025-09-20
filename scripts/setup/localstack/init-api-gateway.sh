#!/bin/bash

# LocalStack API Gateway Initialization Script
# Portfolio Serverless System - Auto-configuration for Lambda API Gateway Integration
# This script automatically detects lambda configurations and sets up API Gateway

set -e

echo "🚀 Inicializando LocalStack API Gateway para Portfolio System..."

# Configuration
AWS_REGION="us-east-1"
API_NAME="portfolio-api"
STAGE_NAME="prod"
LAMBDA_DIR="/opt/code/localstack/server/lambda"

# AWS CLI configuration for LocalStack
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=$AWS_REGION

# Function to wait for LocalStack to be fully ready
wait_for_localstack() {
    echo "⏳ Esperando que LocalStack esté completamente listo..."

    max_attempts=30
    attempt=0

    while [ $attempt -lt $max_attempts ]; do
        if awslocal sts get-caller-identity &>/dev/null; then
            echo "✅ LocalStack está listo!"
            return 0
        fi

        echo "🔄 Intento $((attempt + 1))/$max_attempts - LocalStack aún no está listo..."
        sleep 5
        attempt=$((attempt + 1))
    done

    echo "❌ Error: LocalStack no respondió después de $max_attempts intentos"
    return 1
}

# Function to create IAM role for Lambda
create_lambda_role() {
    echo "🔐 Creando rol IAM para Lambda..."

    # Create trust policy
    cat > /tmp/trust-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

    # Create role (ignore if already exists)
    awslocal iam create-role \
        --role-name lambda-execution-role \
        --assume-role-policy-document file:///tmp/trust-policy.json \
        --output table 2>/dev/null || echo "⚠️  Rol lambda-execution-role ya existe"

    # Attach basic execution policy (ignore if already attached)
    awslocal iam attach-role-policy \
        --role-name lambda-execution-role \
        --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole 2>/dev/null || echo "⚠️  Policy ya está attachada"
}

# Function to discover lambda configurations
discover_lambda_configs() {
    echo "🔍 Buscando configuraciones de lambda..."

    # This will be populated by the Python script that reads lambda configs
    echo "Los lambdas serán descubiertos por el script Python"
}

# Function to create API Gateway
create_api_gateway() {
    echo "🌐 Creando API Gateway: $API_NAME..."

    # Create REST API
    API_ID=$(awslocal apigateway create-rest-api \
        --name $API_NAME \
        --description "Portfolio Serverless System API Gateway" \
        --query 'id' \
        --output text)

    echo "✅ API Gateway creado con ID: $API_ID"
    echo $API_ID > /tmp/api-gateway-id.txt

    # Get root resource
    ROOT_RESOURCE_ID=$(awslocal apigateway get-resources \
        --rest-api-id $API_ID \
        --query 'items[0].id' \
        --output text)

    echo "✅ Root resource ID: $ROOT_RESOURCE_ID"
    echo $ROOT_RESOURCE_ID > /tmp/root-resource-id.txt

    return 0
}

# Function to deploy API
deploy_api() {
    local api_id=$1

    echo "🚀 Desplegando API Gateway..."

    awslocal apigateway create-deployment \
        --rest-api-id $api_id \
        --stage-name $STAGE_NAME \
        --description "Portfolio API deployment" \
        --output table

    echo "✅ API desplegada en stage: $STAGE_NAME"
    echo "🌐 URL de la API: http://localhost:4566/restapis/$api_id/$STAGE_NAME/_user_request_"
}

# Function to create CORS options for a resource
create_cors_options() {
    local api_id=$1
    local resource_id=$2

    echo "🔗 Configurando CORS para recurso $resource_id..."

    # Add OPTIONS method
    awslocal apigateway put-method \
        --rest-api-id $api_id \
        --resource-id $resource_id \
        --http-method OPTIONS \
        --authorization-type NONE \
        --output table || echo "OPTIONS method ya existe"

    # Add MOCK integration for OPTIONS
    awslocal apigateway put-integration \
        --rest-api-id $api_id \
        --resource-id $resource_id \
        --http-method OPTIONS \
        --type MOCK \
        --request-templates '{"application/json":"{\"statusCode\": 200}"}' \
        --output table || echo "MOCK integration ya existe"

    # Add method response for OPTIONS
    awslocal apigateway put-method-response \
        --rest-api-id $api_id \
        --resource-id $resource_id \
        --http-method OPTIONS \
        --status-code 200 \
        --response-parameters \
            method.response.header.Access-Control-Allow-Headers=false,method.response.header.Access-Control-Allow-Methods=false,method.response.header.Access-Control-Allow-Origin=false \
        --output table || echo "Method response ya existe"

    # Add integration response for OPTIONS
    awslocal apigateway put-integration-response \
        --rest-api-id $api_id \
        --resource-id $resource_id \
        --http-method OPTIONS \
        --status-code 200 \
        --response-parameters \
            method.response.header.Access-Control-Allow-Headers="'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",method.response.header.Access-Control-Allow-Methods="'GET,POST,PUT,DELETE,OPTIONS'",method.response.header.Access-Control-Allow-Origin="'*'" \
        --output table || echo "Integration response ya existe"
}

# Main execution
main() {
    echo "🎯 Iniciando configuración de LocalStack API Gateway..."

    # Wait for LocalStack
    if ! wait_for_localstack; then
        echo "❌ Error: No se pudo conectar a LocalStack"
        exit 1
    fi

    # Create IAM role
    create_lambda_role

    # Create API Gateway
    create_api_gateway

    # The lambda configurations will be processed by the Python script
    echo "⏭️  Las configuraciones específicas de lambda serán procesadas por el script Python de setup"
    echo "✅ Inicialización básica de LocalStack completada"

    # Save configuration for Python script
    cat > /tmp/localstack-config.json << EOF
{
    "api_id": "$(cat /tmp/api-gateway-id.txt)",
    "root_resource_id": "$(cat /tmp/root-resource-id.txt)",
    "stage_name": "$STAGE_NAME",
    "aws_region": "$AWS_REGION"
}
EOF

    echo "📝 Configuración guardada en /tmp/localstack-config.json"
}

# Execute main function
main "$@"