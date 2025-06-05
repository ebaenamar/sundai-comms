#!/bin/bash
set -e

# Function to initialize PostgreSQL
init_postgres() {
    echo "Initializing PostgreSQL database..."
    
    # Initialize PostgreSQL if data directory is empty
    if [ -z "$(ls -A $PGDATA)" ]; then
        echo "Data directory is empty, initializing PostgreSQL..."
        su - postgres -c "initdb -D $PGDATA"
        
        # Configure PostgreSQL to listen on all interfaces
        echo "host all all 0.0.0.0/0 md5" >> $PGDATA/pg_hba.conf
        echo "listen_addresses='*'" >> $PGDATA/postgresql.conf
    else
        echo "PostgreSQL data directory already exists, skipping initialization"
    fi
    
    # Start PostgreSQL temporarily to create database and user
    su - postgres -c "pg_ctl -D $PGDATA -o '-c listen_addresses=localhost' -w start"
    
    # Create database and user if they don't exist
    if ! su - postgres -c "psql -tAc \"SELECT 1 FROM pg_database WHERE datname='tally_subscribers'\"" | grep -q 1; then
        echo "Creating database: tally_subscribers"
        su - postgres -c "createdb tally_subscribers"
    fi
    
    # Set password for postgres user
    su - postgres -c "psql -c \"ALTER USER postgres WITH PASSWORD 'postgres';\""
    
    # Stop PostgreSQL
    su - postgres -c "pg_ctl -D $PGDATA -m fast -w stop"
    
    echo "PostgreSQL initialization completed"
}

# Run initialization
init_postgres
