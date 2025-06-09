from django.urls import reverse_lazy
from django.views.generic import CreateView

from orders.forms import OrderCreateForm


class OrderCreateView(CreateView):
    template_name = 'orders/orders_create.html'
    form_class = OrderCreateForm
    success_url = reverse_lazy('orders:order_create')
    extra_context = {'title': 'Create new order'}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
