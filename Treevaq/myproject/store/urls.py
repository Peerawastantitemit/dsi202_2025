from django.contrib import admin
from django.urls import path, include
from store import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:pk>/<str:action>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('confirm_cart/', views.confirm_cart, name='confirm_cart'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('cart/get_cart_items/', views.get_cart_items, name='get_cart_items'),
    path('products/', views.product_list, name='products'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)