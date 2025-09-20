# Neon WebSocket Proxy for Local Development
# Enables Neon serverless driver compatibility with local PostgreSQL
# Based on community Dockerfile by TimoWilhelm

FROM node:22-alpine

# Install dependencies
RUN apk add --no-cache git

# Clone and setup Neon WebSocket proxy
WORKDIR /app
RUN git clone https://github.com/TimoWilhelm/local-neon-http-proxy.git .
RUN npm install

# Create configuration
COPY neon-proxy-config.json /app/config.json

# Expose proxy port (WebSocket and HTTP)
EXPOSE 5433

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5433/health || exit 1

# Start the proxy
CMD ["npm", "start"]