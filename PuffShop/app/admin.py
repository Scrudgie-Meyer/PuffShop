from django.contrib import admin
from .models import Item, Category, Order, UserProfile, Cart, CartItem, OrderItem

admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(UserProfile)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)
