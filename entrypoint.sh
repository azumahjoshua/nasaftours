#!/bin/sh

# Wait for DB
nc -z $DATABASE_HOST $DATABASE_PORT
while [ $? -ne 0 ]; do
  echo "Waiting for database at $DATABASE_HOST:$DATABASE_PORT..."
  sleep 1
  nc -z $DATABASE_HOST $DATABASE_PORT
done

# Run migrations and start app
python manage.py migrate
python manage.py collectstatic --noinput
exec gunicorn nasaftours.wsgi:application --bind 0.0.0.0:8000

# #!/bin/bash
# echo "Waiting for postgres..."

# while ! nc -z db 5432; do
#   sleep 1
# done

# echo "PostgreSQL started"

# python manage.py migrate
# python manage.py collectstatic --noinput
# exec python manage.py runserver 0.0.0.0:8000
