from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import LoginUserView, register_view

app_name = 'users'

urlpatterns = [
    path("login/", LoginUserView.as_view(), name="login"),
    path("register/", register_view, name="register"),
]