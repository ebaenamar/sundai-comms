FROM postgres:14

# Install Python and required packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-full \
    supervisor \
    procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create and activate virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements first for better caching
COPY backend/requirements.txt .

# Install dependencies in the virtual environment
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY backend/ .

# Copy configuration files
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Create script to initialize the application after PostgreSQL is ready
RUN echo '#!/bin/bash\n\
echo "Starting Flask application..."\n\
source /opt/venv/bin/activate\n\
exec gunicorn --bind 0.0.0.0:5000 app:create_app()' > /start-flask.sh \
    && chmod +x /start-flask.sh

# Create database initialization script
RUN mkdir -p /docker-entrypoint-initdb.d
RUN echo '#!/bin/bash\n\
echo "Creating tally_subscribers database..."\n\
psql -U postgres -c "CREATE DATABASE tally_subscribers;"\n\
echo "Database created successfully."' > /docker-entrypoint-initdb.d/create-db.sh \
    && chmod +x /docker-entrypoint-initdb.d/create-db.sh

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tally_subscribers
ENV POSTGRES_PASSWORD=postgres

# Expose the port
EXPOSE 5000

# Copy custom entrypoint
COPY docker/docker-entrypoint.sh /usr/local/bin/custom-entrypoint.sh
RUN chmod +x /usr/local/bin/custom-entrypoint.sh

# Use custom entrypoint
ENTRYPOINT ["/usr/local/bin/custom-entrypoint.sh"]
