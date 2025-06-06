from http import HTTPStatus

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from products.models import Cart, Product, ProductCategory
from users.models import User


class UserRegistrationTestCase(TestCase):

    def setUp(self):
        self.path = reverse('users:register')
        self.test_data = {
            'first_name': 'John', 'last_name': 'Doe',
            'username': 'johndoe', 'email': 'johndoe@gmail.com',
            'password1': 'adminadmin', 'password2': 'adminadmin'
        }

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Registration')
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration_post_success(self):
        # Check whether user exist before post
        username = self.test_data['username']
        self.assertFalse(User.objects.filter(username=username).exists())

        response = self.client.post(self.path, self.test_data)

        # Check existance of User after post
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

    def test_user_registration_post_error(self):
        User.objects.create_user(self.test_data['username'])
        response = self.client.post(self.path, self.test_data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'A user with that username already exists.', html=True)


class UserProfileTestCase(TestCase):

    def setUp(self):
        self.path = reverse('users:profile')
        self.password = 'testpass123'
        self.user = User.objects.create_user('testuser', password=self.password)
        self.category = ProductCategory.objects.create(name='testcategory')
        self.product = Product.objects.create(name='testproduct', price=100, category=self.category)
        self.test_data = {
            'first_name': 'John', 'last_name': 'Doe', 'username': self.user.username,
        }

    def test_login_required(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn('/login', response.url)

    def test_user_profile_view(self):
        self.client.login(username=self.user.username, password=self.password)
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/profile.html')

        self.assertEqual(response.context_data['title'], 'Profile')
        self.assertEqual(response.context_data['default_image'], settings.DEFAULT_USER_IMAGE)

    def test_profile_context_cart(self):
        Cart.objects.create(user=self.user, product_id=self.product.pk, quantity=2)
        self.client.login(username=self.user.username, password=self.password)
        response = self.client.get(self.path)
        cart_qs = response.context_data['cart']

        self.assertTrue(cart_qs.exists())
        self.assertEqual(cart_qs.first().user, self.user)

    def test_profile_update(self):
        self.client.login(username=self.user.username, password=self.password)
        response = self.client.post(self.path, self.test_data, follow=True)
        print(response.context['form'].errors)

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertTemplateUsed(response, 'users/profile.html')


@override_settings(
    CELERY_TASK_ALWAYS_EAGER=True,
    CELERY_TASK_EAGER_PROPAGATES=True,
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'
)
class PasswordResetTestCase(TestCase):
    def setUp(self):
        self.path = reverse('users:password_reset')
        self.email = 'testemail@test.ss'
        User.objects.create_user('testuser', email=self.email, password='testtesttest')

    def _common_test_(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/password_reset_form.html')
        self.assertEqual(response.context_data['title'], 'Password reset')

    def test_user_password_reset_get(self):
        response = self.client.get(self.path)
        self._common_test_(response)

    def test_user_password_reset_post_success(self):
        response = self.client.post(self.path, {'email': self.email}, follow=True)
        self._common_test_(response)

        # Check success message
        messages = list(response.context['messages'])
        self.assertTrue(any("We’ve emailed you instructions for setting your password" in str(m) for m in messages))

        # Check email sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.email, mail.outbox[0].to)

    def test_user_password_reset_post_error(self):
        response = self.client.post(self.path, {'email': 'fakeemail@fake.ss'})
        self._common_test_(response)

        self.assertContains(response, 'This email is not registered.', html=True)


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class PasswordResetConfirmTestCase(TestCase):
    def setUp(self):
        self.email = 'testuser@test.com'
        self.password = 'testpassword'
        self.user = User.objects.create_user(
            username='testuser',
            email=self.email,
            password=self.password
        )
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)
        self.url = reverse('users:password_reset_confirm', kwargs={
            'uidb64': self.uid,
            'token': self.token,
        })

    def _common_test_(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Password reset')
        self.assertTemplateUsed(response, 'users/password_reset_confirm.html')

    def test_get_confirm_form(self):
        response = self.client.get(self.url, follow=True)
        self._common_test_(response)

    def test_password_reset_confirm_success(self):
        new_password = 'StrongPassw0rd!'

        self.client.get(self.url, follow=True)

        response = self.client.post(reverse('users:password_reset_confirm',
                                            kwargs={
                                                'uidb64': self.uid,
                                                'token': 'set-password',
                                            }),
                                    {
                                        'new_password1': new_password,
                                        'new_password2': new_password,
                                    },
                                    follow=True)

        user = User.objects.get(pk=self.user.pk)
        self.assertTrue(user.check_password(new_password))

        messages = list(response.context['messages'])
        self.assertTrue(any('You have successfully reset your password' in str(m) for m in messages))
