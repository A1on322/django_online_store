from django.db import models

from users.models import User


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUS = (
        (CREATED, 'Created'),
        (PAID, 'Paid'),
        (ON_WAY, 'On Way'),
        (DELIVERED, 'Delivered'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    cart = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.SmallIntegerField(choices=STATUS, default=CREATED)

    def __str__(self):
        return f'Order #{self.id}: {self.first_name} {self.last_name}'


