from django.test import TestCase
from .models import Product

class ProductTests(TestCase):
    def test_product_creation(self):
        product = Product.objects.create(name="Test Product", price=100.00, co2_reduction=0.5)
        self.assertEqual(product.name, "Test Product")