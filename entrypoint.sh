#!/bin/bash
set -e

# ตรวจสอบและสร้างโปรเจกต์ Django ถ้ายังไม่มี
if [ ! -f "/usr/src/app/manage.py" ]; then
    django-admin startproject myproject .
fi

# เปลี่ยนไปที่โฟลเดอร์ myproject (ถ้าจำเป็น)
cd myproject

# Apply migrations
python manage.py migrate

# Run the server
exec python manage.py runserver 0.0.0.0:8000