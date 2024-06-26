from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about_us', views.about_us, name='about_us'),
    path('contact', views.contact, name='contact'),
    path('cart', views.cart, name='cart'),
    path('add_<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('delete_<int:pk>/', views.delete_from_cart, name='delete_from_cart'),
    path('place_order', views.place_order, name='place_order'),
    path('detail_<int:pk>/', views.detail, name='item_detail'),
    path('product/', views.item_list, name='item_list'),
    path('order_<int:pk>/', views.order_details, name='order_details')
]