FROM python:3.9-slim

# Install PostgreSQL and required packages
RUN apt-get update && apt-get install -y \
    postgresql \
    postgresql-contrib \
    libpq-dev \
    supervisor \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY backend/ .

# Copy configuration files
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY docker/init-db.sh /docker-entrypoint-initdb.d/
COPY docker/start.sh /start.sh

# Make scripts executable
RUN chmod +x /docker-entrypoint-initdb.d/init-db.sh /start.sh

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV PGDATA=/var/lib/postgresql/data
ENV DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tally_subscribers

# Create directory for PostgreSQL data
RUN mkdir -p /var/lib/postgresql/data \
    && chown -R postgres:postgres /var/lib/postgresql/data

# Expose the port
EXPOSE 5000

# Start services using supervisord
CMD ["/start.sh"]
