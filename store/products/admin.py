from django.contrib import admin
from django.utils.safestring import mark_safe

from products.models import Product, ProductCategory


# Register your models here.
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'quantity', 'category', 'post_image']
    list_filter = ['category__name']


    @admin.display(description="Image", ordering='content')
    def post_image(self, product: Product):
        if product.image:
            return mark_safe(f"<img src='{product.image.url}' width=50>")
        return "No image"