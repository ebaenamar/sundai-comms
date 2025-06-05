#!/bin/bash
set -e

# Activate Python virtual environment
source /opt/venv/bin/activate

# Start supervisord which will manage both PostgreSQL and Flask
exec supervisord -c /etc/supervisor/conf.d/supervisord.conf
