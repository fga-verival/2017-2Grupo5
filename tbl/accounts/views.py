from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import (AllowAny, IsAuthenticatedOrReadOnly)
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .serializers import (UserSerializer, UserRegisterSerializer)
from .models import User
from .permissions import UpdateOwnProfile


class UserRegisterAPIView(CreateAPIView):
    """
    Controller of user register.
    """

    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer


class UserListAPIView(ListAPIView):
    """
    Controller to list all users.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'email')
    ordering_fields = ('email', )


class UserAPIView(RetrieveUpdateDestroyAPIView):
    """
    Controller to show, edit and delete user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, UpdateOwnProfile)
