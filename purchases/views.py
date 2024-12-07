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
    try:
        # Obtener el carrito del usuario
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()  # Todos los elementos del carrito
        total = cart.total_price()  # Método en tu modelo Cart
    except Cart.DoesNotExist:
        # Si no hay carrito, la lista estará vacía y el total será 0
        cart_items = []
        total = 0

    # Renderizar el template con los datos del carrito
    return render(request, 'purchases/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)  # Crea el carrito si no existe

    # Verificar si el producto ya está en el carrito
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1  # Incrementar cantidad si ya existe
        cart_item.save()

    messages.success(request, f"¡'{product.name}' se ha agregado al carrito!")
    return redirect('view_cart')

@login_required
def remove_from_cart(request, item_id):
    # Obtener el carrito del usuario actual
    cart = get_object_or_404(Cart, user=request.user)

    # Obtener el artículo a eliminar del carrito
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    # Eliminar el artículo del carrito
    cart_item.delete()

    # Mensaje de confirmación
    messages.success(request, f'Se ha eliminado "{cart_item.product.name}" del carrito.')

    # Redirigir al carrito
    return redirect('view_cart')
    


# Vista para realizar la compra
@login_required
def checkout(request):
    try:
        # Obtener el carrito del usuario actual
        cart = Cart.objects.get(user=request.user)
    except ObjectDoesNotExist:
        messages.error(request, 'No tienes productos en el carrito.')
        return redirect('view_cart')

    # Verificar si el carrito tiene artículos
    if cart.items.count() == 0:
        messages.error(request, 'No tienes productos en el carrito.')
        return redirect('view_cart')

    # Enviar un correo de confirmación con los detalles del carrito
    cart_details = "\n".join(
        [f"{item.product.name} - {item.quantity} x ${item.product.price}" for item in cart.items.all()]
    )
    send_mail(
        'Nueva Compra en el Carrito',
        f"El usuario {request.user.username} ha realizado una compra.\n\nDetalles:\n{cart_details}",
        'from@example.com',
        ['admin@example.com'],  # Cambia a tu correo de administrador
        fail_silently=False,
    )

    # Vaciar el carrito después de realizar la compra
    cart.items.all().delete()

    # Mensaje de éxito
    messages.success(request, '¡Tu compra ha sido realizada con éxito!')
    return redirect('home')

@login_required
def cart_detail(request):
    cart = Cart.objects.get_or_create(user=request.user)[0]
    return render(request, 'purchases/cart_detail.html', {'cart': cart})

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

