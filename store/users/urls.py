from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import LoginUserView, RegisterUserView

app_name = 'users'

urlpatterns = [
    path("login/", LoginUserView.as_view(), name="login"),
    path("register/", RegisterUserView.as_view(), name="register"),
]