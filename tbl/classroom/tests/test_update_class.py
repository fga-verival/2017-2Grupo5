from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import Teacher, Student
from discipline.models import Discipline
from classroom.models import ClassRoom
from classroom.serializers import ClassRoomSerializer


class UpdateClassRoomTestCase(APITestCase):
    """
    Unit test case to test update discipline classes in the system.
    """

    def setUp(self):
        """
        This method will run before any test.
        """

        self.student = Student.objects.create(
            name='Estudante',
            email='estudante@gmail.com',
            password='123456'
        )

        self.teacher01 = Teacher.objects.create(
            name='Professor 01',
            email='professor01@gmail.com',
            is_teacher=True,
            password='123456'
        )

        self.discipline01 = Discipline.objects.create(
            title='Disciplina 01',
            description='Description 01',
            course='course 01',
            teacher=self.teacher01
        )

        self.classroom01 = ClassRoom.objects.create(
            title='Turma A',
            student_limit=5,
            password='123456',
            discipline=self.discipline01,
            is_closed=False
        )

        self.teacher02 = Teacher.objects.create(
            name='Professor 02',
            email='professor02@gmail.com',
            is_teacher=True,
            password='123456'
        )

        self.discipline02 = Discipline.objects.create(
            title='Disciplina 02',
            description='Description 02',
            course='course 02',
            teacher=self.teacher02
        )

        self.classroom02 = ClassRoom.objects.create(
            title='Turma A',
            student_limit=5,
            password='123456',
            discipline=self.discipline02,
            is_closed=False
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
        self.classroom01.delete()
        self.classroom02.delete()
        self.student.delete()

    def test_valid_update_discipline_class(self):
        """
        Test to update the own discipline class.
        """

        self.client.force_authenticate(self.teacher01)
        url = self.get_url(self.discipline01.id, self.classroom01.id)
        data = ClassRoomSerializer(self.classroom01).data
        data.update({'title': 'Turma B'})
        response = self.client.put(url, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['title'], 'Turma B')

    def test_invalid_not_logged_update_discipline_class(self):
        """
        Not logged user can't update discipline classes
        """

        url = self.get_url(self.discipline01.id, self.classroom01.id)
        data = ClassRoomSerializer(self.classroom01).data
        data.update({'title': 'Turma B'})
        response = self.client.put(url, data)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_update_discipline_class_by_student(self):
        """
        Student can't update discipline classes.
        """

        self.client.force_authenticate(self.student)
        url = self.get_url(self.discipline01.id, self.classroom01.id)
        data = ClassRoomSerializer(self.classroom01).data
        data.update({'title': 'Turma B'})
        response = self.client.put(url, data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_update_another_discipline_class(self):
        """
        Can't update discipline classes by another teacher.
        """

        self.client.force_authenticate(self.teacher02)
        url = self.get_url(self.discipline01.id, self.classroom01.id)
        data = ClassRoomSerializer(self.classroom01).data
        data.update({'title': 'Turma B'})
        response = self.client.put(url, data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_discipline_class_not_found(self):
        """
        Test to edit class that not exists for specific discipline.
        """

        self.client.force_authenticate(self.teacher01)
        url = self.get_url(self.discipline01.id, self.classroom02.id)
        data = ClassRoomSerializer(self.classroom01).data
        data.update({'title': 'Turma B'})
        response = self.client.put(url, data)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_invalid_title_by_discipline_class(self):
        """
        Test can't update a specific discipline class. Invalid title.
        """

        self.client.force_authenticate(self.teacher01)
        url = self.get_url(self.discipline01.id, self.classroom01.id)
        data = ClassRoomSerializer(self.classroom01).data
        data.update({'title': ''})
        response = self.client.put(url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data,
            {'title': [_('This field may not be blank.')]}
        )

    def test_update_invalid_negative_student_limit_by_discipline_class(self):
        """
        Test can't update a specific discipline class. Invalid student limit.
        """

        self.client.force_authenticate(self.teacher01)
        url = self.get_url(self.discipline01.id, self.classroom01.id)
        data = ClassRoomSerializer(self.classroom01).data
        data.update({'student_limit': -5})
        response = self.client.put(url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data,
            {'student_limit': [_('-5 is not bigger than 0.')]}
        )

    def test_update_invalid_zero_student_limit_by_discipline_class(self):
        """
        Test can't update a specific discipline class. Invalid student limit.
        """

        self.client.force_authenticate(self.teacher01)
        url = self.get_url(self.discipline01.id, self.classroom01.id)
        data = ClassRoomSerializer(self.classroom01).data
        data.update({'student_limit': 0})
        response = self.client.put(url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data,
            {'student_limit': [_('0 is not bigger than 0.')]}
        )

    def test_valid_update_discipline_class_without_students(self):
        """
        Test can take off all students from discipline class.
        """

        self.client.force_authenticate(self.teacher01)
        url = self.get_url(self.discipline01.id, self.classroom01.id)
        data = ClassRoomSerializer(self.classroom01).data
        data.update({'students': []})
        response = self.client.put(url, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['students'], [])

    def get_url(self, discipline_id, class_id):
        """
        Get the specific discipline classes URL.
        """

        url = reverse(
            'classroom:details',
            kwargs={'discipline_id': discipline_id, 'class_id': class_id})

        return url
