#!/bin/bash
set -e

if [ ! -f "/usr/src/app/manage.py" ]; then
    django-admin startproject myproject .
 fi


cd myproject  # ถ้าคุณใช้โฟลเดอร์ myproject

python manage.py migrate
exec python manage.py runserver 0.0.0.0:8000
