from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from products.models import ProductCategory


@receiver([post_save, post_delete], sender=ProductCategory)
def clear_categories_cache(sender, **kwargs):
    cache.delete('product_categories_list')
