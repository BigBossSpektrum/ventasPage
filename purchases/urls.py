from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('products/', views.available_products, name='available_products'),
    path('products/add/', views.add_product, name='add_product'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

]
