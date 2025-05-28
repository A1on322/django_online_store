from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView

from products.models import Product, Cart


# Create your views here.

class ProductHome(ListView):
    template_name = "products/index.html"
    extra_context = {'title': 'Home'}

    def get_queryset(self):
        return {'data':' Hello '}



class ProductsView(ListView):
    template_name = "products/products.html"
    context_object_name = "products"
    extra_context = {'title': 'Products'}

    def get_queryset(self):
        return Product.objects.all()

def cart_add(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.filter(user_id=request.user.id, product = product)

    if not cart.exists():
        Cart.objects.create(user_id=request.user.id, product = product, quantity=1)
    else:
        c = cart.first()
        c.quantity += 1
        c.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def cart_remove(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))