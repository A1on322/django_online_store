from django.shortcuts import render
from django.views.generic import ListView


# Create your views here.

class ProductHome(ListView):
    template_name = "products/index.html"
    context_object_name = "products"
    title_page = "Home"

    def get_queryset(self):
        return {'data':' Hello '}

def products(request):
    return render(request, 'products/products.html')