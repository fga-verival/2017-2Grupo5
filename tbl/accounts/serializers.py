from rest_framework.serializers import (
    ModelSerializer, CharField, ValidationError
)
from .models import User


class UserSerializer(ModelSerializer):
    """
    A serializer for our user profile objects.
    """

    class Meta:
        model = User
        fields = (
            'id', 'email', 'name', 'institution', 'course', 'photo',
            'is_teacher', 'last_login', 'created_at', 'updated_at'
        )


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
            raise ValidationError('The new passwords do not match.')

        # Verify if the old password is correct.
        if not instance.check_password(password):
            raise ValidationError('Old password invalid.')

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

    class Meta:
        model = User
        fields = [
            'name', 'email', 'is_teacher', 'password', 'confirm_password'
        ]

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
            raise ValidationError('This user has already registered.')

        # Verify if the passwords not match.
        if password != confirm_password:
            raise ValidationError('The passwords do not match.')

        return data

    @staticmethod
    def create(validated_data):
        """
        Create and return a new user.
        """

        user = User(
            email=validated_data['email'],
            name=validated_data['name'],
            is_teacher=validated_data['is_teacher']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
