from django.utils.translation import ugettext_lazy as _
from rest_framework.serializers import (
    ModelSerializer, CharField, DateTimeField, ValidationError,
    SerializerMethodField
)
from .models import User, Teacher, Student
from discipline.models import Discipline
from classroom.models import ClassRoom


class UserSerializer(ModelSerializer):
    """
    A serializer for our user profile objects.
    """
    disciplines = SerializerMethodField()
    classes = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'name', 'institution', 'course', 'photo',
            'is_teacher', 'disciplines', 'classes', 'last_login',
            'created_at', 'updated_at'
        )
        extra_kwargs = {'is_teacher': {'read_only': True}}

    def get_disciplines(self, obj):
        """
        If user is a teacher get his disciplines.
        """

        if obj.is_teacher:
            queryset = Discipline.objects.filter(teacher=obj.id)
            disciplines = []
            for discipline in queryset:
                disciplines.append(discipline.id)
            return disciplines
        else:
            return []

    def get_classes(self, obj):
        """
        If user is a student get their classes.
        """

        if not obj.is_teacher:
            return []
        else:
            return []


class UserPasswordSerializer(ModelSerializer):
    """
    A serializer to edit user password.
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
        model = User
        fields = ('password', 'new_password', 'confirm_password')

    @staticmethod
    def update(instance, validated_data):
        """
        Update the user password.
        """

        password = validated_data['password']
        new_password = validated_data['new_password']
        confirm_password = validated_data['confirm_password']

        # Verify if new password and confirm password match.
        if new_password != confirm_password:
            raise ValidationError(_('The new passwords do not match.'))

        # Verify if the old password is correct.
        if not instance.check_password(password):
            raise ValidationError(_('Old password invalid.'))

        instance.set_password(new_password)

        instance.save()

        return instance


class UserRegisterSerializer(ModelSerializer):
    """
    A serializer to register a new user.
    """

    password = CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    confirm_password = CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    last_login = DateTimeField(
        read_only=True
    )

    disciplines = SerializerMethodField()
    classes = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'name', 'email', 'institution', 'course', 'photo',
            'is_teacher', 'disciplines', 'classes', 'last_login',
            'created_at', 'updated_at', 'password', 'confirm_password'
        )

    def get_disciplines(self, obj):
        """
        If user is a teacher get his disciplines.
        """

        if obj.is_teacher:
            queryset = Discipline.objects.filter(teacher=obj.id)
            disciplines = []
            for discipline in queryset:
                disciplines.append(discipline.id)
            return disciplines
        else:
            return []

    def get_classes(self, obj):
        """
        If user is a student get their classes.
        """

        if not obj.is_teacher:
            return []
        else:
            return []

    @staticmethod
    def validate(data):
        """
        Validate if existis another user with same email address and verify
        if the password not match.
        """

        email = data['email']
        password = data['password']
        confirm_password = data['confirm_password']

        # Verify if exists another user with same email address
        user = User.objects.filter(email=email)
        if user.exists():
            raise ValidationError(_('This user has already registered.'))

        # Verify if the passwords not match.
        if password != confirm_password:
            raise ValidationError(_('The passwords do not match.'))

        return data

    @staticmethod
    def create(validated_data):
        """
        Create and return a new user.
        """

        if validated_data['is_teacher'] is True:
            user = Teacher(
                email=validated_data['email'],
                name=validated_data['name'],
                is_teacher=validated_data['is_teacher'],
            )
        else:
            user = Student(
                email=validated_data['email'],
                name=validated_data['name'],
                is_teacher=validated_data['is_teacher'],
            )

        user.set_password(validated_data['password'])
        user.save()

        return user
