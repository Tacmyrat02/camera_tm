from django.db import models

class Product(models.Model):
      brand = models.CharField(max_length=100)
      model_name = models.CharField(max_length=100)
      description = models.TextField()
      image = models.ImageField(upload_to='products/')

      def __str__(self):
          return f"{self.brand} {self.model_name}"

class CameraVariant(models.Model):
      product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='camera_variants')
      resolution = models.CharField(max_length=50)
      price = models.DecimalField(max_digits=10, decimal_places=2)
      stock = models.PositiveIntegerField(default=0)

      def __str__(self):
          return f"{self.product} - {self.resolution}"

class HardDiskVariant(models.Model):
      product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='harddisk_variants')
      storage_capacity = models.CharField(max_length=50)
      price = models.DecimalField(max_digits=10, decimal_places=2)
      stock = models.PositiveIntegerField(default=0)

      def __str__(self):
          return f"{self.product} - {self.storage_capacity}"

class NVRVariant(models.Model):
      product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='nvr_variants')
      channels = models.PositiveIntegerField()
      price = models.DecimalField(max_digits=10, decimal_places=2)
      stock = models.PositiveIntegerField(default=0)

      def __str__(self):
          return f"{self.product} - {self.channels} channels"

class SwitchVariant(models.Model):
      product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='switch_variants')
      channels = models.PositiveIntegerField()
      price = models.DecimalField(max_digits=10, decimal_places=2)
      stock = models.PositiveIntegerField(default=0)

      def __str__(self):
          return f"{self.product} - {self.channels} ports"

class CartItem(models.Model):
      session_key = models.CharField(max_length=40)
      camera_variant = models.ForeignKey(CameraVariant, on_delete=models.CASCADE, null=True, blank=True)
      harddisk_variant = models.ForeignKey(HardDiskVariant, on_delete=models.CASCADE, null=True, blank=True)
      nvr_variant = models.ForeignKey(NVRVariant, on_delete=models.CASCADE, null=True, blank=True)
      switch_variant = models.ForeignKey(SwitchVariant, on_delete=models.CASCADE, null=True, blank=True)
      quantity = models.PositiveIntegerField(default=1)
      added_at = models.DateTimeField(auto_now_add=True)  # Added this field

      def __str__(self):
          variant = self.camera_variant or self.harddisk_variant or self.nvr_variant or self.switch_variant
          return f"CartItem: {variant} (Qty: {self.quantity})"
from django.db import models

class Order(models.Model):
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.full_name}"

    def get_order_summary(self):
        """Returns a string summary of the items in this order."""
        items = self.items.all()
        summary = []
        for item in items:
            variant = item.camera_variant or item.harddisk_variant or item.nvr_variant or item.switch_variant
            if variant:
                product = variant.product
                variant_detail = (
                    variant.resolution if hasattr(variant, 'resolution') else
                    variant.storage_capacity if hasattr(variant, 'storage_capacity') else
                    f"{variant.channels}CH" if hasattr(variant, 'channels') and item.nvr_variant else
                    f"{variant.channels}-port" if hasattr(variant, 'channels') and item.switch_variant else "Unknown"
                )
                summary.append(f"{product.brand} {product.model_name} ({variant_detail}) x {item.quantity}")
        return "; ".join(summary) if summary else "No items ordered"

    def get_item_count(self):
        """Returns the total number of items (quantities summed) in the order."""
        return sum(item.quantity for item in self.items.all())
class OrderItem(models.Model):
      order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
      camera_variant = models.ForeignKey(CameraVariant, on_delete=models.SET_NULL, null=True, blank=True)
      harddisk_variant = models.ForeignKey(HardDiskVariant, on_delete=models.SET_NULL, null=True, blank=True)
      nvr_variant = models.ForeignKey(NVRVariant, on_delete=models.SET_NULL, null=True, blank=True)
      switch_variant = models.ForeignKey(SwitchVariant, on_delete=models.SET_NULL, null=True, blank=True)
      quantity = models.PositiveIntegerField()
      price = models.DecimalField(max_digits=10, decimal_places=2)

      def __str__(self):
          variant = self.camera_variant or self.harddisk_variant or self.nvr_variant or self.switch_variant
          return f"OrderItem: {variant} (Qty: {self.quantity})"
class Wishlist(models.Model):
    user_session_key = models.CharField(max_length=40)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user_session_key', 'product'),)

    def __str__(self):
        return f"Wishlist: {self.product} for {self.user_session_key}"