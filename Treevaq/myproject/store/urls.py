from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'store'  # Add this namespace

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:pk>/<str:action>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/confirm/', views.confirm_cart, name='confirm_cart'),
    path('cart/items/', views.get_cart_items, name='get_cart_items'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    
    # path('login/', auth_views.LoginView.as_view(), name='login'), # <--- อันนี้เป็น Django's LoginView
    path('promptpay_qr/', views.promptpay_qr, name='promptpay_qr'),
    path('register/', views.register, name='register'), # ดูเหมือนคุณมี register ด้วย
]