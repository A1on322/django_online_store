from django.contrib.auth.views import LoginView
from django.shortcuts import render

from users.forms import LoginUserForm


# Create your views here.
class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'

def register_view(request):
    return render(request, 'users/register.html')
