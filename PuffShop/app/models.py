from django.db import models
from django.contrib.auth.models import User

# Модель категорії
class Category(models.Model):
    name = models.CharField('Name', max_length=50)

    def __str__(self):
        return self.name

# Модель товару
class Item(models.Model):
    name = models.CharField('Name', max_length=50)
    price = models.DecimalField('Price', max_digits=10, decimal_places=2)
    quantity = models.IntegerField('Quantity')
    description = models.TextField('Description')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return self.name

# Модель профілю користувача
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField('Phone', max_length=20, blank=True, null=True)
    address = models.CharField('Address', max_length=255, blank=True, null=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

# Модель корзини
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    items = models.ManyToManyField(Item, through='CartItem')

    def __str__(self):
        return f'Cart of {self.user.username}'

# Модель позиції в корзині
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField('Quantity', default=1)

    def __str__(self):
        return f'{self.quantity} x {self.item.name}'

# Модель замовлення
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField(Item, through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField('Status', max_length=20, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ])

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

# Модель позиції в замовленні
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField('Quantity', default=1)
    price = models.DecimalField('Price', max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} x {self.item.name}'
