from decimal import Decimal
from django.db import models
class IPCamera(models.Model):
    model_name = models.CharField(max_length=255)
    features = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to='images/cameras/')
    available_mps = models.JSONField(default=list)  # e.g., [12, 16, 20]

    def __str__(self):
        return self.model_name

    def get_price_for_mp(self, mp):
        return self.base_price + (Decimal(mp) * Decimal('50.00'))

    @property
    def default_price(self):
        return self.get_price_for_mp(self.available_mps[0]) if self.available_mps else 0
class HomePhone(models.Model):
    model_name = models.CharField(max_length=255)
    features = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    num_handsets = models.IntegerField(default=1)
    image = models.ImageField(upload_to='images/phones/')

    def __str__(self):
        return self.model_name

class CartItem(models.Model):
    camera = models.ForeignKey(IPCamera, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    session_key = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.camera.model_name} ({self.quantity})"

class NVR(models.Model):
    model_name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    channels = models.IntegerField()
    storage_capacity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.model_name

class Switch(models.Model):
    model_name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    ports = models.IntegerField()
    speed = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.brand} {self.model_name}"

class HardDisk(models.Model):
    storage_capacity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.storage_capacity}GB - ${self.price}"

class PageView(models.Model):
    page_name = models.CharField(max_length=100, unique=True)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.page_name}: {self.view_count} views"

class Order(models.Model):
    DELIVERY_TYPE_CHOICES = [
        ('pickup', 'Pickup'),
        ('delivery', 'Delivery'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('online', 'Online Payment'),
    ]

    name = models.CharField(max_length=255)
    family_name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_TYPE_CHOICES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)  # Re-added
    notes = models.TextField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.name} {self.family_name} on {self.created_at}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    camera = models.ForeignKey(IPCamera, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.camera.model_name} in Order {self.order.id}"