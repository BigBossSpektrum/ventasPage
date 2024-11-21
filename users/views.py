from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


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
    return redirect('home')g