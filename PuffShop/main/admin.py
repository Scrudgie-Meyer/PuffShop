from django.contrib import admin
from .models import Item, Category, Order, OrderItem

# Register your models here.
admin.site.register(Item)
admin.site.register(Category)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'address', 'created_at', 'status']
    list_filter = ['status']
    search_fields = ['name', 'phone', 'address']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)