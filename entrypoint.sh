#!/bin/sh
set -e

echo "Checking database connection at $DATABASE_HOST:$DATABASE_PORT..."
until nc -z "$DATABASE_HOST" "$DATABASE_PORT"; do
  echo "Waiting for database..."
  sleep 2
done
echo "Database is up!"

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Run offline compression first
echo "Running offline compression..."
python manage.py compress --force

# Collect static files after compression
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn nasaftours.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --log-level info \
    --access-logfile '-' \
    --error-logfile '-'


