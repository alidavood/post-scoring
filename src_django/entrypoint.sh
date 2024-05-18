#!/bin/sh

# Apply database migrations
echo "Running database migrations..."
python manage.py migrate

# Start Gunicorn server
echo "Starting Gunicorn server..."
poetry run gunicorn --bind 0.0.0.0:8000 main_app.wsgi:application
