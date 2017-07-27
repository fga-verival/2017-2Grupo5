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
            'created_at', 'updated_at'
        )


class UserRegisterSerializer(ModelSerializer):
    """
    A serializer to register a new user.
    """

    confirm_password = CharField()

    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }

    def validate(self, data):
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

    def create(self, validated_data):
        """
        Create and return a new user.
        """

        user = User(
            email=validated_data['email'],
            name=validated_data['name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return validated_data
