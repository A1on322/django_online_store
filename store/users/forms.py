from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django import forms



class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Username",
                               widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(attrs={'class': 'form-control py-4'}))


    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
