from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User, Teacher, Student


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
        self.url = reverse('accounts:list-create')

    def tearDown(self):
        """
        This method will run after any test.
        """

        self.superuser.delete()
        self.user.delete()

    def test_valid_create_teacher_user(self):
        """
        Create a new user in the system.
        """

        self.assertEquals(User.objects.count(), 2)
        data = {
            'name': 'Fulano de Tal',
            'is_teacher': True,
            'email': 'fulano@gmail.com',
            'password': 'fulano123456',
            'confirm_password': 'fulano123456'
        }
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(User.objects.count(), 3)
        self.assertEquals(Teacher.objects.count(), 1)
        self.assertEquals(Student.objects.count(), 0)

    def test_valid_create_student_user(self):
        """
        Create a new user in the system.
        """

        self.assertEquals(User.objects.count(), 2)
        data = {
            'name': 'Fulano de Tal',
            'is_teacher': False,
            'email': 'fulano@gmail.com',
            'password': 'fulano123456',
            'confirm_password': 'fulano123456'
        }
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(User.objects.count(), 3)
        self.assertEquals(Teacher.objects.count(), 0)
        self.assertEquals(Student.objects.count(), 1)

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
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(User.objects.count(), 2)

    def test_invalid_email_create_user(self):
        """
        Can't create a new user in the system, because of invalid email.
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
            {'email': [_('This field may not be blank.')]}
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
            {'non_field_errors': [_('The passwords do not match.')]}
        )
