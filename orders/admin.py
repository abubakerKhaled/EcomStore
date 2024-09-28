from django.contrib import admin
from .models.order_model import Order
from .models.order_item_model import OrderItem
from .forms import OrderItemForm

class OrderItemInline(admin.TabularInline):
    model = OrderItem  # This ensures it references the correct model
    form = OrderItemForm  # Use the custom form for the inline
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'last_name',
        'email',
        'address',
        'postal_code',
        'city',
        'paid',
        'created',
        'updated',
    ]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]