from django.contrib.auth.forms import AuthenticationForm
from django import forms


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Username",
                               widget=forms.TextInput())
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput())