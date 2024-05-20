from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:pk>/', views.category_items, name='category_items'),
]