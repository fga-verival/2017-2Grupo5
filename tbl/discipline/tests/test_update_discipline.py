from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import Teacher, Student
from discipline.models import Discipline
from discipline.serializers import DisciplineSerializer


class UpdateDisciplineTestCase(APITestCase):
    """
    Unit test case to test a discipline's update on the system
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

    def test_valid_update_discipline(self):
        """
        Test to update the own discipline.
        """

        self.client.force_authenticate(self.teacher)
        data = DisciplineSerializer(self.discipline).data
        data.update({'title': 'Discipline 02'})
        response = self.client.put(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['title'], 'Discipline 02')

    def test_invalid_update_discipline_by_not_logged_teacher(self):
        """
        Test to update discipline by not logged user.
        """

        data = DisciplineSerializer(self.discipline).data
        data.update({'title': 'Discipline 02'})
        response = self.client.put(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_update_by_student(self):
        """
        Only teacher can update discipline
        """

        self.client.force_authenticate(self.student)
        data = DisciplineSerializer(self.discipline).data
        data.update({'description': 'Update description'})
        response = self.client.put(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_description_update_discipline(self):
        """
        Test can't update a specific discipline. Invalid description.
        """

        self.client.force_authenticate(self.teacher)
        data = DisciplineSerializer(self.discipline).data
        data.update({'description': ''})
        response = self.client.put(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data,
            {'description': [_('This field may not be blank.')]}
        )

    def test_invalid_title_update_discipline(self):
        """
        Test can't update a specific discipline. Invalid title.
        """

        self.client.force_authenticate(self.teacher)
        data = DisciplineSerializer(self.discipline).data
        data.update({'title': ''})
        response = self.client.put(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data,
            {'title': [_('This field may not be blank.')]}
        )

    def test_invalid_course_update_discipline(self):
        """
        Test can't update a specific discipline. Invalid course.
        """

        self.client.force_authenticate(self.teacher)
        data = DisciplineSerializer(self.discipline).data
        data.update({'course': ''})
        response = self.client.put(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data,
            {'course': [_('This field may not be blank.')]}
        )

    def test_invalid_update_another_discipline(self):
        """
        Can't Update another teacher discipline of system.
        """

        self.teacher2 = Teacher.objects.create(
            name='Teacher 02',
            email='teacher02@gmail.com',
            is_teacher=True,
            password='123456'
        )
        self.client.force_authenticate(self.teacher2)
        data = DisciplineSerializer(self.discipline).data
        data.update({'description': 'Update description'})
        response = self.client.put(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_discipline_not_found(self):
        """
        Test to find discipline that not exists.
        """

        url_invalid = reverse('discipline:details', kwargs={'pk': 30})
        data = DisciplineSerializer(self.discipline).data
        data.update({'title': 'Update Title'})
        response = self.client.put(url_invalid, data)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
