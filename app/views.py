from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from .models import IPCamera , CartItem

def home(request):
    cameras_by_brand = {
        'UNV': IPCamera.objects.filter(model_name__icontains='UNV'),
        'TVT': IPCamera.objects.filter(model_name__icontains='TVT'),
        'Tiandy': IPCamera.objects.filter(model_name__icontains='Tiandy'),
        'Uniarch': IPCamera.objects.filter(model_name__icontains='Uniarch'),
    }

    context = {
        'company_name': _('CameraTM'),
        'about_us_text': _('Welcome to CameraTM! We specialize in providing high-quality IP cameras and reliable home phone systems to meet your security and communication needs. Our mission is to offer innovative and user-friendly solutions with excellent customer support.'),
        'email': 'info@cameratm.com',
        'tiktok_link': 'https://www.tiktok.com/@camera.tm',
        'instagram_link': 'https://www.instagram.com/cameratm/',
        'linkedin_link': 'https://www.linkedin.com/company/cameratm',
        'imo_link': 'https://imo.im/c/CameraTM',
        'cameras_by_brand': cameras_by_brand,
    }
    return render(request, 'home.html', context)
def brand_cameras(request, brand):
    cameras = IPCamera.objects.filter(model_name__icontains=brand)
    context = {
        'brand': brand,
        'cameras': cameras
    }
    return render(request, 'brand_cameras.html', context)
def add_to_cart(request, camera_id):
    camera = IPCamera.objects.get(id=camera_id)
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_item, created = CartItem.objects.get_or_create(
        camera=camera,
        session_key=session_key,
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')
def view_cart(request):
    session_key = request.session.session_key
    cart_items = CartItem.objects.filter(session_key=session_key)
    return render(request, 'cart.html', {'cart_items': cart_items})

from django.shortcuts import render
from .models import NVR  # Assuming you have an NVR model

def nvr_list(request):
    nvr_items = NVR.objects.all()  # Get all NVR items
    return render(request, 'nvr.html', {'nvr_items': nvr_items})
from django.shortcuts import render
from .models import HardDisk

def harddisk_list(request):
    harddisks = HardDisk.objects.all()  # Get all hard disk items
    return render(request, 'harddisk.html', {'harddisks': harddisks})
from django.shortcuts import render
from .models import Switch, NVR  # Assuming you have the Switch model

def switch_list(request):
    switches = Switch.objects.all()  # Fetch all switches
    return render(request, 'switch.html', {'switches': switches})
