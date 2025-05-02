from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from .models import IPCamera, CartItem, NVR, HardDisk, OrderItem, Switch, PageView, Order
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Sum, F

def home(request):
    # Increment page view count
    page_view, created = PageView.objects.get_or_create(page_name="home")
    page_view.view_count += 1
    page_view.save()

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
        'view_count': page_view.view_count,
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

@require_POST
def update_cart_quantity(request, cart_item_id, action):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            return JsonResponse({'status': 'deleted'})

    # Calculate new cart total
    session_key = request.session.session_key
    cart_items = CartItem.objects.filter(session_key=session_key)
    cart_total = cart_items.aggregate(
        total=Sum(F('quantity') * F('camera__price'))
    )['total'] or 0

    return JsonResponse({
        'status': 'updated',
        'quantity': cart_item.quantity,
        'cart_total': cart_total,
    })

def view_cart(request):
    session_key = request.session.session_key
    cart_items = CartItem.objects.filter(session_key=session_key)
    return render(request, 'cart.html', {'cart_items': cart_items})

def nvr_list(request):
    nvr_items = NVR.objects.all()
    return render(request, 'nvr.html', {'nvr_items': nvr_items})

def harddisk_list(request):
    harddisks = HardDisk.objects.all()
    return render(request, 'harddisk.html', {'harddisks': harddisks})

def switch_list(request):
    switches = Switch.objects.all()
    return render(request, 'switch.html', {'switches': switches})

@require_POST
def place_order(request):
    session_key = request.session.session_key
    cart_items = CartItem.objects.filter(session_key=session_key)

    if not cart_items:
        return redirect('view_cart')

    # Calculate delivery cost
    delivery_type = request.POST.get('delivery_type')
    delivery_cost = 50 if delivery_type == 'delivery' else 0  # 50 TMT for delivery, 0 for pickup
    subtotal = cart_items.aggregate(
        total=Sum(F('quantity') * F('camera__price'))
    )['total'] or 0
    total_amount = subtotal + delivery_cost

    # Create order
    order = Order.objects.create(
        name=request.POST.get('name'),
        family_name=request.POST.get('family_name'),
        address=request.POST.get('address'),
        city=request.POST.get('city'),
        phone=request.POST.get('phone'),
        email=request.POST.get('email', ''),
        delivery_type=delivery_type,
        payment_method=request.POST.get('payment_method'),  # Re-added
        notes=request.POST.get('notes', ''),
        total_amount=total_amount,
    )

    # Associate cart items with the order
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            camera=item.camera,
            quantity=item.quantity,
            price=item.camera.price
        )

    # Clear the cart
    cart_items.delete()

    return redirect('order_confirmation', order_id=order.id)

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})