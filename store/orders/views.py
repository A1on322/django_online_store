from django.views.generic import CreateView

from orders.forms import OrderCreateForm


class OrderCreateView(CreateView):
    template_name = 'orders/orders_create.html'
    form_class = OrderCreateForm

