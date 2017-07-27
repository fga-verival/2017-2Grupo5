from rest_framework.serializers import (
    ModelSerializer,
    EmailField,
    CharField,
    ValidationError
)
from .models import User


class UserSerializer(ModelSerializer):
    """
    A serializer for our user profile objects.
    """

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'institution', 'photo')


class UserRegisterSerializer(ModelSerializer):
    """
    A serializer to register a new user.
    """

    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        email = data['email']
        user = User.objects.filter(email=email)
        if user.exists():
            raise ValidationError('This user has already registered.')

        return data

    def create(self, validated_data):
        """
        Create and return a new user.
        """

        user = User(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()

        return validated_data
