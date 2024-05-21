from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('items', views.items, name='items'),
    path('about_us', views.about_us, name='about_us'),
    path('contact', views.contact, name='contact'),
    path('cart', views.cart, name='cart'), #Concatanate from user session
    path('category_<int:pk>/', views.category_items, name='category_items'),
    path('detail_<int:pk>/', views.detail, name='item_detail')
]