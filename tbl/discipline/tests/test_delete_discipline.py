from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import Teacher, Student
from discipline.models import Discipline


class DeleteUserTestCase(APITestCase):
    """
    Unit test responsible for the removal of system users.
    """

    def setUp(self):
        """
        This method will run before any test.
        """

        self.teacher = Teacher.objects.create(
            name='Teacher 01',
            email='teacher@gmail.com',
            is_teacher=True,
            password='123456'
        )
        self.discipline = Discipline.objects.create(
            title="Discipline 01",
            description="Description 01",
            course="Course 01",
            teacher=self.teacher
        )
        self.student = Student.objects.create(
            name='Student 01',
            email='student@gmail.com',
            password='123456'
        )
        self.url = reverse(
            'discipline:details',
            kwargs={'pk': self.discipline.pk}
        )

    def tearDown(self):
        """
        This method will run after any test.
        """

        self.client.logout()
        self.teacher.delete()
        self.student.delete()
        self.discipline.delete()

    def test_valid_delete_discipline(self):
        """
        Delete your own discipline in the system.
        """

        self.client.force_authenticate(self.teacher)
        self.assertEquals(Discipline.objects.count(), 1)
        response = self.client.delete(self.url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Discipline.objects.count(), 0)

    def test_invalid_delete_another_discipline(self):
        """
        Can't Delete discipline by another teacher of system.
        """

        self.teacher2 = Teacher.objects.create(
            name='Teacher 02',
            email='teacher02@gmail.com',
            is_teacher=True,
            password='123456'
        )
        self.discipline2 = Discipline.objects.create(
            title="Discipline 02",
            description="Description 02",
            course="Course 02",
            teacher=self.teacher2
        )
        self.client.force_authenticate(self.teacher)
        url = reverse('discipline:details', kwargs={'pk': self.discipline2.pk})
        self.assertEquals(Discipline.objects.count(), 2)
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEquals(Discipline.objects.count(), 2)

    def test_invalid_student_delete_discipline(self):
        """
        Student Can't Delete discipline of system.
        """

        self.client.force_authenticate(self.student)
        self.assertEquals(Discipline.objects.count(), 1)
        response = self.client.delete(self.url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEquals(Discipline.objects.count(), 1)

    def test_invalid_delete_discipline_by_not_logged_user(self):
        """
        Not logged user can't delete disciplines.
        """

        self.assertEquals(Discipline.objects.count(), 1)
        response = self.client.delete(self.url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(Discipline.objects.count(), 1)


    def test_not_find_discipline_to_delete(self):
        """
        Can't find discipline to delete, invalid url.
        """

        self.client.force_authenticate(self.teacher)
        url_invalid = reverse('discipline:details', kwargs={'pk': 30})
        self.assertEquals(Discipline.objects.count(), 1)
        response = self.client.delete(url_invalid)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(Discipline.objects.count(), 1)
