from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView

from products.models import Product, Cart, ProductCategory
from products.utils import DataMixxin


# Create your views here.

class ProductHome(ListView):
    template_name = "products/index.html"
    extra_context = {'title': 'Home'}

    def get_queryset(self):
        return



class ProductsView(DataMixxin, ListView):
    template_name = "products/products.html"
    context_object_name = "products"
    extra_context = {'title': 'Products'}
    paginate_by = 6


    def get_queryset(self):
        return Product.objects.all()

@login_required
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

@login_required
def cart_remove(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ProductCategoryView(DataMixxin, ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(category_id = self.kwargs['cat_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_selected'] = self.kwargs['cat_id']
        return context