from django.contrib import admin
from .models import Product, Category

# Usar decorador @admin.register para un solo registro
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'seller', 'is_sold')
    list_filter = ('seller', 'is_sold', 'category')

# Usar el decorador también para Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


