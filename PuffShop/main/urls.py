from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category_<int:pk>/', views.category_items, name='category_items'),
    path('detail_<int:pk>/', views.detail, name='item_detail')
]