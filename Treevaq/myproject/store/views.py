from django.shortcuts import render
from .models import Product

def index(request):
    products = Product.objects.all()
    total_co2 = 0  # ตัวอย่างการคำนวณ CO2
    # ถ้ามีตะกร้า จะคำนวณจากสินค้าที่เลือก
    return render(request, 'store/index.html', {'products': products, 'total_co2': total_co2})