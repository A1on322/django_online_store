from http import HTTPStatus

import stripe
from django.http import HttpResponseRedirect, HttpResponse

from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView, ListView, DetailView
from django.conf import settings
from orders.forms import OrderCreateForm
from orders.models import Order
from products.models import Cart

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_ENDPOINT_SECRET


class SuccessTemplateView(TemplateView):
    template_name = 'orders/success.html'
    extra_context = {
        'title': 'Thank you for ordering!',
    }


class CancelTemplateView(TemplateView):
    template_name = ''


class OrderListView(ListView):
    template_name = 'orders/all_orders.html'
    extra_context = {'title': 'Order List'}
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    context_object_name = 'order'
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Order #{self.object.id}'
        return context


class OrderCreateView(CreateView):
    template_name = 'orders/orders_create.html'
    form_class = OrderCreateForm
    success_url = reverse_lazy('orders:order_create')
    extra_context = {'title': 'Create new order'}

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        cart = Cart.objects.filter(user=self.request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=cart.get_stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_cancel')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def fulfill_checkout(session_id):
    # Retrieve the Checkout Session from the API with line_items expanded
    checkout_session = stripe.checkout.Session.retrieve(
        session_id,
        expand=['line_items'],
    )
    order_id = int(checkout_session.metadata['order_id'])
    order = Order.objects.get(id=order_id)
    order.update_after_payment()


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed' or event['type'] == 'checkout.session.async_payment_succeeded':
        fulfill_checkout(event['data']['object']['id'])

    return HttpResponse(status=200)
