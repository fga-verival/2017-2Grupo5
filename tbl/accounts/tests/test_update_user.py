from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from accounts.serializers import UserSerializer


class UpdateUserTestCase(APITestCase):
    """
    Unit test case to test a user's update on the system
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
        self.client.force_authenticate(self.user)
        self.url = reverse('accounts:details', kwargs={'pk': self.user.pk})
        self.url_invalid = reverse('accounts:details', kwargs={'pk': 30})

    def tearDown(self):
        """
        This method will run after any test.
        """

        self.superuser.delete()
        self.client.logout()
        self.user.delete()

    def test_valid_update_user(self):
        """
        Test to update the own user.
        """

        data = UserSerializer(self.user).data
        data.update({'name': 'Pedro Callile'})
        response = self.client.put(path=self.url, data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_user(self):
        """
        Test to can't update a specific user. Invalid email.
        """

        data = UserSerializer(self.user).data
        data.update({'email': 'fulano'})
        response = self.client.put(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data,
            {'email': ['Enter a valid email address.']}
        )

    def test_invalid_update_another_user(self):
        """
        Can't Update another user of system.
        """

        url = reverse('accounts:details', kwargs={'pk': self.superuser.pk})
        data = UserSerializer(self.superuser).data
        data.update({'email': 'fulano@gmail.com'})
        response = self.client.put(url, data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_not_found(self):
        """
        Test to find user that not exists.
        """

        data = UserSerializer(self.user).data
        data.update({'email': 'fulano@gmail.com'})
        response = self.client.put(self.url_invalid, data)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
