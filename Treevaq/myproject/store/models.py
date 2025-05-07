from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    co2_reduction = models.FloatField(default=0.0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # เพิ่มฟิลด์รูปภาพ

    def __str__(self):
        return self.name