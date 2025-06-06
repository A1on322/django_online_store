from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm, UserCreationForm)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from users.tasks import send_password_reset_email

UserModel = get_user_model()


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label="Username or Email Address",
        widget=forms.TextInput(attrs={"class": "form-control py-4"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control py-4"}),
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "password")


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={"class": "form-control py-4", "placeholder": "Username"}
        ),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control py-4", "placeholder": "Email"}
        ),
    )
    first_name = forms.CharField(
        label="First Name",
        widget=forms.TextInput(
            attrs={"class": "form-control py-4", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(
        label="Last Name",
        widget=forms.TextInput(
            attrs={"class": "form-control py-4", "placeholder": "Last Name"}
        ),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control py-4", "placeholder": "Password"}
        ),
    )
    password2 = forms.CharField(
        label="Password (again)",
        widget=forms.PasswordInput(
            attrs={"class": "form-control py-4", "placeholder": "Confirm Password"}
        ),
    )

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )


class ProfileUserForm(forms.ModelForm):
    first_name = forms.CharField(
        label="First Name", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        label="Last Name",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    image = forms.ImageField(
        label="Image",
        widget=forms.FileInput(attrs={"class": "form-control"}),
        required=False,
    )
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control", "readonly": True}),
    )
    email = forms.EmailField(
        label="Email",
        required=False,
        widget=forms.EmailInput(attrs={"class": "form-control", "readonly": True}),
    )

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "image", "username", "email")


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control py-4", "autocomplete": "email"}
        ),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        user = get_user_model()
        if not user.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is not registered.")
        return email

    def save(
        self,
        domain_override=None,
        subject_template_name="registration/password_reset_subject.txt",
        email_template_name="registration/password_reset_email.html",
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
    ):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override

        email_field_name = UserModel.get_email_field_name()
        for user in self.get_users(email):
            user_email = getattr(user, email_field_name)
            user_pk_bytes = force_bytes(UserModel._meta.pk.value_to_string(user))
            context = {
                "email": user_email,
                "domain": domain,
                "site_name": site_name,
                "uid": urlsafe_base64_encode(user_pk_bytes),
                "username": user.username,
                "token": token_generator.make_token(user),
                "protocol": "https" if use_https else "http",
                **(extra_email_context or {}),
            }

            send_password_reset_email.delay(
                subject_template_name,
                email_template_name,
                context,
                from_email,
                user_email,
                html_email_template_name=html_email_template_name,
            )


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
