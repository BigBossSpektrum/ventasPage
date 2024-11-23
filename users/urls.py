from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path
from django.contrib.auth.views import LoginView
from .views import ProfileView
from django.contrib.auth.views import LogoutView
from django.contrib.messages.views import SuccessMessageMixin


class CustomLogoutView(SuccessMessageMixin, LogoutView):
    success_message = "Has cerrado sesión correctamente."

    
urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('signup/', views.signup_view, name='signup'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    
]

    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),