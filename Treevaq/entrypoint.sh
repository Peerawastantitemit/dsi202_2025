#!/bin/bash
set -e

# Skip project creation if manage.py exists (comment out if you want to create a new project)
# if [ ! -f "/usr/src/app/myproject/manage.py" ]; then
#     cd /usr/src/app
#     django-admin startproject myproject .
#     sed -i "/INSTALLED_APPS = \[/a \    'social_django'," /usr/src/app/myproject/settings.py
#     sed -i "/from django.urls import path/a from django.urls import include" /usr/src/app/myproject/urls.py
#     sed -i "/urlpatterns = \[/a \    path('auth/', include('social_django.urls', namespace='social'))," /usr/src/app/myproject/urls.py
# fi

cd /usr/src/app/myproject

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec daphne -b 0.0.0.0 -p 8000 myproject.asgi:application