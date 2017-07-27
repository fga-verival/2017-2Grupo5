from rest_framework.serializers import (
    ModelSerializer,
    EmailField,
    CharField,
    ValidationError
)
from uuid import uuid4
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


class UserLoginSerializer(ModelSerializer):
    """
    A serializer to authentication login.
    """

    token = CharField(allow_blank=True, read_only=True)
    email = EmailField(label='Email address', allow_blank=True, required=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'token']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        user = None
        password = data['password']

        # Verify if email is empty
        email = data.get('email', None)
        if not email:
            raise ValidationError('The email is required to login.')

        # Verify if exists another user with the same email address
        users = User.objects.filter(email=email)
        if users.exists() and users.count() == 1:
            user = users.first()
        else:
            raise ValidationError('The email is not valid!')

        # Verify if the password inserted is correct.
        if user:
            if not user.check_password(password):
                raise ValidationError('Invalid credentials, please try again')

        # Creates a unique token every time it's called
        data['token'] = uuid4()

        return data
