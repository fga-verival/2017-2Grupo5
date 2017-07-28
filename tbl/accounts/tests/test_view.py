from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User


class RegisterTestCase(APITestCase):
    """
    Unit test case to test user registration in the system.
    """

    def test_register_ok(self):
        """
        Test the status code of register url
        """

        register_url = reverse('accounts:register')
        response = self.client.get(register_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_account(self):
        """
        Ensure we can create a new account object
        """

        data = {
            'name': 'Pedro Calile',
            'email': 'pedro@gmail.com',
            'password': '12345',
            'password_confirmation': '12345'
        }
        register_url = reverse('accounts:register')
        response = self.client.post(register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, 'Pedro Calile')
        self.assertEqual(User.objects.get().email, 'pedro@gmail.com')
