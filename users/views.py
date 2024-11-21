from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import get_backends
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


def login_redirect(request):
    if request.user.is_authenticated:
        if request.user.is_buyer:
            return redirect('buyer_dashboard')  # Redirigir a la página de comprador
        elif request.user.is_seller:
            return redirect('seller_dashboard')  # Redirigir a la página de vendedor
    return redirect('home')

@login_required
def buyer_dashboard(request):
    return render(request, 'users/buyer_dashboard.html')

@login_required
def seller_dashboard(request):
    return render(request, 'users/seller_dashboard.html')

@login_required
def profile_redirect(request):
    if request.user.is_buyer:
        return redirect('buyer_dashboard')  # Redirige al comprador
    elif request.user.is_seller:
        return redirect('seller_dashboard')  # Redirige al vendedor
    return redirect('home')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Obtener el primer backend configurado
            backend = get_backends()[0]
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            messages.success(request, '¡Usuario creado exitosamente!')
            return redirect('home')
        else:
            messages.error(request, 'Hubo un error al crear el usuario. Verifica los datos ingresados.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  # Pasamos el usuario autenticado a la plantilla
        return context