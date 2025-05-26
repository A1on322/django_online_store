from django.urls import path

from products import views

urlpatterns = [
    path("", views.ProductHome.as_view(), name="home"),
    path("products/", views.ProductsView.as_view(), name="products"),


]