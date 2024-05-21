from django.shortcuts import render, get_object_or_404, redirect
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
    items = Item.objects.filter(category=category)
    context = {
        'items': items
    }
    return render(request, 'main/category_items.html', context)

def detail(request, pk):

    item = get_object_or_404(Item, id=pk)
    max_quantity = item.quantity
    quantities = range(1, max_quantity + 1)
    context = {
        'item': item,
        'quantities': quantities
    }
    return render(request, 'main/item_detail.html', context)

def items(request):
    return render(request, 'main/items.html')

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
