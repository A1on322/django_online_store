from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django import forms



class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email Address",
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


class ProfileUserForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name",
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Last Name", required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(label="Image",
                             widget=forms.FileInput(attrs={'class': 'form-control'}),
                             required=False)
    username = forms.CharField(label="Username",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))
    email = forms.EmailField(label="Email", required=False,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': True}))

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'image', 'username', 'email')


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email",
                             widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'autocomplete': 'email'})
                             )


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )