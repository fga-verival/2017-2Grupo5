from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import Teacher, Student
from discipline.models import Discipline
from classroom.models import ClassRoom


class DeleteClassRoomTestCase(APITestCase):
    """
    Unit test case to test delete discipline classes in the system.
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
            is_closed=False,
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

    def test_valid_delete_class(self):
        """
        Delete your own discipline classes in the system.
        """

        self.client.force_authenticate(self.teacher01)
        self.assertEquals(ClassRoom.objects.count(), 2)
        response = self.client.delete(
            self.get_url(
                self.discipline01.id,
                self.classroom01.id
            )
        )
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(ClassRoom.objects.count(), 1)

    def test_invalid_delete_not_own_discipline_classes(self):
        """
        Can't delete classes create by another teacher of system.
        """

        self.client.force_authenticate(self.teacher01)
        self.assertEquals(ClassRoom.objects.count(), 2)
        response = self.client.delete(
            self.get_url(
                self.discipline02.id,
                self.classroom02.id
            )
        )
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEquals(ClassRoom.objects.count(), 2)

    def test_invalid_delete_class_by_student(self):
        """
        Students can't delete classes.
        """

        self.client.force_authenticate(self.student)
        self.assertEquals(ClassRoom.objects.count(), 2)
        response = self.client.delete(
            self.get_url(
                self.discipline01.id,
                self.classroom01.id
            )
        )
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEquals(ClassRoom.objects.count(), 2)

    def test_invalid_delete_class_by_not_logged_user(self):
        """
        Not logged user can't delete classes.
        """

        self.assertEquals(ClassRoom.objects.count(), 2)
        response = self.client.delete(
            self.get_url(
                self.discipline01.id,
                self.classroom01.id
            )
        )
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(ClassRoom.objects.count(), 2)

    def test_not_find_class_to_delete(self):
        """
        Test to delete class that not exists for specific discipline.
        """

        self.client.force_authenticate(self.teacher01)
        self.assertEquals(ClassRoom.objects.count(), 2)
        response = self.client.delete(
            self.get_url(
                self.discipline01.id,
                self.classroom02.id
            )
        )
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(ClassRoom.objects.count(), 2)


    def get_url(self, discipline_id, class_id):
        """
        Get the specific discipline classes URL.
        """

        url = reverse(
            'classroom:details',
            kwargs={'discipline_id': discipline_id, 'class_id': class_id})

        return url

