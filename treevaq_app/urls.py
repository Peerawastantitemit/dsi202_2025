# my_django_project/treevaq_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'), # Corrected this line
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart_quantity/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('checkout/payment/', views.checkout_payment_view, name='checkout_payment'),
    path('generate_qr/', views.generate_qr_code_image, name='generate_qr_code_image'),
    path('register/', views.register, name='register'),
    path('profile/', views.user_profile, name='user_profile'),
]