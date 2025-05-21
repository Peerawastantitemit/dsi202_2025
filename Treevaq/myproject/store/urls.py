from django.urls import path
from . import views

app_name = 'store'  # Add this namespace

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:pk>/<str:action>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/', views.cart, name='cart'),  # This is the missing URL pattern
    path('cart/confirm/', views.confirm_cart, name='confirm_cart'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
]
