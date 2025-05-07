#!/bin/bash
set -e

# ตรวจสอบและสร้างโปรเจกต์ Django ถ้ายังไม่มี
if [ ! -f "/usr/src/app/myproject/manage.py" ]; then
    cd /usr/src/app
    django-admin startproject myproject /usr/src/app/myproject
fi

# เปลี่ยนไปที่โฟลเดอร์ myproject
cd /usr/src/app/myproject

# Apply migrations
python manage.py migrate
exec gunicorn --bind 0.0.0.0:8000 myproject.wsgi:application