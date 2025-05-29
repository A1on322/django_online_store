from unicodedata import category

from django.urls import path

from products.views import cart_add, cart_remove, ProductsView

app_name = 'products'

urlpatterns = [
    path("", ProductsView.as_view(), name="index"),
    path('cart/add/<int:product_id>/', cart_add, name='cart_add' ),
    path('cart/remove/<int:cart_id>/', cart_remove, name='cart_remove'),
    path('category/<int:cat_id>/', ProductsView.as_view(), name='category')


]