#!/bin/bash
set -e

if [ ! -f "/usr/src/app/myproject/manage.py" ]; then
    cd /usr/src/app
    django-admin startproject myproject /usr/src/app/myproject
    sed -i "/INSTALLED_APPS = \[/a \    'social_django'," /usr/src/app/myproject/myproject/settings.py
    sed -i "/from django.urls import path/a from django.urls import include" /usr/src/app/myproject/myproject/urls.py
    sed -i "/urlpatterns = \[/a \    path('auth/', include('social_django.urls', namespace='social'))," /usr/src/app/myproject/myproject/urls.py
fi

cd /usr/src/app/myproject

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec python manage.py runserver 0.0.0.0:8000