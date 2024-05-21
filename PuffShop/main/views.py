from django.shortcuts import render, get_object_or_404
from .models import Category, Item


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
    return render(request, 'main/cart.html', {'cart': cart, 'total_price': total_price})

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
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    cart = request.session.get('cart', {})



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