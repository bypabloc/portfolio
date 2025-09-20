# Frontend Service - Astro v5 with TypeScript
# Portfolio Serverless System

FROM node:22-alpine

# Install system dependencies
RUN apk add --no-cache \
    curl \
    git \
    python3 \
    make \
    g++

# Set work directory
WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S astro -u 1001

# Copy package files
COPY package*.json ./
COPY pnpm-lock.yaml* ./

# Install pnpm globally
RUN npm install -g pnpm@latest

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy application code
COPY . .

# Change ownership to nodejs user
RUN chown -R astro:nodejs /app

# Switch to non-root user
USER astro

# Environment variables
ENV NODE_ENV=development
ENV ASTRO_PORT=4321
ENV HOST=0.0.0.0

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:4321 || exit 1

# Expose port
EXPOSE 4321

# Start Astro development server
CMD ["pnpm", "dev", "--host", "0.0.0.0", "--port", "4321"]