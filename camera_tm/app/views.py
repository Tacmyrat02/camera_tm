
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET
from .models import OrderItem, Product,Wishlist, CameraVariant, HardDiskVariant, NVRVariant, SwitchVariant, CartItem, Order
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.db.models import Q, Prefetch
from random import sample
from django.db.models import Sum,F
import logging

logger = logging.getLogger(__name__)


def home(request):
    # Group cameras by brand with all variants
    brands = ['UNV', 'TVT', 'Tiandy', 'Uniarch']
    cameras_by_brand = {}
    for brand in brands:
        products = Product.objects.filter(brand=brand, camera_variants__stock__gt=0).distinct()
        cameras_by_brand[brand] = {
            product: CameraVariant.objects.filter(product=product, stock__gt=0)
            for product in products
        }

    # Handle session and cart
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    cart_items = CartItem.objects.filter(session_key=session_key).prefetch_related(
        'camera_variant', 'harddisk_variant', 'nvr_variant', 'switch_variant'
    )
    cart_total = sum(
        (item.camera_variant.price if item.camera_variant else
         item.harddisk_variant.price if item.harddisk_variant else
         item.nvr_variant.price if item.nvr_variant else
         item.switch_variant.price) * item.quantity
        for item in cart_items if getattr(item, 'camera_variant', None) or
        getattr(item, 'harddisk_variant', None) or
        getattr(item, 'nvr_variant', None) or
        getattr(item, 'switch_variant', None)
    )

    # Select diverse featured products
    all_products = (
        Product.objects
        .filter(
            Q(camera_variants__stock__gt=0) | Q(harddisk_variants__stock__gt=0) |
            Q(nvr_variants__stock__gt=0) | Q(switch_variants__stock__gt=0)
        )
        .distinct()
    )
    featured_products = sample(list(all_products), min(4, all_products.count())) if all_products else []
    featured_products_with_variants = [
        {
            'product': product,
            'variants': (
                list(product.camera_variants.filter(stock__gt=0)) +
                list(product.harddisk_variants.filter(stock__gt=0)) +
                list(product.nvr_variants.filter(stock__gt=0)) +
                list(product.switch_variants.filter(stock__gt=0))
            )
        }
        for product in featured_products
    ]

    # Calculate total variants
    total_variants = (
        CameraVariant.objects.count() +
        HardDiskVariant.objects.count() +
        NVRVariant.objects.count() +
        SwitchVariant.objects.count()
    )

    context = {
        'cameras_by_brand': cameras_by_brand,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'featured_products': featured_products_with_variants,
        'total_variants': total_variants,  # Add to context
        'email': 'info@cameratm.com',
        'tiktok_link': 'https://tiktok.com/@cameratm',
        'instagram_link': 'https://instagram.com/cameratm',
        'linkedin_link': 'https://linkedin.com/company/cameratm',
        'imo_link': 'https://imo.im/cameratm',
    }
    return render(request, 'home.html', context)
def brand_cameras(request, brand):
    # Get products for the brand with at least one variant in stock
    products = Product.objects.filter(brand=brand, camera_variants__stock__gt=0).distinct()
    
    # Create a list of dictionaries with product and its variants
    product_list = [
        {
            'product': product,
            'variants': CameraVariant.objects.filter(product=product, stock__gt=0)
        }
        for product in products
    ]

    context = {
        'brand': brand,
        'products': product_list,  # Now a list of {'product': ..., 'variants': ...}
    }
    return render(request, 'brand_cameras.html', context)
def camera_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    variants = CameraVariant.objects.filter(product=product)
    context = {'product': product, 'variants': variants}
    return render(request, 'camera_detail.html', context)

def harddisk_list(request):
    products = Product.objects.filter(harddisk_variants__stock__gt=0).distinct()
    harddisk_variants = HardDiskVariant.objects.filter(product__in=products)
    context = {
        'products': products,
        'harddisk_variants': harddisk_variants,
    }
    return render(request, 'harddisk.html', context)
def nvr_list(request):
    products = Product.objects.filter(nvr_variants__stock__gt=0).distinct()
    nvr_variants = NVRVariant.objects.filter(product__in=products)
    context = {
        'products': products,
        'nvr_variants': nvr_variants,
    }
    return render(request, 'nvr.html', context)

def switch_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    variants = SwitchVariant.objects.filter(product=product)
    context = {
        'product': product,
        'variants': variants,
    }
    return render(request, 'switch_detail.html', context)

def nvr_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    variants = NVRVariant.objects.filter(product=product)
    context = {
        'product': product,
        'variants': variants,
    }
    return render(request, 'nvr_detail.html', context)

def switch_list(request):
    products = Product.objects.filter(switch_variants__stock__gt=0).distinct()
    switch_variants = SwitchVariant.objects.filter(product__in=products)
    context = {
        'products': products,
        'switch_variants': switch_variants,
    }
    return render(request, 'switch.html', context)
def add_to_cart(request, variant_id):
    if request.method == 'POST':
        if not request.session.session_key:
            request.session.create()

        variant_type = request.POST.get('variant_type')
        request_id = request.POST.get('request_id', 'unknown')
        session_key = request.session.session_key

        print(f"Add to Cart request received: variant_id={variant_id}, variant_type={variant_type}, request_id={request_id}, session_key={session_key}")

        if not variant_type:
            print(f"Error: Missing variant_type, request_id={request_id}")
            return JsonResponse({'success': False, 'error': _('Missing variant type')}, status=400)

        if variant_type not in ['camera', 'harddisk', 'nvr', 'switch']:
            print(f"Error: Invalid variant_type={variant_type}, request_id={request_id}")
            return JsonResponse({'success': False, 'error': _('Invalid variant type')}, status=400)

        try:
            cart_item_exists = CartItem.objects.filter(
                session_key=session_key,
                **{f"{variant_type}_variant_id": variant_id}
            ).exists()
            if cart_item_exists:
                print(f"Info: Item already in cart, variant_id={variant_id}, variant_type={variant_type}, request_id={request_id}")
                return JsonResponse({'success': False, 'error': _('Item already in cart')})

            cart_item = CartItem.objects.create(
                session_key=session_key,
                **{f"{variant_type}_variant_id": variant_id},
                quantity=1
            )
            print(f"Success: Item added, variant_id={variant_id}, variant_type={variant_type}, request_id={request_id}")
            return JsonResponse({'success': True, 'message': _('Item added to cart')})
        except Exception as e:
            print(f"Error: Failed to add item, variant_id={variant_id}, variant_type={variant_type}, request_id={request_id}, error={str(e)}")
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    print(f"Error: Invalid request method, request_id={request_id}")
    return JsonResponse({'success': False, 'error': _('Invalid request')}, status=400)
@require_GET
def view_cart(request):
      session_key = get_user_session_key(request)
      cart_items = []
      total_price = 0
      for item in CartItem.objects.filter(session_key=session_key):
          variant = (item.camera_variant or item.harddisk_variant or item.nvr_variant or item.switch_variant)
          if variant:
              subtotal = variant.price * item.quantity
              total_price += subtotal
              variant_type = next((t for t in ['camera', 'harddisk', 'nvr', 'switch'] if getattr(item, f'{t}_variant') == variant), None)
              all_variants = []
              if variant_type == 'camera':
                  all_variants = CameraVariant.objects.filter(product=variant.product, stock__gt=0)
              elif variant_type == 'harddisk':
                  all_variants = HardDiskVariant.objects.filter(product=variant.product, stock__gt=0)
              elif variant_type == 'nvr':
                  all_variants = NVRVariant.objects.filter(product=variant.product, stock__gt=0)
              elif variant_type == 'switch':
                  all_variants = SwitchVariant.objects.filter(product=variant.product, stock__gt=0)
              cart_items.append({
                  'item': item,
                  'variant': variant,
                  'variant_type': variant_type,
                  'subtotal': subtotal,
                  'all_variants': all_variants,
              })
      context = {
          'cart_items': cart_items,
          'total_price': total_price,
      }
      return render(request, 'cart.html', context)
@require_POST
def update_cart_quantity(request):
    item_id = request.POST.get('item_id')
    quantity = int(request.POST.get('quantity', 1))
    try:
        cart_item = CartItem.objects.get(id=item_id, session_key=request.session.session_key)
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        messages.success(request, _("Cart updated successfully."))
    except CartItem.DoesNotExist:
        messages.error(request, _("Cart item not found."))
    return redirect('view_cart')

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages

def place_order(request):
    if request.method == 'POST':
        session_key = get_user_session_key(request)
        cart_items = CartItem.objects.filter(session_key=session_key)
        if not cart_items.exists():
            messages.error(request, 'Your cart is empty.')
            return redirect('view_cart')

        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        if not all([full_name, phone_number, address]):
            messages.error(request, 'All fields are required.')
            return redirect('view_cart')

        order = Order.objects.create(
            full_name=full_name,
            phone_number=phone_number,
            address=address,
            total_price=sum(
                (item.camera_variant.price * item.quantity if item.camera_variant else
                 item.harddisk_variant.price * item.quantity if item.harddisk_variant else
                 item.nvr_variant.price * item.quantity if item.nvr_variant else
                 item.switch_variant.price * item.quantity if item.switch_variant else 0)
                for item in cart_items
            ),
        )

        for item in cart_items:
            variant = item.camera_variant or item.harddisk_variant or item.nvr_variant or item.switch_variant
            OrderItem.objects.create(
                order=order,
                camera_variant=item.camera_variant,
                harddisk_variant=item.harddisk_variant,
                nvr_variant=item.nvr_variant,
                switch_variant=item.switch_variant,
                quantity=item.quantity,
                price=variant.price if variant else 0,
            )

        cart_items.delete()

        # Detect if the user is on a mobile device
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        is_mobile = any(device in user_agent for device in ['mobile', 'android', 'iphone', 'ipad'])

        # Prepare the message body
        message_body = f"Order ID: {order.id}\nOrdered Items: {order.get_order_summary()}"

        # Prepare the redirect URL
        if is_mobile:
            redirect_url = f"sms:+99365455558?body={message_body.replace(' ', '%20')}"
        else:
            redirect_url = f"mailto:admin@cameratm.com?subject=New%20Order%20Notification&body={message_body.replace(' ', '%20')}"

        messages.success(request, 'Order placed successfully! Redirecting to confirm your order...')
        return render(request, 'order_confirmation.html', {
            'redirect_url': redirect_url,
            'is_mobile': is_mobile,
            'order': order,
        })

    return render(request, 'cart.html')

def order_confirmation(request):
      return render(request, 'order_confirmation.html')
######
def get_user_session_key(request):
       """
       Helper function to get or create the user's session key.
       """
       if not request.session.session_key:
           request.session.save()  # Create a session if it doesn't exist
       return request.session.session_key

@require_POST
def add_to_wishlist(request, product_id):
      user_session_key = get_user_session_key(request)
      try:
          product = Product.objects.get(id=product_id)
          wishlist_item, created = Wishlist.objects.get_or_create(
              user_session_key=user_session_key,
              product=product
          )
          if created:
              messages.success(request, 'Product added to wishlist successfully.')
          else:
              messages.info(request, 'This product is already in your wishlist.')
          return JsonResponse({'success': True})
      except Product.DoesNotExist:
          return JsonResponse({'success': False, 'error': 'Product not found'}, status=404)
      except Exception as e:
          return JsonResponse({'success': False, 'error': str(e)}, status=400)

@require_GET
def wishlist_view(request):
      user_session_key = get_user_session_key(request)
      wishlist_items = Wishlist.objects.filter(user_session_key=user_session_key).select_related('product')
      context = {
          'wishlist_items': wishlist_items,
      }
      return render(request, 'wishlist.html', context)

@require_POST
def remove_from_wishlist(request, product_id):
    user_session_key = get_user_session_key(request)
    try:
        product = Product.objects.get(id=product_id)
        wishlist_item = Wishlist.objects.get(user_session_key=user_session_key, product=product)
        wishlist_item.delete()
        messages.success(request, 'Product removed from wishlist.')
        return JsonResponse({'success': True})
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Product not found'}, status=404)
    except Wishlist.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Wishlist item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
def get_wishlist_count(request):
    try:
        user_session_key = get_user_session_key(request)
        count = Wishlist.objects.filter(user_session_key=user_session_key).count()
        return JsonResponse({'count': count})
    except Exception as e:
        logger.error(f"Failed to fetch wishlist count: {str(e)}")
        return JsonResponse({'count': 0}, status=500)
def get_cart_count(request):
    session_key = request.session.session_key
    if not session_key:
        count = 0
    else:
        count = CartItem.objects.filter(session_key=session_key).count()
    return JsonResponse({'count': count})






# from django.shortcuts import render, get_object_or_404
# from django.core.files.storage import FileSystemStorage
# import cv2
# import numpy as np
# from .models import Product
# from .forms import ImageUploadForm
# from PIL import Image
# import io

# def some_similarity_check(img1, img2):
#     img1_resized = cv2.resize(img1, (128, 128))
#     img2_resized = cv2.resize(img2, (128, 128))

#     hist1 = cv2.calcHist([img1_resized], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
#     hist2 = cv2.calcHist([img2_resized], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])

#     cv2.normalize(hist1, hist1)
#     cv2.normalize(hist2, hist2)

#     similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

#     return similarity

# def find_similar_products(reference_image):
#     products = Product.objects.all()
#     similar_products = []

#     for product in products:
#         product_image = cv2.imread(product.image.path)  # Adjust path as necessary
#         if product_image is not None:
#             score = some_similarity_check(reference_image, product_image)
#             similar_products.append((product, score))

#     # Sort by similarity score in descending order
#     similar_products.sort(key=lambda x: x[1], reverse=True)

#     return similar_products

# def image_search(request):
#     if request.method == 'POST':
#         uploaded_image = request.FILES['image']
        
#         # Convert InMemoryUploadedFile to a format OpenCV can read
#         img = Image.open(uploaded_image)
#         img_array = np.array(img)
        
#         # Convert RGB to BGR (OpenCV uses BGR)
#         reference_image = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

#         similar_products = find_similar_products(reference_image)

#         if similar_products:
#             return render(request, 'search/results.html', {'similar_products': similar_products})
#         else:
#             return render(request, 'search/no_results.html')
    
#     return render(request, 'search/upload.html')
from django.shortcuts import render

def search(request):
    query = request.GET.get('q', '')
    image_query = request.GET.get('image', '')
    results = []

    if query:
        # Text search: look for matches in brand, model_name, and description
        results = Product.objects.filter(
            Q(brand__icontains=query) |
            Q(model_name__icontains=query) |
            Q(description__icontains=query)
        ).distinct()

    elif image_query:
        # Image search: placeholder logic (matching filename as a demo)
        # In a real implementation, you'd use an image recognition API here
        results = Product.objects.filter(
            image__icontains=image_query
        ).distinct()

    context = {
        'query': query,
        'image_query': image_query,
        'results': results,
    }
    return render(request, 'search_results.html', context)

def image_search(request):
    if request.method == 'POST':
        # Placeholder for image processing
        # You would typically process the image here using an API like Google Vision
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
from django.shortcuts import render, get_object_or_404

def harddisk_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    variants = HardDiskVariant.objects.filter(product=product)
    context = {
        'product': product,
        'variants': variants,
    }
    return render(request, 'harddisk_detail.html', context)


def remove_from_cart(request, item_id):
    if request.method == 'POST':
        # Ensure the session key exists
        if not request.session.session_key:
            request.session.create()

        try:
            # Remove the item
            item = CartItem.objects.get(id=item_id, session_key=request.session.session_key)
            item.delete()

            # Calculate total price dynamically
            total_price = (CartItem.objects
                         .filter(session_key=request.session.session_key)
                         .annotate(total_price=F('quantity') * F('camera_variant__price'))  # Adjust based on variant type
                         .aggregate(total=Sum('total_price'))['total'] or 0)
            # Add fallback for other variant types if needed
            if total_price == 0:
                total_price = (CartItem.objects
                             .filter(session_key=request.session.session_key)
                             .annotate(total_price=F('quantity') * F('harddisk_variant__price'))
                             .aggregate(total=Sum('total_price'))['total'] or 0)
                if total_price == 0:
                    total_price = (CartItem.objects
                                 .filter(session_key=request.session.session_key)
                                 .annotate(total_price=F('quantity') * F('nvr_variant__price'))
                                 .aggregate(total=Sum('total_price'))['total'] or 0)
                    if total_price == 0:
                        total_price = (CartItem.objects
                                     .filter(session_key=request.session.session_key)
                                     .annotate(total_price=F('quantity') * F('switch_variant__price'))
                                     .aggregate(total=Sum('total_price'))['total'] or 0)

            return JsonResponse({'success': True, 'total_price': total_price})
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False}, status=404)
    return JsonResponse({'success': False}, status=400)
@require_POST
def update_cart_variant(request):
    item_id = request.POST.get('item_id')
    new_variant_id = request.POST.get('variant_id')
    variant_type = request.POST.get('variant_type')

    if not all([item_id, new_variant_id, variant_type]):
        return JsonResponse({'success': False, 'error': _('Missing required fields')}, status=400)

    if variant_type not in ['camera', 'harddisk', 'nvr', 'switch']:
        return JsonResponse({'success': False, 'error': _('Invalid variant type')}, status=400)

    try:
        cart_item = CartItem.objects.get(id=item_id, session_key=request.session.session_key)
        cart_item.camera_variant = None
        cart_item.harddisk_variant = None
        cart_item.nvr_variant = None
        cart_item.switch_variant = None

        if variant_type == 'camera':
            new_variant = CameraVariant.objects.get(id=new_variant_id, stock__gt=0)
            cart_item.camera_variant = new_variant
        elif variant_type == 'harddisk':
            new_variant = HardDiskVariant.objects.get(id=new_variant_id, stock__gt=0)
            cart_item.harddisk_variant = new_variant
        elif variant_type == 'nvr':
            new_variant = NVRVariant.objects.get(id=new_variant_id, stock__gt=0)
            cart_item.nvr_variant = new_variant
        elif variant_type == 'switch':
            new_variant = SwitchVariant.objects.get(id=new_variant_id, stock__gt=0)
            cart_item.switch_variant = new_variant

        cart_item.save()

        subtotal = new_variant.price * cart_item.quantity
        total_price = sum(
            (item.camera_variant.price if item.camera_variant else
             item.harddisk_variant.price if item.harddisk_variant else
             item.nvr_variant.price if item.nvr_variant else
             item.switch_variant.price) * item.quantity
            for item in CartItem.objects.filter(session_key=request.session.session_key)
            if item.camera_variant or item.harddisk_variant or item.nvr_variant or item.switch_variant
        )

        variant_details = {
            'price': float(new_variant.price),
            'subtotal': float(subtotal)
        }
        if variant_type == 'camera':
            variant_details['spec'] = new_variant.resolution
        elif variant_type == 'harddisk':
            variant_details['spec'] = new_variant.storage_capacity
        elif variant_type in ['nvr', 'switch']:
            variant_details['spec'] = str(new_variant.channels)

        return JsonResponse({
            'success': True,
            'total_price': float(total_price),
            'variant_details': variant_details
        })
    except (CartItem.DoesNotExist, CameraVariant.DoesNotExist, HardDiskVariant.DoesNotExist, NVRVariant.DoesNotExist, SwitchVariant.DoesNotExist):
        return JsonResponse({'success': False, 'error': _('Item or variant not found')}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
