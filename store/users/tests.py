from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

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
