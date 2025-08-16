#!/bin/sh
set -e

# Wait for DB to be ready
echo "Checking database connection at $DATABASE_HOST:$DATABASE_PORT..."
until nc -z "$DATABASE_HOST" "$DATABASE_PORT"; do
  echo "Waiting for database..."
  sleep 2
done
echo "Database is up!"

# Ensure directories exist and are writable
# mkdir -p /app/staticfiles /app/logs
chmod -R 755 /app/staticfiles /app/logs

# Run Django migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn nasaftours.wsgi:application --bind 0.0.0.0:8000



#!/bin/sh

# # Wait for DB
# nc -z $DATABASE_HOST $DATABASE_PORT
# while [ $? -ne 0 ]; do
#   echo "Waiting for database at $DATABASE_HOST:$DATABASE_PORT..."
#   sleep 1
#   nc -z $DATABASE_HOST $DATABASE_PORT
# done

# set -e

# # Ensure logs directory exists and is writable
# # mkdir -p /app/logs
# # chown -R appuser:appuser /app/logs


# # Run migrations and start app
# python manage.py migrate
# python manage.py collectstatic --noinput
# exec gunicorn nasaftours.wsgi:application --bind 0.0.0.0:8000

# #!/bin/bash
# echo "Waiting for postgres..."

# while ! nc -z db 5432; do
#   sleep 1
# done

# echo "PostgreSQL started"

# python manage.py migrate
# python manage.py collectstatic --noinput
# exec python manage.py runserver 0.0.0.0:8000
