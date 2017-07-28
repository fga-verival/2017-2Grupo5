from rest_framework.filters import (
    SearchFilter, OrderingFilter
)
from rest_framework.permissions import (
    AllowAny, IsAuthenticated
)
from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
)
from .serializers import (
    UserSerializer, UserRegisterSerializer, UserPasswordSerializer
)
from .models import User
from .permissions import UpdateOwnProfile


class UserRegisterAPIView(CreateAPIView):
    """
    Controller that allows any user to register to the system.
    """

    serializer_class = UserRegisterSerializer

    permission_classes = [AllowAny]

    # Take the authentication default off, you don't need to be
    # authenticated to use this funcionality
    authentication_classes = ()


class UserListAPIView(ListAPIView):
    """
    Controller that allows any logged user see all users.
    """

    serializer_class = UserSerializer

    queryset = User.objects.all()

    permission_classes = [IsAuthenticated]

    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'email')
    ordering_fields = ('email', )


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
