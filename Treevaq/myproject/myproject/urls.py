from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('api/', include('rest_framework.urls')),  # เพิ่มสำหรับ API
]