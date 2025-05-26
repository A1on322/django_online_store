from django import template

from products.models import ProductCategory

register = template.Library()

@register.inclusion_tag('products/list_cats.html')
def show_categories():
    cats = ProductCategory.objects.all()
    return {'cats': cats}