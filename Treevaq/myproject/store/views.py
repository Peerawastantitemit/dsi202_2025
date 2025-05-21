import os
import qrcode
import io
import logging
from django.http import HttpResponse, JsonResponse
from promptpay import qr_code
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Cart
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Set up logging
logger = logging.getLogger(__name__)

def index(request):
    query = request.GET.get('q', '').strip()
    if query:
        products = Product.objects.filter(name__icontains=query) | Product.objects.filter(description__icontains=query)
    else:
        products = Product.objects.all()
    
    cart_items = Cart.objects.filter(user=request.user).select_related('product') if request.user.is_authenticated else []
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
    return redirect('store:cart')

@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(Cart, pk=pk, user=request.user)
    cart_item.delete()
    messages.success(request, "ลบสินค้าออกจากตะกร้าแล้ว!")
    return redirect('store:cart')

@login_required
def update_cart_quantity(request, pk, action):
    cart_item = get_object_or_404(Cart, pk=pk, user=request.user)
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()
    messages.success(request, "อัปเดตจำนวนสินค้าเรียบร้อยแล้ว!")
    return redirect('store:cart')

@login_required
def cart(request):
    # Use select_related to optimize database queries
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    # Ensure total is a Decimal to avoid floating-point issues
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

    # Fetch cart items and calculate total
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
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
    try:
        payload = qr_code.generate_payload(phone_number=promptpay_id, amount=total)
        qr = qrcode.make(payload)
        buffer = io.BytesIO()
        qr.save(buffer, format="PNG")
        qr_image_data = buffer.getvalue()
    except Exception as e:
        logger.error(f"Error generating PromptPay QR code: {str(e)}")
        messages.error(request, "เกิดข้อผิดพลาดในการสร้าง QR Code สำหรับชำระเงิน กรุณาลองใหม่อีกครั้ง")
        qr_image_data = None

    # Clear the cart after confirmation
    Cart.objects.filter(user=request.user).delete()
    messages.success(request, "ยืนยันคำสั่งซื้อเรียบร้อยแล้ว! กรุณาชำระเงินผ่าน QR Code")

    return render(request, 'store/order_confirmation.html', {
        'cart_items': cart_items,
        'total': total,
        'qr_image_data': qr_image_data  # Pass QR code data to template
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "สมัครสมาชิกสำเร็จ! ยินดีต้อนรับสู่ Treevaq")
            return redirect('store:index')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def about(request):
    return render(request, 'store/about.html')

@login_required
def get_cart_items(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    data = {
        'cart_items': []
    }
    for item in cart_items:
        price = float(item.product.price) if item.product.price else 0.0
        quantity = int(item.quantity) if item.quantity else 0
        total_price = price * quantity
        data['cart_items'].append({
            'id': item.id,
            'product': {
                'id': item.product.id,
                'name': item.product.name,
                'price': price,
                'image': item.product.image.url if item.product.image else '',
            },
            'quantity': quantity,
            'total_price': total_price,
        })
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
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
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
        payload = qr_code.generate_payload(phone_number=promptpay_id, amount=total)
        qr = qrcode.make(payload)
        buffer = io.BytesIO()
        qr.save(buffer, format="PNG")
        logger.info(f"Generated PromptPay QR code for user {request.user.username}, total: {total}")
        return HttpResponse(buffer.getvalue(), content_type="image/png")
    except Exception as e:
        logger.error(f"Error generating PromptPay QR code: {str(e)}")
        return HttpResponse("เกิดข้อผิดพลาดในการสร้าง QR Code", status=500)