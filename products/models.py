from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)  # Agregar stock (si lo necesitas)
    category = models.CharField(max_length=255, null=True, blank=True)  # Agregar categoría (si lo necesitas)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='products_for_sale', on_delete=models.CASCADE)
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return self.name
