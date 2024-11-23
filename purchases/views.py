from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from products.forms import ProductForm
from products.models import Product
from .models import Cart, CartItem
from django.contrib import messages

# Vista para ver el carrito
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {
        'cart': cart,
        'total_price': cart.total_price(),
    }
    return render(request, 'purchases/cart.html', context)

def add_to_cart(request, product_id):
    # Obtenemos el carrito de la sesión
    cart = request.session.get('cart', {})

    # Convertimos el ID del producto a string (las claves de la sesión deben ser strings)
    product_id_str = str(product_id)

    if product_id_str in cart:
        # Si el producto ya está en el carrito, incrementamos la cantidad
        cart[product_id_str]['quantity'] += 1
    else:
        # Si el producto no está en el carrito, lo agregamos con cantidad 1
        from products.models import Product  # Asegúrate de importar el modelo correctamente
        product = Product.objects.get(id=product_id)

        cart[product_id_str] = {
            'product_id': product.id,
            'name': product.name,
            'price': float(product.price),  # Convertir a float por seguridad
            'quantity': 1,
        }

    # Guardamos el carrito actualizado en la sesión
    request.session['cart'] = cart

    # Redirigimos a la página del carrito o donde prefieras
    return redirect('view_cart')

# Vista para realizar la compra
@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)

    # Si el carrito está vacío, mostramos un mensaje de error
    if cart.items.count() == 0:
        messages.error(request, 'No tienes productos en el carrito.')
        return redirect('view_cart')

    # Enviar un correo de confirmación (simulado)
    send_mail(
        'Nueva Compra en el Carrito',
        f"El usuario {request.user.username} ha agregado productos al carrito.\n\nDetalles:\n" +
        "\n".join([f"{item.product.name} - {item.quantity} x ${item.product.price}" for item in cart.items.all()]),
        'from@example.com',
        ['admin@example.com'],
        fail_silently=False,
    )

    # Aquí podrías agregar la lógica de pago, realizar la compra, etc.
    messages.success(request, '¡Tu compra ha sido realizada con éxito!')
    return redirect('home')

@login_required
def cart_detail(request):
    cart = Cart.objects.get_or_create(user=request.user)[0]
    return render(request, 'purchases/cart_detail.html', {'cart': cart})

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        if cart[product_id_str]['quantity'] > 1:
            # Reduce la cantidad
            cart[product_id_str]['quantity'] -= 1
        else:
            # Elimina el producto si la cantidad llega a 0
            del cart[product_id_str]
        request.session['cart'] = cart  # Actualiza el carrito en la sesión
    
    return redirect('view_cart')

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

