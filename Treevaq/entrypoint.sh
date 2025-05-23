#!/bin/bash
set -e

# Navigate to the directory containing manage.py (if needed)
cd /app/myproject

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000
if [ "$USE_CHANNELS" = "true" ]; then
    daphne -b 0.0.0.0 -p 8000 myproject.asgi:application
else
    gunicorn --bind 0.0.0.0:8000 myproject.wsgi:application
fi