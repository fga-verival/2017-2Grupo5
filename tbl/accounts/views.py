from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """
    Handles creating, heading, delete and update profiles
    """
    pass

    serializer_class = UserSerializer

    queryset = User.objects.all()
