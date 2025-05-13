from django.db import models
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    co2_reduction = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # เพิ่มฟิลด์
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def co2_reduction(self):
        # ตัวอย่าง: CO2 ลดลงตามราคา (สมมติ 0.1 kg CO2 ต่อ 1 บาท)
        return round(float(self.price) * 0.1, 2)