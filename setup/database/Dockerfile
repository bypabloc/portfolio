# PostgreSQL 17 with Neon compatibility for Portfolio Serverless System
# Based on Neon local development setup with WebSocket proxy support

FROM postgres:17-alpine

# Install additional tools for Neon compatibility
RUN apk add --no-cache \
    curl \
    jq \
    ca-certificates

# Set environment variables for PostgreSQL
ENV POSTGRES_DB=portfolio_db
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=portfolio_password
ENV PGDATA=/var/lib/postgresql/data/pgdata

# Create custom configuration directory
RUN mkdir -p /docker-entrypoint-initdb.d
RUN mkdir -p /etc/postgresql

# Copy initialization scripts
COPY init-portfolio-db.sql /docker-entrypoint-initdb.d/
COPY postgresql.conf /etc/postgresql/

# Expose PostgreSQL port
EXPOSE 5432

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD pg_isready -U $POSTGRES_USER -d $POSTGRES_DB

# Use custom configuration
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]