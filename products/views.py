from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView
from .models import Product, Category
from .forms import ProductForm
from django.contrib.auth.decorators import login_required

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
        form = ProductForm(request.POST)
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