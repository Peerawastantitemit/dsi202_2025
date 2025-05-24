# my_django_project/treevaq_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login # Added: Import login function
from .models import Product, Cart, CartItem
from .forms import AddToCartForm, UpdateCartQuantityForm
import io
import qrcode
from .qr_utils import generate_promptpay_qr_payload, QRError, InvalidInputError
from decimal import Decimal

def home(request):
    context = {
        'company_name': 'Treevaq',
        'slogan': 'Value in Every Alternative, Quality for a Greener World',
        'hero_text': 'Shop Eco-Friendly Products for a Sustainable Future.',
        'call_to_action': 'Explore Our Collection'
    }
    return render(request, 'treevaq_app/home.html', context)

def products(request):
    all_products = Product.objects.all().filter(is_active=True)
    context = {
        'company_name': 'Treevaq',
        'products': all_products
    }
    return render(request, 'treevaq_app/products.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Get or create the cart for the current logged-in user
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Get quantity from the form, default to 1 if not provided or invalid
    quantity = 1
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            quantity = 1 # Fallback to 1 if quantity is not a valid number

    # Get or create the CartItem for the product in this cart
    # If it exists, 'item_created' will be False, and we update quantity
    # If it's new, 'item_created' will be True
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if quantity > 0:
        if not item_created: # If item already existed, add to its quantity
            cart_item.quantity += quantity
        else: # If it's a new item, set its quantity
            cart_item.quantity = quantity
        cart_item.save()
    elif not item_created: # If quantity is 0 or less, and item already exists, remove it
        cart_item.delete()

    # Redirect to the cart detail page after adding/updating
    return redirect('cart_detail')

@login_required
def user_profile(request):
    # The request.user object contains the current logged-in user's information
    # No need to fetch it from the database explicitly if using @login_required

    # You can fetch other related data here, e.g., user's past orders
    # from .models import Order # Assuming you'll have an Order model later
    # user_orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'user': request.user,
        # 'user_orders': user_orders, # Uncomment when you have an Order model
        'company_name': 'Treevaq',
    }
    return render(request, 'treevaq_app/user_profile.html', context)


@login_required
def cart_detail(request):
    cart = None
    cart_items = []
    total_price = Decimal('0.00')

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
        total_price = cart.get_total_price()
    # No 'else' block for anonymous cart for now, as system assumes logged-in user for cart actions

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'update_quantity_form': UpdateCartQuantityForm(), # Pass the form to the template
    }
    return render(request, 'treevaq_app/cart_detail.html', context)

def register(request):
    from .forms import CustomUserCreationForm # Ensure CustomUserCreationForm is imported here or at the top
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home') # Or 'products' or desired page after registration
    else:
        form = CustomUserCreationForm()

    context = {
        'company_name': 'Treevaq',
        'form': form
    }
    return render(request, 'registration/register.html', context)

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart_detail')

@login_required
def update_cart_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        form = UpdateCartQuantityForm(request.POST, instance=cart_item)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete() # Remove item if quantity is 0 or less
            return redirect('cart_detail')
    return redirect('cart_detail') # Redirect back even if not POST or form invalid

@login_required
def checkout_payment_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    total_amount = cart.get_total_price()

    context = {
        'total_amount': total_amount,
        'merchant_promptpay_id': '0822154560', # IMPORTANT: REPLACE WITH YOUR ACTUAL PROMPTPAY ID
    }
    return render(request, 'treevaq_app/checkout_payment.html', context)

def generate_qr_code_image(request):
    mobile_number = request.GET.get('mobile', None)
    nid = request.GET.get('nid', None)
    amount = request.GET.get('amount', None)

    if not (mobile_number or nid):
        return HttpResponse("Error: Missing PromptPay ID (mobile or NID).", status=400)
    if not amount:
        return HttpResponse("Error: Missing amount.", status=400)

    try:
        amount_decimal = Decimal(amount)
        if amount_decimal <= 0:
            return HttpResponse("Error: Amount must be positive.", status=400)
        amount_float = float(amount_decimal)

        payload = generate_promptpay_qr_payload(
            mobile=mobile_number,
            nid=nid,
            amount=amount_float,
            one_time=True
        )

        qr_img_obj = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr_img_obj.add_data(payload)
        qr_img_obj.make(fit=True)

        img = qr_img_obj.make_image(fill_color="black", back_color="white")

        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        return HttpResponse(img_byte_arr.getvalue(), content_type="image/png")

    except (QRError, InvalidInputError) as e:
        return HttpResponse(f"Error generating QR payload: {e}", status=400)
    except ValueError:
        return HttpResponse("Error: Invalid amount format.", status=400)
    except Exception as e:
        return HttpResponse(f"An unexpected error occurred: {e}", status=500)