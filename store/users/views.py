from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy

from users.forms import LoginUserForm


# Create your views here.
class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Login'}

    def get_success_url(self):
        return reverse_lazy('home')


def register_view(request):
    return render(request, 'users/register.html')
