from products.models import Cart

def cart(request):
    user = request.user
    return {'cart': Cart.objects.filter(user=user) if user.is_authenticated else []}
