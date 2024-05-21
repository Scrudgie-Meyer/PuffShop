from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Item, OrderItem, Order
from django.db import transaction


# Create your views here.

def index(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'main/index.html', context)

def category_items(request, pk):
    category = get_object_or_404(Category, id=pk)
    attributes = get_attributes(Item.objects.filter(category=category).values_list('attributes', flat=True))

    # Отримуємо параметри фільтрації з GET запитів
    filters = {}
    for key, value in request.GET.items():
        filters[f'attributes__{key}'] = value

    if filters:
        items = Item.objects.filter(category=category).filter(**filters)
    else:
        items = Item.objects.filter(category=category)

    context = {
        'items': items,
        'attributes': attributes,
        'selected_filters': request.GET,
    }
    return render(request, 'main/category_items.html', context)


def detail(request, pk):
    items = get_object_or_404(Item, id=pk)

    context = {
        'item': items
    }
    return render(request, 'main/item_detail.html', context)


def get_attributes(attributes):
    all_attributes = {}

    for attr_dict in attributes:
        for key, value in attr_dict.items():
            if key not in all_attributes:
                all_attributes[key] = set()
            all_attributes[key].add(value)

    # Конвертуємо набори значень у списки
    for key in all_attributes:
        all_attributes[key] = list(all_attributes[key])

    return all_attributes


def item_full_list(request):
    attributes = get_attributes(Item.objects.values_list('attributes', flat=True))

    # Отримуємо параметри фільтрації з GET запитів
    filters = {}
    for key, value in request.GET.items():
        filters[f'attributes__{key}'] = value

    if filters:
        items = Item.objects.filter(**filters)
    else:
        items = Item.objects.all()

    context = {
        'items': items,
        'attributes': attributes,
        'selected_filters': request.GET,
    }
    return render(request, 'main/item_full_list.html', context)


def about_us(request):
    return render(request, 'main/about_us.html')


def contact(request):
    return render(request, 'main/contact.html')

def cart(request):
    cart = request.session.get('cart', {})
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    orders_list = request.session.get('orders', [])

    return render(request, 'main/cart.html', {'cart': cart, 'total_price': total_price, 'orders_list': orders_list})

def add_to_cart(request, pk):
    item = get_object_or_404(Item, id=pk)
    quantity = int(request.GET.get('quantity', 1))
    cart = request.session.get('cart', {})

    if str(pk) in cart:
        cart[str(pk)]['quantity'] += quantity
    else:
        cart[str(pk)] = {
            'name': item.name,
            'price': float(item.price),
            'quantity': quantity
        }

    request.session['cart'] = cart
    return redirect('cart')


def delete_from_cart(request, pk):
    item = get_object_or_404(Item, id=pk)
    quantity = int(request.GET.get('quantity', 1))
    cart = request.session.get('cart', {})

    if str(pk) in cart:
        cart[str(pk)]['quantity'] -= quantity
        if cart[str(pk)]['quantity'] <= 0:
            del cart[str(pk)]

    request.session['cart'] = cart
    return redirect('cart')

def place_order(request):
    # Отримуємо дані з форми
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    # Створюємо нове замовлення
    order = Order.objects.create(
        name=name,
        phone=phone,
        address=address,
        status='pending'
    )

    # Використовуємо транзакцію для гарантії цілісності даних
    with transaction.atomic():
        for item_id, item_data in cart.items():
            quantity = item_data['quantity']
            # Отримуємо товар
            item = get_object_or_404(Item, id=item_id)

            if item.quantity < quantity:
                # Якщо кількість товару менше ніж замовлена, відкатимо транзакцію
                raise ValueError(f"Not enough quantity for item {item.name}")

            # Віднімаємо кількість товару з інвентаря
            item.quantity -= quantity
            item.save()

            # Створюємо OrderItem для кожного товару в корзині
            order_item = OrderItem.objects.create(
                order=order,
                item=item,
                name=item.name,
                price=item.price,
                quantity=quantity,
                description=item.description
            )

    orders_list = request.session.get('orders', [])
    orders_list.append(order.id)
    request.session['orders'] = orders_list

    request.session['cart'] = {}

    return redirect('cart')

def cancel_order(request):
    cart = request.session.get('cart', {})

    if str(pk) in cart:
        cart[str(pk)]['quantity'] -= quantity
        if cart[str(pk)]['quantity'] <= 0:
            del cart[str(pk)]

    request.session['cart'] = cart
    return redirect('cart')

def order_details(request, pk):
    order = get_object_or_404(Order, id=pk)
    order_items = OrderItem.objects.filter(order=order)

    return render(request, 'main/order_details.html', {'order': order, 'order_items': order_items})