from django.shortcuts import render, get_object_or_404
from .models import Category, Item
# Create your views here.

def index(request):
    categories = Category.objects.all()

    data = {
        'categories': categories,
    }

    return render(request, 'main/index.html', data)

def category_items(request, pk):
    category = get_object_or_404(Category, id=pk)
    items = Item.objects.filter(category=category)
    context = {
        'category': category,
        'items': items
    }
    return render(request, 'main/category_items.html', context)