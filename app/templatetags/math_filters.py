# myapp/templatetags/math_filters.py
from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def sum_cart_total(cart_items):
    try:
        return sum(item.quantity * item.camera.price for item in cart_items)
    except (AttributeError, TypeError):
        return 0
