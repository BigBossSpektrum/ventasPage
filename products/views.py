from asyncio.log import logger
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView

from purchases.models import Cart, CartItem
from .models import Product, Category
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Vista para listar productos con filtrado por categoría usando ListView
class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()  # Obtén todas las categorías
        context['categories'] = categories  # Pasa las categorías al template
        return context

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.GET.get('category')  # Obtener el filtro de categoría desde el GET
        if category_id:
            queryset = queryset.filter(category__id=category_id)  # Filtrar por ID de categoría
        return queryset

@login_required
def sell_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user  # Asociar el producto con el vendedor (usuario logueado)
            product.save()
            return redirect('product_list')  # Redirigir a la lista de productos después de guardar el producto
    else:
        form = ProductForm()

    return render(request, 'products/sell_product.html', {'form': form})

@login_required
def sell_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # Guardar el nuevo producto en la base de datos
            product = form.save(commit=False)
            product.seller = request.user  # Asocia el producto al usuario autenticado
            product.save()

            # Mensaje de éxito
            messages.success(request, '¡Producto vendido con éxito!')
            return redirect('home')  # Redirige a la página principal o a donde quieras

        else:
            messages.error(request, 'Hubo un error al registrar el producto. Por favor, verifica los datos.')

    else:
        form = ProductForm()

    return render(request, 'sell_product.html', {'form': form})

@login_required
def remove_from_cart(request, id):
    logger.info(f"Intentando eliminar el producto con ID: {id}")
    try:
        # Obtener el carrito del usuario
        cart = Cart.objects.get(user=request.user)

        # Verificar si el producto existe en el carrito
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=id)

        if cart_item.quantity > 1:
            # Reducir la cantidad si es mayor a 1
            cart_item.quantity -= 1
            cart_item.save()
        else:
            # Si la cantidad es 1, eliminar el producto completamente del carrito
            cart_item.delete()

        # Mensaje de confirmación
        messages.success(request, "El producto se eliminó correctamente del carrito.")

    except Cart.DoesNotExist:
        messages.error(request, "No tienes un carrito activo.")
    except CartItem.DoesNotExist:
        messages.error(request, "El producto no está en tu carrito.")

    return redirect('view_cart')

@login_required
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})