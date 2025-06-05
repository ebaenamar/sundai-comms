#!/bin/bash
set -e

# Run PostgreSQL initialization script
/docker-entrypoint-initdb.d/init-db.sh

# Start all services using supervisord
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
