from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='products/images/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)  # Indica la cantidad en inventario
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='products_for_sale', on_delete=models.CASCADE)
    is_sold = models.BooleanField(default=False)  # Indica si el producto está vendido
    is_available = models.BooleanField(default=True)  # Nuevo campo para indicar disponibilidad

    def __str__(self):
        return self.name

    
    @property
    def is_available(self):
        return self.stock > 0
