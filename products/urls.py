from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('add_product/', views.add_product, name='add_product'),
    
]