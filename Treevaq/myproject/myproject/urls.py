# dsi202/Treevaq/myproject/myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store import views as store_views # <--- Import views จากแอป store

urlpatterns = [
    path('', store_views.index, name='home'), # <--- ทำให้ path ว่าง ชี้ไปที่ store_views.index
    path('admin/', admin.site.urls),
    # path('accounts/', ...),
    # path('auth/', ...),
    path('store/', include('store.urls')), # URL อื่นๆ ของ store จะอยู่ที่ /store/...
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 