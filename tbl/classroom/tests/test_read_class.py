from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import Teacher, Student
from discipline.models import Discipline
from classroom.models import ClassRoom
from classroom.serializers import ClassRoomRegisterSerializer, ClassRoomSerializer


class ReadClassRoomTestCase(APITestCase):
    """
    Unit test case to test read discipline classes in the system.
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

    def test_valid_not_logged_discipline_class_list(self):
        """
        Test found the discipline classes list by not logged user.
        """

        classes = ClassRoom.objects.filter(
            discipline=self.discipline01.id
        )
        serializer = ClassRoomRegisterSerializer(classes, many=True)
        url = reverse(
            'classroom:list-create',
            kwargs={'discipline_id': self.discipline01.id}
        )
        response = self.client.get(url)
        self.assertEquals(classes.count(), 1)
        self.assertEquals(response.data, serializer.data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_valid_student_discipline_class_list(self):
        """
        Test found the discipline classes list by logged user.
        """

        classes = ClassRoom.objects.filter(
            discipline=self.discipline01.id
        )
        serializer = ClassRoomRegisterSerializer(classes, many=True)
        url = reverse(
            'classroom:list-create',
            kwargs={'discipline_id': self.discipline01.id}
        )
        response = self.client.get(url)
        self.assertEquals(classes.count(), 1)
        self.assertEquals(response.data, serializer.data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_valid_logged_student_discipline_class_list(self):
        """
        Test found the discipline classes list by student.
        """

        classes = ClassRoom.objects.filter(
            discipline=self.discipline01.id
        )
        self.client.force_authenticate(self.student)
        serializer = ClassRoomRegisterSerializer(classes, many=True)
        url = reverse(
            'classroom:list-create',
            kwargs={'discipline_id': self.discipline01.id}
        )
        response = self.client.get(url)
        self.assertEquals(classes.count(), 1)
        self.assertEquals(response.data, serializer.data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_invalid_url_discipline_class_list(self):
        """
        Test not found the specific discipline class
        """

        classes = ClassRoom.objects.filter(
            discipline=self.discipline01.id
        )
        self.client.force_authenticate(self.teacher01)
        serializer = ClassRoomRegisterSerializer(classes, many=True)
        url = reverse(
            'classroom:list-create',
            kwargs={'discipline_id': 30}
        )
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_own_discipline_class_detail(self):
        """
        Test found the own discipline class.
        """

        self.client.force_authenticate(self.teacher01)
        serializer = ClassRoomSerializer(self.classroom01)
        url = self.get_url(self.discipline01.id, self.classroom01.id)
        response = self.client.get(url)
        self.assertEquals(response.data, serializer.data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_not_logged_valid_discipline_class_detail(self):
        """
        Test found the discipline class by not logged user.
        """

        serializer = ClassRoomSerializer(self.classroom01)
        url = self.get_url(self.discipline01.id, self.classroom01.id)
        response = self.client.get(url)
        self.assertEquals(response.data, serializer.data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_student_valid_discipline_class_detail(self):
        """
        Test found the disciipline class by student.
        """

        self.client.force_authenticate(self.student)
        serializer = ClassRoomSerializer(self.classroom01)
        url = self.get_url(self.discipline01.id, self.classroom01.id)
        response = self.client.get(url)
        self.assertEquals(response.data, serializer.data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_valid_another_discipline_class_detail(self):
        """
        Test found the discipline from another teacher.
        """

        self.client.force_authenticate(self.teacher02)
        serializer = ClassRoomSerializer(self.classroom01)
        url = self.get_url(self.discipline01.id, self.classroom01.id)
        response = self.client.get(url)
        self.assertEquals(response.data, serializer.data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_invalid_url_discipline_class_detail(self):
        """
        Test to see class that not exists for specific discipline.
        """

        self.client.force_authenticate(self.teacher01)
        url = self.get_url(self.discipline01.id, self.classroom02.id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def get_url(self, discipline_id, class_id):
        """
        Get the specific discipline classes URL.
        """

        url = reverse(
            'classroom:details',
            kwargs={'discipline_id': discipline_id, 'class_id': class_id})

        return url

