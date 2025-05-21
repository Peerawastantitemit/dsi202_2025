import os
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Cart
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.contrib.auth import login

def index(request):
    query = request.GET.get('q', '').strip()
    if query:
        products = Product.objects.filter(name__icontains=query) | Product.objects.filter(description__icontains=query)
    else:
        products = Product.objects.all()
    
    cart_items = Cart.objects.filter(user=request.user) if request.user.is_authenticated else []
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
    
    return render(request, 'store/index.html', {'products': products, 'cart_items': cart_items, 'query': query})

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
    return redirect('store:cart')  # Note the namespace 'store:cart'

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
    total = sum(
        float(item.product.price) * int(item.quantity) 
        for item in cart_items
    )
    for item in cart_items:
        item.total_price = float(item.product.price) * int(item.quantity)
    return render(request, 'store/cart.html', {
        'cart_items': cart_items, 
        'total': total
    })

@login_required
def confirm_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
    Cart.objects.filter(user=request.user).delete()
    return render(request, 'store/order_confirmation.html', {'cart_items': cart_items, 'total': total})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('store:index')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def about(request):
    return render(request, 'store/about.html')

@login_required
def get_cart_items(request):
    cart_items = Cart.objects.filter(user=request.user)
    data = {
        'cart_items': []
    }
    for item in cart_items:
        # Ensure numeric values by converting to float
        price = float(item.product.price) if item.product.price else 0.0
        quantity = int(item.quantity) if item.quantity else 0
        total_price = price * quantity
        
        data['cart_items'].append({
            'id': item.id,
            'product': {
                'id': item.product.id,
                'name': item.product.name,
                'price': price,  # Ensure this is numeric
                'image': item.product.image.url if item.product.image else '',
            },
            'quantity': quantity,  # Ensure this is numeric
            'total_price': total_price,
        })
    return JsonResponse(data)

@login_required
def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'store/profile.html')

def product_list(request):
    products = Product.objects.all()  # Assuming you have a Product model
    return render(request, 'store/products.html', {'products': products})