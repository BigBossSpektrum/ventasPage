from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('sell_product/', views.sell_product, name='sell_product'),
]