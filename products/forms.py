from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'is_available': forms.CheckboxInput(),
        }

@property
def is_available(self):
    return self.stock > 0

class UpdateImageForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['img']