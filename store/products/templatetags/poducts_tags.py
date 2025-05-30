from django import template
from products.models import ProductCategory

register = template.Library()


@register.inclusion_tag("products/list_cats.html", takes_context=True)
def show_categories(context):
    cats = ProductCategory.objects.all()
    return {
        "cats": cats,
        "cat_selected": context.get("cat_selected", None),
    }
