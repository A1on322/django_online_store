from django.db import models
from users.models import User


class CustomManager(models.QuerySet):
    def get_total_price(self):
        return sum(item.get_sum() for item in self)

    def get_quantity(self):
        return sum(item.quantity for item in self)


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
    image = models.ImageField(upload_to="products_images", null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Products"
        verbose_name = "Products"

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = CustomManager().as_manager()

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

    def get_sum(self):
        return self.quantity * self.product.price
