from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView, PasswordResetConfirmView,
                                       PasswordResetView)
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from products.models import Cart
from users.forms import (CustomPasswordResetForm, CustomSetPasswordForm,
                         LoginUserForm, ProfileUserForm, RegisterUserForm)


# Create your views here.
class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = "users/login.html"
    extra_context = {"title": "Login"}

    def get_success_url(self):
        return reverse_lazy("home")


class RegisterUserView(SuccessMessageMixin, CreateView):
    form_class = RegisterUserForm
    template_name = "users/register.html"
    extra_context = {"title": "Registration"}
    success_url = reverse_lazy("users:login")
    success_message = "You have successfully registered! Please log in."


class ProfileUserView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = "users/profile.html"

    def get_success_url(self):
        return reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"] = Cart.objects.filter(user=self.request.user)
        context["title"] = "Profile"
        context["default_image"] = settings.DEFAULT_USER_IMAGE
        return context


class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = "users/password_reset_form.html"
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset")
    success_message = (
        "We’ve emailed you instructions for setting your password, if an account exists with the email "
        "you entered.\nYou should receive them shortly."
    )
    form_class = CustomPasswordResetForm


class CustomPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:login")
    success_message = "You have successfully reset your password!\nPlease log in."
    form_class = CustomSetPasswordForm
