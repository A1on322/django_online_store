from django.urls import path

from products import views
from products.views import cart_add, cart_remove

app_name = 'products'

urlpatterns = [
    path("", views.ProductsView.as_view(), name="index"),
    path('cart/add/<int:product_id>/', cart_add, name='cart_add' ),
    path('cart/remove/<int:cart_id>/', cart_remove, name='cart_remove'),


]