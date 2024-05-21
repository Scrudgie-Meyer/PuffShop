rom django.shortcuts import render, get_object_or_404
from .models import Category, Item


# Create your views here.

def index(request):
	@@ -11,28 +13,82 @@ def index(request):

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


def cart(request):
    return render(request, 'main/cart.html')


def about_us(request):
    return render(request, 'main/about_us.html')


def contact(request):
    return render(request, 'main/contact.html')
