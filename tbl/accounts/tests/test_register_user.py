from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User


class CreateUserTestCase(APITestCase):
    """
    Unit test case to test creating new users in the system.
    """

    def setUp(self):
        """
        This method will run before any test.
        """

        self.superuser = User.objects.create_superuser(
            name='Victor Arnaud',
            email='victorhad@gmail.com',
            password='victorhad123456'
        )
        self.user = User.objects.create(
            name='Pedro Calile',
            email='pedro@gmail.com',
            password='pedro123456'
        )
        self.url = reverse('accounts:register')

    def tearDown(self):
        """
        This method will run after any test.
        """

        self.superuser.delete()
        self.user.delete()

    def test_valid_create_user(self):
        """
        Create a new user in the system.
        """

        self.assertEquals(User.objects.count(), 2)
        data = {
            'name': 'Fulano de Tal',
            'email': 'fulano@gmail.com',
            'password': 'fulano123456',
            'confirm_password': 'fulano123456'
        }
        response = self.client.post(path=self.url, data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(User.objects.count(), 3)

    def test_invalid_same_email_created_user(self):
        """
        Can't create a user with same email address.
        """

        self.assertEquals(User.objects.count(), 2)
        data = {
            'name': 'Fulano de Tal',
            'email': 'victorhad@gmail.com',
            'password': 'fulano123456',
            'confirm_password': 'fulano123456'
        }
        response = self.client.post(path=self.url, data=data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(User.objects.count(), 2)
        self.assertEquals(
            response.data,
            {'email': ['User with this E-mail already exists.']}
        )

    def test_invalid_email_create_user(self):
        """
        Can't create a new user in the system, bacause of invalid email.
        """

        self.assertEquals(User.objects.count(), 2)
        data = {
            'name': 'Maria de Fatima',
            'email': '',
            'password': 'maria123456',
            'confirm_password': 'maria123456'
        }
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(User.objects.count(), 2)
        self.assertEquals(
            response.data,
            {'email': ['This field may not be blank.']}
        )

    def test_invalid_password_create_user(self):
        """
        Can't create a new user in the system, because of invalid password.
        """

        self.assertEquals(User.objects.count(), 2)
        data = {
            'name': 'Maria de Fatima',
            'email': 'maria@gmail.com',
            'password': 'maria123456',
            'confirm_password': 'maria12345'
        }
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(User.objects.count(), 2)
        self.assertEquals(
            response.data,
            {'non_field_errors': ['The passwords do not match.']}
        )
