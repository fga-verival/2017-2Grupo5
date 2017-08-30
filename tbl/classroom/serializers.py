from django.utils.translation import ugettext_lazy as _
from rest_framework.serializers import (
    ModelSerializer, CharField, ValidationError
)
from .models import ClassRoom, Discipline


class ClassRoomSerializer(ModelSerializer):
    """
    A serializer to update, delete and view classes of specific discipline.
    """

    class Meta:
        model = ClassRoom
        fields = (
            'id', 'title', 'password', 'student_limit', 'is_closed',
            'discipline', 'students'
        )
        extra_kwargs = {
            'discipline': {'read_only': True},
            'password': {'read_only': True}
        }


class ClassRoomRegisterSerializer(ModelSerializer):
    """
    A serializer to list and register a new classes of specific discipline
    """
    password = CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = ClassRoom
        fields = (
            'id', 'title', 'password', 'student_limit', 'is_closed',
            'discipline', 'students'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'discipline': {'read_only': True}
        }

    def create(self, validated_data):
        """
        Create and return a new discipline class
        """

        discipline = Discipline.objects.get(
            id=self.context['discipline'].id
        )

        # Remove the many to many field to create instance
        students = validated_data.pop('students')

        # Create instance
        classroom = ClassRoom(
            title=validated_data['title'],
            password=validated_data['password'],
            student_limit=validated_data['student_limit'],
            is_closed=validated_data['is_closed'],
            discipline=discipline,
        )

        classroom.save()

        # Insert many to many field to instance
        classroom.students = students

        return classroom


class ClassRoomPasswordSerializer(ModelSerializer):
    """
    A serializer to edit classroom password.
    """

    password = CharField(write_only=True, style={'input_type': 'password'})
    new_password = CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    confirm_password = CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = ClassRoom
        fields = ('password', 'new_password', 'confirm_password')

    @staticmethod
    def update(instance, validated_data):
        """
        Update the classroom password.
        """

        password = validated_data['password']
        new_password = validated_data['new_password']
        confirm_password = validated_data['confirm_password']

        # Verify if new password and confirm password match.
        if new_password != confirm_password:
            raise ValidationError(_('The new passwords do not match.'))

        # Verify if the old password is correct.
        if password != instance.password:
            raise ValidationError(_('Old password invalid.'))

        instance.password = new_password

        instance.save()

        return instance
