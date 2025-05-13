from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart_quantity/<int:pk>/<str:action>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/', views.cart, name='cart'),
    path('confirm_cart/', views.confirm_cart, name='confirm_cart'),
]