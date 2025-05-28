from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms



class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Username",
                               widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(attrs={'class': 'form-control py-4'}))


    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Username",
                               widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Username'}))
    email = forms.EmailField(label="Email",
                             widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'placeholder': 'Email'}))
    first_name = forms.CharField(label="First Name",
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control py-4', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="Last Name",
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control py-4', 'placeholder': 'Last Name'}))
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control py-4', 'placeholder': 'Password'}))
    password2 = forms.CharField(label="Password (again)",
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control py-4', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
