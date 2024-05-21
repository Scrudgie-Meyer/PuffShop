from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('items', views.items, name='items'),
    path('about_us', views.about_us, name='about_us'),
    path('contact', views.contact, name='contact'),
    path('cart', views.cart, name='cart'),
    path('add_<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('delete_<int:pk>/', views.delete_from_cart, name='delete_from_cart'),
    path('category_<int:pk>/', views.category_items, name='category_items'),
    path('detail_<int:pk>/', views.detail, name='item_detail')
]