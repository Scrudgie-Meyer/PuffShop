from django.test import TestCase
from django.urls import reverse
from .models import Category, Item, Order


class IndexViewTest(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')

    def test_popular_categories(self):
        Category.objects.create(name='Test Category', image_url='test.jpg')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Category')

    def test_popular_categories_show_up_in_a_list(self):
        for i in range(10):
            Category.objects.create(name=f'Test Category {i}', image_url=f'test{i}.jpg')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['categories']) == 10)


class ItemDetailViewTest(TestCase):

    def test_item_description(self):
        item = Item.objects.create(name='Test Item', price=10.0, description='Test Description')
        response = self.client.get(reverse('item_detail', kwargs={'pk': item.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Description')

    def test_item_price(self):
        item = Item.objects.create(name='Test Item', price=10.0)
        response = self.client.get(reverse('item_detail', kwargs={'pk': item.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '10.0')

    def test_item_add_to_cart(self):
        item = Item.objects.create(name='Test Item', price=10.0)
        response = self.client.get(reverse('item_detail', kwargs={'pk': item.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add to Cart')


    def test_item_add_to_cart_redirect(self):
        item = Item.objects.create(name='Test Item', price=10.0)
        response = self.client.get(reverse('add_to_cart', kwargs={'pk': item.pk}))
        self.assertEqual(response.status_code, 302)

    def test_item_quantity_changes(self):
        item = Item.objects.create(name='Test Item', price=10.0, quantity=10)
        response = self.client.get(reverse('add_to_cart', kwargs={'pk': item.pk}))
        self.assertEqual(response.status_code, 302)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 10)

    def test_item_add_to_card_with_quantity(self):
        item = Item.objects.create(name='Test Item', price=10.0, quantity=10)
        response = self.client.get(reverse('add_to_cart', kwargs={'pk': item.pk}))
        self.assertEqual(response.status_code, 302)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 10)


class OrderAddTest(TestCase):

    def test_order_add(self):
        response = self.client.get(reverse('place_order'))
        self.assertEqual(response.status_code, 302)

    def test_item_add(self):
        item = Item.objects.create(name='Test Item', price=10.0)
        response = self.client.get(reverse('add_to_cart', kwargs={'pk': item.pk}))
        self.assertEqual(response.status_code, 302)

    def test_order_add_with_quantity(self):
        item = Item.objects.create(name='Test Item', price=10.0, quantity=1)
        # add item
        response = self.client.get(reverse('add_to_cart', kwargs={'pk': item.pk}))
        self.assertEqual(response.status_code, 302)
        # place order
        response = self.client.post(reverse('place_order'), {'name': 'Test Name', 'phone': '1234567890', 'address': 'Test Address'})
        self.assertEqual(response.status_code, 302)
        # check order
        order = Order.objects.first()
        self.assertEqual(order.order_items.count(), 1)


    def test_order_with_quantity_from_detailed_view(self):
        item = Item.objects.create(name='Test Item', price=10.0, quantity=10)
        response = self.client.get(reverse('item_detail', kwargs={'pk': item.pk}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('add_to_cart', kwargs={'pk': item.pk}), {'quantity': 5})
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('place_order'), {'name': 'Test Name', 'phone': '1234567890', 'address': 'Test Address'})
        self.assertEqual(response.status_code, 302)
        order = Order.objects.first()
        self.assertEqual(order.order_items.count(), 1)
        order_item = order.order_items.first()
        self.assertEqual(order_item.quantity, 5)


    def test_delete_order_from_cart(self):
        item = Item.objects.create(name='Test Item', price=10.0, quantity=10)
        response = self.client.get(reverse('add_to_cart', kwargs={'pk': item.pk}))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('delete_from_cart', kwargs={'pk': item.pk}))
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('place_order'), {'name': 'Test Name', 'phone': '1234567890', 'address': 'Test Address'})
        self.assertEqual(response.status_code, 302)
        order = Order.objects.first()
        self.assertIsNone(order)


    def test_delete_order_from_cart_with_quantity(self):   
        item = Item.objects.create(name='Test Item', price=10.0, quantity=10)
        response = self.client.get(reverse('add_to_cart', kwargs={'pk': item.pk}))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('delete_from_cart', kwargs={'pk': item.pk}), {'quantity': 5})
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('place_order'), {'name': 'Test Name', 'phone': '1234567890', 'address': 'Test Address'})
        self.assertEqual(response.status_code, 302)
        order = Order.objects.first()
        self.assertIsNone(order)


class AddToCartTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.item = Item.objects.create(name='Test Item', price=10.0)
        cls.url = reverse('add_to_cart', kwargs={'pk': cls.item.pk})

    def test_add_to_cart(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class DeleteFromCartTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.item = Item.objects.create(name='Test Item', price=10.0)
        cls.url = reverse('delete_from_cart', kwargs={'pk': cls.item.pk})

    def test_delete_from_cart(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

class CatalogFilter(TestCase):
    def test_catalog_filter(self):
        category = Category.objects.create(name='Test Category', image_url='test.jpg')
        item = Item.objects.create(name='Test Item', price=10.0, category=category)
        response = self.client.get(reverse('item_list'), {'category': category.pk})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Item')
        self.assertContains(response, 'Test Category')
        self.assertContains(response, '10.0')
        self.assertContains(response, 'Add to Cart')

    def test_catalog_filter_no_items(self):
        category = Category.objects.create(name='Test Category', image_url='test.jpg')
        response = self.client.get(reverse('item_list'), {'category': category.pk})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Test Item')
        self.assertNotContains(response, '10.0')
        self.assertNotContains(response, 'Add to Cart')

    def test_catalog_filer_by_min_price(self):
        category = Category.objects.create(name='Test Category', image_url='test.jpg')
        item = Item.objects.create(name='Test Item', price=10.0, category=category)
        response = self.client.get(reverse('item_list'), {'min_price': 5})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Item')
        self.assertContains(response, 'Test Category')
        self.assertContains(response, '10.0')
        self.assertContains(response, 'Add to Cart')

    def test_catalog_filter_by_max_price(self):
        category = Category.objects.create(name='Test Category', image_url='test.jpg')
        item = Item.objects.create(name='Test Item', price=10.0, category=category)
        response = self.client.get(reverse('item_list'), {'max_price': 15})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Item')
        self.assertContains(response, 'Test Category')
        self.assertContains(response, '10.0')
        self.assertContains(response, 'Add to Cart')

    def test_catalog_filter_by_min_and_max_price(self):
        category = Category.objects.create(name='Test Category', image_url='test.jpg')
        item = Item.objects.create(name='Test Item', price=10.0, category=category)
        response = self.client.get(reverse('item_list'), {'min_price': 5, 'max_price': 15})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Item')
        self.assertContains(response, 'Test Category')
        self.assertContains(response, '10.0')
        self.assertContains(response, 'Add to Cart')


    def test_catalog_filter_by_material(self):
        category = Category.objects.create(name='Test Category', image_url='test.jpg')
        item = Item.objects.create(name='Test Item', price=10.0, category=category, attributes={'material': 'wood'})
        response = self.client.get(reverse('item_list'), {'material': 'wood'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Item')
        self.assertContains(response, 'Test Category')
        self.assertContains(response, '10.0')
        self.assertContains(response, 'Add to Cart')

    def test_catalog_filter_by_material_no_items(self):
        category = Category.objects.create(name='Test Category', image_url='test.jpg')
        item = Item.objects.create(name='Test Item', price=10.0, category=category, attributes={'material': 'wood'})
        response = self.client.get(reverse('item_list'), {'material': 'metal'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Test Item')
        self.assertNotContains(response, '10.0')
        self.assertNotContains(response, 'Add to Cart')

    def test_catalog_filter_by_color(self):
        category = Category.objects.create(name='Test Category', image_url='test.jpg')
        item = Item.objects.create(name='Test Item', price=10.0, category=category, attributes={'color': 'red'})
        response = self.client.get(reverse('item_list'), {'color': 'red'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Item')
        self.assertContains(response, 'Test Category')
        self.assertContains(response, '10.0')
        self.assertContains(response, 'Add to Cart')

    def test_catalog_filter_by_color_no_items(self):
        category = Category.objects.create(name='Test Category', image_url='test.jpg')
        item = Item.objects.create(name='Test Item', price=10.0, category=category, attributes={'color': 'red'})
        response = self.client.get(reverse('item_list'), {'color': 'blue'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Test Item')
        self.assertNotContains(response, '10.0')
        self.assertNotContains(response, 'Add to Cart')


    def test_catalog_filter_by_size(self):
        category = Category.objects.create(name='Test Category', image_url='test.jpg')
        item = Item.objects.create(name='Test Item', price=10.0, category=category, attributes={'size': 'large'})
        response = self.client.get(reverse('item_list'), {'size': 'large'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Item')
        self.assertContains(response, 'Test Category')
        self.assertContains(response, '10.0')
        self.assertContains(response, 'Add to Cart')

    def test_catalog_filter_by_size_no_items(self):
        category = Category.objects.create(name='Test Category', image_url='test.jpg')
        item = Item.objects.create(name='Test Item', price=10.0, category=category, attributes={'size': 'large'})
        response = self.client.get(reverse('item_list'), {'size': 'small'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Test Item')
        self.assertNotContains(response, '10.0')
        self.assertNotContains(response, 'Add to Cart')

    def test_catalog_filter_by_category_and_material(self):
        category = Category.objects.create(name='Test Category', image_url='test.jpg')
        item = Item.objects.create(name='Test Item', price=10.0, category=category, attributes={'material': 'wood'})
        response = self.client.get(reverse('item_list'), {'category': category.pk, 'material': 'wood'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Item')
        self.assertContains(response, 'Test Category')
        self.assertContains(response, '10.0')
        self.assertContains(response, 'Add to Cart')

    def test_catalog_filter_by_category_and_material_no_items(self):
        category = Category.objects.create(name='Test Category', image_url='test.jpg')
        item = Item.objects.create(name='Test Item', price=10.0, category=category, attributes={'material': 'wood'})
        response = self.client.get(reverse('item_list'), {'category': category.pk, 'material': 'metal'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Test Item')
        self.assertNotContains(response, '10.0')
        self.assertNotContains(response, 'Add to Cart')



