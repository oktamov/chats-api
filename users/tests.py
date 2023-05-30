from django.test import TestCase
from django.urls import reverse

from users.models import User


# Create your tests here.


class UserTest(TestCase):
    def test_register(self):
        user_data = {
            "email": "aa@gmail.com",
            "username": "test_user",
            "password": "test_password"
        }

        url = reverse('register')

        response = self.client.post(url, user_data)

        self.assertEquals(response.status_code, 201)

    def test_login(self):
        User.objects.create_user(email="aa@mail.com", username='test_user', password='test_password')
        login_data = {
            "username_or_email": "test_user",
            "password": "test_password"
        }

        url = reverse('login')

        response = self.client.post(url, data=login_data)

        self.assertEquals(response.status_code, 201)

    def test_user_login(self):
        user = User.objects.create_user(
            username='testuser1',
            password='123456'
        )

        data = {
            "username_or_email": "testuser1",
            "password": "123456"
        }

        url = reverse('login')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
