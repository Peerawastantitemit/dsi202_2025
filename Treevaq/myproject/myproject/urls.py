from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('tadmin/', admin.site.urls),
    path('', include('store.urls')),
]