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
    items = Item.objects.filter(category=category)
    context = {
        'items': items
    }
    return render(request, 'main/category_items.html', context)

def detail(request, pk):

    items = get_object_or_404(Item, id=pk)

    context = {
        'item': items
    }
    return render(request, 'main/item_detail.html', context)

def cart(request):
    return render(request, 'main/cart.html')

def about_us(request):
    return render(request, 'main/about_us.html')

def contact(request):
    return render(request, 'main/contact.html')