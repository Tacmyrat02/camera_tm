from django.contrib import admin
from django.urls import path, include
from app.views import harddisk_list, home , brand_cameras, nvr_list,view_cart,add_to_cart,switch_list
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('brand/<str:brand>/', brand_cameras, name='brand_cameras'),
    path('add-to-cart/<int:camera_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('switches/', switch_list, name='switch_list'),
    path('nvrs/', nvr_list, name='nvr_list'),
    path('harddisk/', harddisk_list, name='harddisk_list'),
]
    # ... other URLs
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)