from http import HTTPStatus

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

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
        Cart.objects.create(user=self.user, product_id=1, quantity=2)
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
