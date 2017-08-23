from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView, UpdateAPIView, ListCreateAPIView
)
from .serializers import (
    UserSerializer, UserRegisterSerializer, UserPasswordSerializer
)
from .models import User
from .permissions import UpdateOwnProfile, CreateListUserPermission


class UserListCreateAPIView(ListCreateAPIView):
    """
    Controller that allows any logged user see all users and only not
    logged user and admin user to create user.
    """

    serializer_class = UserRegisterSerializer

    queryset = User.objects.all()

    permission_classes = [CreateListUserPermission]

    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'email')
    ordering_fields = ('email', 'institution')


class UserAPIView(RetrieveUpdateDestroyAPIView):
    """
    Controller that allows a logged-in user to view edit and
    delete your account.
    """

    serializer_class = UserSerializer

    queryset = User.objects.all()

    permission_classes = (IsAuthenticated, UpdateOwnProfile)


class UserPasswordAPIView(UpdateAPIView):
    """
    Controller that allows a logged-in user to edit your own password.
    """

    serializer_class = UserPasswordSerializer

    queryset = User.objects.all()

    permission_classes = (IsAuthenticated, UpdateOwnProfile)
