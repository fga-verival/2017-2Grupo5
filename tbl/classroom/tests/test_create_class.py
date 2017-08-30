from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import Teacher, Student
from discipline.models import Discipline
from classroom.models import ClassRoom


class CreateClassRoomTestCase(APITestCase):
    """
    Unit test case to test creating new discipline classes in the system.
    """

    def setUp(self):
        """
        This method will run before any test.
        """

        self.teacher01 = Teacher.objects.create(
            name='Professor 01',
            email='professor01@gmail.com',
            is_teacher=True,
            password='123456'
        )

        self.teacher02 = Teacher.objects.create(
            name='Professor 02',
            email='professor02@gmail.com',
            is_teacher=True,
            password='123456'
        )

        self.discipline01 = Discipline.objects.create(
            title='Disciplina 01',
            description='Description 01',
            course='course 01',
            teacher=self.teacher01
        )

        self.discipline02 = Discipline.objects.create(
            title='Disciplina 02',
            description='Description 02',
            course='course 02',
            teacher=self.teacher02
        )

        self.student = Student.objects.create(
            name='Estudante',
            email='estudante@gmail.com',
            password='123456'
        )

    def tearDown(self):
        """
        This method will run after any test.
        """

        self.client.logout()
        self.teacher01.delete()
        self.teacher02.delete()
        self.discipline01.delete()
        self.discipline02.delete()
        self.student.delete()

    def test_valid_create_discipline_class(self):
        """
        Create a new discipline class by teacher in the system.
        """

        self.client.force_authenticate(self.teacher01)
        url = self.get_url(self.discipline01.pk)
        self.assertEquals(ClassRoom.objects.count(), 0)
        data = {
            'title': 'Turma A',
            'password': '123456',
            'student_limit': 5,
            'is_closed': False,
            'students': [self.student.id]
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(ClassRoom.objects.count(), 1)

    def test_invalid_create_discipline_class_that_not_owner(self):
        """
        Only can create class of your own discipline.
        """

        self.client.force_authenticate(self.teacher01)
        url = self.get_url(self.discipline02.pk)
        self.assertEquals(ClassRoom.objects.count(), 0)
        data = {
            'title': 'Turma A',
            'password': '123456',
            'student_limit': 5,
            'is_closed': False,
            'students': [self.student.id]
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEquals(ClassRoom.objects.count(), 0)

    def test_invalid_create_discipline_class_by_student(self):
        """
        Student can't create discipline classes.
        """

        self.client.force_authenticate(self.student)
        url = self.get_url(self.discipline01.pk)
        self.assertEquals(ClassRoom.objects.count(), 0)
        data = {
            'title': 'Turma A',
            'password': '123456',
            'student_limit': 5,
            'is_closed': False,
            'students': [self.student.id]
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEquals(ClassRoom.objects.count(), 0)

    def test_invalid_create_discipline_class_by_not_logged_user(self):
        """
        Student can't create discipline classes.
        """

        url = self.get_url(self.discipline01.pk)
        self.assertEquals(ClassRoom.objects.count(), 0)
        data = {
            'title': 'Turma A',
            'password': '123456',
            'student_limit': 5,
            'is_closed': False,
            'students': [self.student.id]
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(ClassRoom.objects.count(), 0)

    def test_invalid_title_field_to_create_class(self):
        """
        Title can't be blank.
        """

        self.client.force_authenticate(self.teacher01)
        url = self.get_url(self.discipline01.pk)
        self.assertEquals(ClassRoom.objects.count(), 0)
        data = {
            'title': '',
            'password': '123456',
            'student_limit': 5,
            'is_closed': False,
            'students': [self.student.id]
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(ClassRoom.objects.count(), 0)
        self.assertEquals(
            response.data,
            {'title': [_('This field may not be blank.')]}
        )

    def test_invalid_password_field_to_create_class(self):
        """
        Password can't be blank.
        """

        self.client.force_authenticate(self.teacher01)
        url = self.get_url(self.discipline01.pk)
        self.assertEquals(ClassRoom.objects.count(), 0)
        data = {
            'title': 'Turma A',
            'password': '',
            'student_limit': 5,
            'is_closed': False,
            'students': [self.student.id]
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(ClassRoom.objects.count(), 0)
        self.assertEquals(
            response.data,
            {'password': [_('This field may not be blank.')]}
        )

    def test_valid_empty_class_to_create_class(self):
        """
        Title can't be blank.
        """

        self.client.force_authenticate(self.teacher01)
        url = self.get_url(self.discipline01.pk)
        self.assertEquals(ClassRoom.objects.count(), 0)
        data = {
            'title': 'Turma A',
            'password': '123456',
            'student_limit': 5,
            'is_closed': False,
            'students': []
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(ClassRoom.objects.count(), 1)

    def test_invalid_zero_student_limit_to_create_class(self):
        """
        Student limit can't be negative.
        """

        self.client.force_authenticate(self.teacher01)
        url = self.get_url(self.discipline01.pk)
        self.assertEquals(ClassRoom.objects.count(), 0)
        data = {
            'title': 'Turma A',
            'password': '123456',
            'student_limit': 0,
            'is_closed': False,
            'students': [self.student.id]
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(ClassRoom.objects.count(), 0)
        self.assertEquals(
            response.data,
            {'student_limit': [_('0 is not bigger than 0.')]}
        )

    def test_invalid_negative_student_limit_to_create_class(self):
        """
        Student limit can't be negative.
        """

        self.client.force_authenticate(self.teacher01)
        url = self.get_url(self.discipline01.pk)
        self.assertEquals(ClassRoom.objects.count(), 0)
        data = {
            'title': 'Turma A',
            'password': '123456',
            'student_limit': -5,
            'is_closed': False,
            'students': [self.student.id]
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(ClassRoom.objects.count(), 0)
        self.assertEquals(
            response.data,
            {'student_limit': [_('-5 is not bigger than 0.')]}
        )

    def test_invalid_url_to_create_class(self):
        """
        Try to create a class in invalid url.
        """

        self.client.force_authenticate(self.teacher01)
        url = self.get_url(30)
        self.assertEquals(ClassRoom.objects.count(), 0)
        data = {
            'title': 'Turma A',
            'password': '123456',
            'student_limit': 5,
            'is_closed': False,
            'students': [self.student.id]
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEquals(ClassRoom.objects.count(), 0)

    def get_url(self, pk):
        """
        Get the specific discipline classes URL.
        """

        url = reverse('classroom:list-create', kwargs={'discipline_id': pk})

        return url
