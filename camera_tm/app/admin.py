from django.contrib import admin
from .models import Order, OrderItem, Product, CameraVariant, HardDiskVariant, NVRVariant, SwitchVariant, CartItem, Wishlist

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('camera_variant', 'harddisk_variant', 'nvr_variant', 'switch_variant', 'quantity', 'price')
    can_delete = False

    def get_variant(self, obj):
        variant = obj.camera_variant or obj.harddisk_variant or obj.nvr_variant or obj.switch_variant
        if variant:
            return str(variant)
        return "N/A"
    get_variant.short_description = 'Variant'

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id_display', 'full_name', 'phone_number', 'address', 'total_price', 'get_item_count', 'created_at', 'get_order_summary')
    list_filter = ('created_at',)
    search_fields = ('id', 'full_name', 'phone_number')
    inlines = [OrderItemInline]

    def order_id_display(self, obj):
        return f"ORD-{obj.id}"
    order_id_display.short_description = 'Order ID'

    def get_order_summary(self, obj):
        return obj.get_order_summary()
    get_order_summary.short_description = 'Order Summary'

    def get_item_count(self, obj):
        return obj.get_item_count()
    get_item_count.short_description = 'Total Items'

admin.site.register(Order, OrderAdmin)
admin.site.register(Product)
admin.site.register(CameraVariant)
admin.site.register(HardDiskVariant)
admin.site.register(NVRVariant)
admin.site.register(SwitchVariant)
admin.site.register(CartItem)
admin.site.register(Wishlist)