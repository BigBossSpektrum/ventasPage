from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Cart, CartItem

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart = Cart.objects.get(user=request.user)
    return render(request, 'purchases/cart_detail.html', {'cart': cart})

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart_detail')