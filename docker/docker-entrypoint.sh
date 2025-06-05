#!/bin/bash
set -e

# This script is based on the official postgres docker-entrypoint.sh
# but modified to also start our Flask application

# Create the database if it doesn't exist
if [ "$1" = 'postgres' ]; then
    # Call the original entrypoint script from postgres image
    # which sets up the database
    /usr/local/bin/docker-entrypoint.sh postgres &
    
    # Wait for PostgreSQL to become available
    until pg_isready -h localhost -p 5432 -U postgres; do
        echo "Waiting for PostgreSQL to become available..."
        sleep 2
    done
    
    # Create our application database if it doesn't exist
    psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
        CREATE DATABASE tally_subscribers;
        GRANT ALL PRIVILEGES ON DATABASE tally_subscribers TO postgres;
EOSQL
    
    # Start the Flask application
    echo "Starting Flask application..."
    cd /app
    exec supervisord -c /etc/supervisor/conf.d/supervisord.conf
else
    # If not starting postgres, just run the command
    exec "$@"
fi
