from django.contrib import admin

from orders.models import Order


# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status')
    fields = (
        'id',
        ('first_name', 'last_name'),
        ('email', 'address'),
        'cart',
        'created_at',
        'status',
        'user'
    )
    readonly_fields = ('id', 'created_at')
