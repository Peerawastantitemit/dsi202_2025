# my_django_project/treevaq_app/admin.py
from django.contrib import admin
from .models import Product # นำเข้า Model Product ของเรา

admin.site.register(Product) # ลงทะเบียน Product กับ Django Admin