from django.db import models

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
    name = models.CharField('Name', max_length=50)
    price = models.DecimalField('Price', max_digits=10, decimal_places=2)
    quantity = models.IntegerField('Quantity')
    description = models.TextField('Description')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='items', blank=True, null=True)
    image_urls = models.JSONField('Image URLs', default=list)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.id}'