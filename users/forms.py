from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm

class CustomUserCreationForm(UserCreationForm):
    is_buyer = forms.BooleanField(required=False, initial=True)
    is_seller = forms.BooleanField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'email', 'phone_number', 'address', 'is_buyer', 'is_seller']

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['is_buyer']:
            user.is_buyer = True
        if self.cleaned_data['is_seller']:
            user.is_seller = True
        if commit:
            user.save()
        return user
    

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('login')
