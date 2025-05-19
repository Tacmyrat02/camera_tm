from django.contrib import admin
from django.urls import path, include
from app.views import add_to_wishlist,order_confirmation,update_cart_variant,remove_from_cart,switch_detail,nvr_detail,harddisk_detail,search,image_search,get_cart_count, get_wishlist_count, harddisk_list, camera_detail,home, brand_cameras, nvr_list, remove_from_wishlist, view_cart, add_to_cart, switch_list, update_cart_quantity, place_order, wishlist_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('search/', search, name='search'),
    path('image_search/', image_search, name='image_search'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('camera/<int:product_id>/',camera_detail, name='camera_detail'),
    path('cart/add/<int:variant_id>/', add_to_cart, name='add_to_cart'),
    path('cart/count/', get_cart_count, name='get_cart_count'),
    path('cart/', view_cart, name='view_cart'),
    path('update_cart_quantity/', update_cart_quantity, name='update_cart_quantity'),
    path('place_order/', place_order, name='place_order'),
    path('brand/<str:brand>/',brand_cameras, name='brand_cameras'),
    path('harddisk/', harddisk_list, name='harddisk_list'),
    path('nvr/', nvr_list, name='nvr_list'),
    path('nvr/<int:product_id>/', nvr_detail, name='nvr_detail'),
    path('switch/', switch_list, name='switch_list'),
    path('order_confirmation/', order_confirmation, name='order_confirmation'),
    path('switch/<int:product_id>/', switch_detail, name='switch_detail'),
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/',remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/count/', get_wishlist_count, name='get_wishlist_count'),
    path('wishlist/', wishlist_view, name='wishlist_view'),
    path('cart/update-variant/', update_cart_variant, name='update_cart_variant'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('harddisk/<int:product_id>/', harddisk_detail, name='harddisk_detail'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)