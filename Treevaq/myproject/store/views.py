# store/views.py
import os
import qrcode
import io
import logging
import base64
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from decimal import Decimal
from pypromptpay import qr_code
from .models import Product, Cart, CartItem

# Set up logging
logger = logging.getLogger(__name__)

def index(request):
    query = request.GET.get('q', '').strip()
    if query:
        products = Product.objects.filter(name__icontains=query) | Product.objects.filter(description__icontains=query)
    else:
        products = Product.objects.all()
    
    cart_items = CartItem.objects.filter(cart__user=request.user).select_related('product') if request.user.is_authenticated else []
    for item in cart_items:
        item.total_price = Decimal(str(item.product.price)) * Decimal(str(item.quantity))
    
    return render(request, 'store/index.html', {
        'products': products,
        'cart_items': cart_items,
        'query': query
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, pk):
    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('store:product_detail', pk=pk)
    
    product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"เพิ่ม {product.name} ลงตะกร้าแล้ว!")
    return JsonResponse({'status': 'success', 'message': f'เพิ่ม {product.name} ลงตะกร้าแล้ว!'}) if request.is_ajax() else redirect('store:cart')

@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "ลบสินค้าออกจากตะกร้าแล้ว!")
    return redirect('store:cart')

@login_required
def update_cart_quantity(request, pk, action):
    cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()
    messages.success(request, "อัปเดตจำนวนสินค้าเรียบร้อยแล้ว!")
    return redirect('store:cart')

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user).select_related('product')
    total = sum(
        Decimal(str(item.product.price)) * Decimal(str(item.quantity))
        for item in cart_items
    )
    for item in cart_items:
        item.total_price = Decimal(str(item.product.price)) * Decimal(str(item.quantity))
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def confirm_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart_items = CartItem.objects.filter(cart__user=request.user).select_related('product')
    if not cart_items:
        messages.warning(request, "ตะกร้าของคุณว่างเปล่า!")
        return redirect('store:cart')

    total = sum(
        Decimal(str(item.product.price)) * Decimal(str(item.quantity))
        for item in cart_items
    )
    for item in cart_items:
        item.total_price = Decimal(str(item.product.price)) * Decimal(str(item.quantity))

    # Generate PromptPay QR code payload
    promptpay_id = "0822154560"  # Replace with your PromptPay ID or make it configurable
    qr_image_data = None
    try:
        payload = qr_code.generate_payload(phone_number=promptpay_id, amount=float(total))
        qr = qrcode.make(payload)
        buffer = io.BytesIO()
        qr.save(buffer, format="PNG")
        qr_image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    except Exception as e:
        logger.error(f"Error generating PromptPay QR code: {str(e)}")
        messages.error(request, "เกิดข้อผิดพลาดในการสร้าง QR Code สำหรับชำระเงิน กรุณาลองใหม่อีกครั้ง")

    # Save cart items for display before clearing
    cart_items_list = list(cart_items)
    # Clear the cart after confirmation
    CartItem.objects.filter(cart__user=request.user).delete()
    messages.success(request, "ยืนยันคำสั่งซื้อเรียบร้อยแล้ว! กรุณาชำระเงินผ่าน QR Code")

    return render(request, 'store/order_confirmation.html', {
        'cart_items': cart_items_list,
        'total': total,
        'qr_image_data': qr_image_data
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "สมัครสมาชิกสำเร็จ! คุณได้เข้าสู่ระบบแล้ว")
            return redirect('store:index')
    else:
        form = UserCreationForm()
    return render(request, 'store/registration/register.html', {'form': form})

def about(request):
    return render(request, 'store/about.html')

@login_required
def get_cart_items(request):
    cart_items = CartItem.objects.filter(cart__user=request.user).select_related('product')
    data = {
        'cart_items': [
            {
                'id': item.id,
                'product': {
                    'id': item.product.id,
                    'name': item.product.name,
                    'price': float(item.product.price),
                    'image': item.product.image.url if item.product.image else '',
                },
                'quantity': int(item.quantity),
                'total_price': float(item.product.price * item.quantity),
            }
            for item in cart_items
        ]
    }
    return JsonResponse(data)

@login_required
def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'store/profile.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/products.html', {'products': products})

@login_required
def promptpay_qr(request):
    cart_items = CartItem.objects.filter(cart__user=request.user).select_related('product')
    if not cart_items:
        return HttpResponse("ตะกร้าของคุณว่างเปล่า", status=400)

    total = sum(
        Decimal(str(item.product.price)) * Decimal(str(item.quantity))
        for item in cart_items
    )
    if total <= 0:
        return HttpResponse("ยอดรวมไม่ถูกต้อง", status=400)

    promptpay_id = "0822154560"  # Replace with your PromptPay ID or make it configurable
    try:
        payload = qr_code.generate_payload(phone_number=promptpay_id, amount=float(total))
        qr = qrcode.make(payload)
        buffer = io.BytesIO()
        qr.save(buffer, format="PNG")
        logger.info(f"Generated PromptPay QR code for user {request.user.username}, total: {total}")
        return HttpResponse(buffer.getvalue(), content_type="image/png")
    except Exception as e:
        logger.error(f"Error generating PromptPay QR code: {str(e)}")
        return HttpResponse("เกิดข้อผิดพลาดในการสร้าง QR Code", status=500)