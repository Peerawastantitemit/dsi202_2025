# store/models.py
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    co2_reduction = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def calculate_co2_reduction(self):
        return round(float(self.price) * 0.1, 2)

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username if self.user else 'Anonymous'}"
    
        # === Environmental fields ===
    sustainability_score = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="คะแนนด้านความยั่งยืน 1-10"
    )
    materials_used = models.TextField(
        blank=True,
        help_text="เช่น ฝ้ายออร์แกนิก, พลาสติกรีไซเคิล"
    )
    certifications = models.CharField(
        max_length=255, blank=True,
        help_text="เช่น Fair Trade, GOTS, FSC Certified"
    )
    carbon_footprint_kg_co2e = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True,
        help_text="ปริมาณการปล่อย CO2 เทียบเท่า (kg)"
    )
    water_usage_liters = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        help_text="ปริมาณการใช้น้ำ (ลิตร) โดยประมาณ"
    )
    recyclability_info = models.TextField(
        blank=True,
        help_text="ข้อมูลการรีไซเคิลสินค้าหรือบรรจุภัณฑ์"
    )
    supplier_eco_policy_link = models.URLField(
        blank=True,
        help_text="ลิงก์ไปยังนโยบายสิ่งแวดล้อมของซัพพลายเออร์"
    )
    country_of_origin = models.CharField(max_length=100, blank=True)

class CartItem(models.Model):
    # ตัวอย่างฟิลด์
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    # เพิ่มฟิลด์อื่น ๆ ตามที่ต้องการ

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"