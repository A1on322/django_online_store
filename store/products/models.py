from django.db import models

# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Product Categories"
        verbose_name = "Product Category"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Products"
        verbose_name = "Products"

    def __str__(self):
        return self.name

