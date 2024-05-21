from django.contrib import admin
from .models import Item, Category, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'address', 'created_at', 'status']
    list_filter = ['status']
    search_fields = ['name', 'phone', 'address']
    inlines = [OrderItemInline]

    def save_model(self, request, obj, form, change):
        if obj.status == 'canceled' and obj.pk:
            order_items = OrderItem.objects.filter(order=obj)
            for order_item in order_items:
                item = order_item.item
                item.quantity += order_item.quantity
                item.save()
        super().save_model(request, obj, form, change)

# Register your models here.
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Order, OrderAdmin)