from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'co2_reduction']  # แสดงฟิลด์ในตาราง
    list_filter = ['price']  # เพิ่มตัวกรอง
    search_fields = ['name']  # เพิ่มช่องค้นหา