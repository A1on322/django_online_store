from django.shortcuts import render
from django.views.generic import ListView

from products.models import Product


# Create your views here.

class ProductHome(ListView):
    template_name = "products/index.html"
    title = "Home"

    def get_queryset(self):
        return {'data':' Hello '}



class ProductsView(ListView):
    template_name = "products/products.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.all()