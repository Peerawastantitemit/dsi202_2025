from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Cart
from django.contrib import messages

def index(request):
    products = Product.objects.all()
    cart_items = Cart.objects.filter(user=request.user) if request.user.is_authenticated else []
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
    return render(request, 'store/index.html', {'products': products, 'cart_items': cart_items})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"เพิ่ม {product.name} ลงตะกร้าแล้ว!")
    return redirect('cart')

@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(Cart, pk=pk, user=request.user)
    cart_item.delete()
    messages.success(request, "ลบสินค้าออกจากตะกร้าแล้ว!")
    return redirect('cart')

@login_required
def update_cart_quantity(request, pk, action):
    cart_item = get_object_or_404(Cart, pk=pk, user=request.user)
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()
    return redirect('cart')

@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def confirm_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
    # ลบสินค้าจากตะกร้าหลังยืนยัน (ชั่วคราว)
    Cart.objects.filter(user=request.user).delete()
    return render(request, 'store/order_confirmation.html', {'cart_items': cart_items, 'total': total})