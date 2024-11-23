from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from products.forms import ProductForm
from products.models import Product
from .models import Cart, CartItem

# Agregar un producto al carrito
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Verificar si el producto ya está en el carrito del usuario
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:  # Si ya existe, incrementar la cantidad
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')  # Redirigir al detalle del carrito

@login_required
def cart_detail(request):
    cart = Cart.objects.get_or_create(user=request.user)[0]
    return render(request, 'purchases/cart_detail.html', {'cart': cart})

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart_detail')

# Listar productos disponibles
def available_products(request):
    products = Product.objects.all()
    return render(request, 'purchases/buy.html', {'products': products})

def is_seller(user):
    return user.is_authenticated and user.is_seller

@user_passes_test(is_seller)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user  # Asignar el producto al vendedor
            product.save()
            return redirect('available_products')
    else:
        form = ProductForm()

    return render(request, 'products/add_product.html', {'form': form})

