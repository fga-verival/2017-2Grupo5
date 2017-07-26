from rest_framework.serializers import ModelSerializer
from .models import User


class UserSerializer(ModelSerializer):
    """
    A serializer for our user profile objects.
    """

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'institution', 'photo', 'password')
        extra_kwargs = {'password': {'write_only': True}}

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

        return user
