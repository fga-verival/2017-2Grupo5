from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import Teacher, Student
from discipline.models import Discipline


class CreateDisciplineTestCase(APITestCase):
    """
    Unit test case to test creating new disciplines in the system.
    """

    def setUp(self):
        """
        This method will run before any test.
        """

        self.teacher = Teacher.objects.create(
            name='Professor',
            email='professor@gmail.com',
            is_teacher=True,
            password='123456'
        )

        self.student = Student.objects.create(
            name='Estudante',
            email='estudante@gmail.com',
            password='123456'
        )

        self.url = reverse('discipline:list-create')

    def tearDown(self):
        """
        This method will run after any test.
        """

        self.client.logout()
        self.teacher.delete()
        self.student.delete()

    def test_valid_create_discipline(self):
        """
        Create a new discipline by teacher in the system.
        """

        self.client.force_authenticate(self.teacher)
        self.assertEquals(Discipline.objects.count(), 0)
        data = {
            'title': "Discipline 01",
            'description': "Description 01",
            'course': "Course 01"
        }
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Discipline.objects.count(), 1)

    def test_student_create_discipline(self):
        """
        Try to create a discipline by student.
        """

        self.client.force_authenticate(self.student)
        self.assertEquals(Discipline.objects.count(), 0)
        data = {
            'title': "Discipline 01",
            'description': "Description 01",
            'course': "Course 01"
        }
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEquals(Discipline.objects.count(), 0)

    def test_not_logged_create_discipline(self):
        """
        Try to create a discipline without be logged.
        """

        self.assertEquals(Discipline.objects.count(), 0)
        data = {
            'title': "Discipline 01",
            'description': "Description 01",
            'course': "Course 01"
        }
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(Discipline.objects.count(), 0)

    def test_invalid_empty_title_create_discipline(self):
        """
        Try to create a discipline without title
        """

        self.client.force_authenticate(self.teacher)
        self.assertEquals(Discipline.objects.count(), 0)
        data = {
            'title': "",
            'description': "Description 01",
            'course': "Course 01"
        }
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(Discipline.objects.count(), 0)
        self.assertEquals(
            response.data,
            {'title': [_('This field may not be blank.')]}
        )

    def test_invalid_empty_description_create_discipline(self):
        """
        Tr to create a discipline without title
        """

        self.client.force_authenticate(self.teacher)
        self.assertEquals(Discipline.objects.count(), 0)
        data = {
            'title': "Discipline 01",
            'description': "",
            'course': "Course 01"
        }
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(Discipline.objects.count(), 0)
        self.assertEquals(
            response.data,
            {'description': [_('This field may not be blank.')]}
        )

    def test_invalid_empty_course_create_discipline(self):
        """
        Try to create a discipline without title
        """

        self.client.force_authenticate(self.teacher)
        self.assertEquals(Discipline.objects.count(), 0)
        data = {
            'title': "Discipline 01",
            'description': "Description 01",
            'course': ""
        }
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(Discipline.objects.count(), 0)
        self.assertEquals(
            response.data,
            {'course': [_('This field may not be blank.')]}
        )
