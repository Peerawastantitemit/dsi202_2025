#!/bin/bash
set -e

if [ ! -f "/usr/src/app/myproject/manage.py" ]; then
    cd /usr/src/app
    django-admin startproject myproject /usr/src/app/myproject
fi

cd /usr/src/app/myproject

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec python manage.py runserver 0.0.0.0:8000