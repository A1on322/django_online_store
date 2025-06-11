from django import template
from django.core.cache import cache

from products.models import ProductCategory

register = template.Library()


@register.inclusion_tag("products/list_cats.html", takes_context=True)
def show_categories(context):
    cats = cache.get('category_list')
    if cats is None:
        cats = ProductCategory.objects.all()
        cache.set('category_list', cats, 60*10)

    return {
        "cats": cats,
        "cat_selected": context.get("cat_selected", None),
    }
