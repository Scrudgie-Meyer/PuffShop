from django.db import models
from ckeditor.fields import RichTextField

# Модель категорії
class Category(models.Model):
    name = models.CharField('Name', max_length=50)
    image_url = models.CharField('Image URL', max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.id}'


# Модель товару
class Item(models.Model):
    name = models.CharField('Name', max_length=50, null=True)
    price = models.DecimalField('Price', max_digits=10, decimal_places=2)
    quantity = models.IntegerField('Quantity', default=0)
    description = RichTextField('Description', default='Description')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='items', blank=True, null=True)
    image_urls = models.JSONField('Image URLs', default=list)
    attributes = models.JSONField('Attributes', default=dict)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.id}'

class Order(models.Model):
    name = models.CharField('Name', max_length=50)
    phone = models.CharField('Phone', max_length=20, blank=True)
    address = models.CharField('Address', max_length=255, blank=True, null=True)
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
        return f'Order {self.id} by {self.phone}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')  # Зв'язок із замовленням
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # Зв'язок із товаром
    name = models.CharField('Name', max_length=50)
    price = models.DecimalField('Price', max_digits=10, decimal_places=2)
    quantity = models.IntegerField('Quantity', default=0)
    description = models.TextField('Description', null=True)

    def __str__(self):
        return f'{self.quantity} x {self.name}'
