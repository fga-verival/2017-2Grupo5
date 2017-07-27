from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import (AllowAny, IsAuthenticatedOrReadOnly)
# from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .serializers import (
    UserSerializer,
    UserRegisterSerializer,
    UserLoginSerializer
)
from .models import User
from .permissions import UpdateOwnProfile


class UserRegisterAPIView(CreateAPIView):
    """
    Controller of user register.
    """

    serializer_class = UserRegisterSerializer

    permission_classes = [AllowAny]


class UserLoginAPIView(APIView):
    """
    Controller to login in the system.
    Checks email and password and returns an auth token.
    """

    serializer_class = UserLoginSerializer

    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        serializer = UserLoginSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.data
            return Response(validated_data, status=HTTP_200_OK)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


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

    serializer_class = UserSerializer

    queryset = User.objects.all()

    permission_classes = (IsAuthenticatedOrReadOnly, UpdateOwnProfile)
