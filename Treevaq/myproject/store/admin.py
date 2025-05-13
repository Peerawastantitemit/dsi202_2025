from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'co2_reduction']

    def co2_reduction(self, obj):
        # ตัวอย่าง: CO2 ลดลงตามราคา
        return round(float(obj.price) * 0.1, 2)
    co2_reduction.short_description = 'CO2 Reduction (kg)'