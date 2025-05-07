from django.shortcuts import render
from .models import Product

def index(request):
    products = Product.objects.all()
    total_co2 = sum(product.co2_reduction for product in products)
    return render(request, 'store/index.html', {'products': products, 'total_co2': total_co2})