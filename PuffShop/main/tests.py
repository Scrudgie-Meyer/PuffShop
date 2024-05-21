from django.test import TestCase
from django.urls import reverse
from .models import Category, Item

class IndexViewTest(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')



class AddToCartTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.item = Item.objects.create(name='Test Item', price=10.0)
        cls.url = reverse('add_to_cart', kwargs={'pk': cls.item.pk})

    def test_add_to_cart(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Перенаправлення



