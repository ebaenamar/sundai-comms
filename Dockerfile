FROM postgres:14

# Install Python and required packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    supervisor \
    procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY backend/requirements.txt .

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY backend/ .

# Copy configuration files
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Create script to initialize the application after PostgreSQL is ready
RUN echo '#!/bin/bash\n\
echo "Starting Flask application..."\n\
exec gunicorn --bind 0.0.0.0:5000 app:create_app()' > /start-flask.sh \
    && chmod +x /start-flask.sh

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tally_subscribers

# Expose the port
EXPOSE 5000

# Override the entrypoint to start both PostgreSQL and Flask
COPY docker/docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["postgres"]
