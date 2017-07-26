from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter
from .models import User
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """
    Handles creating, heading, delete and update profiles
    """

    serializer_class = UserSerializer

    queryset = User.objects.all()

    permission_classes = (IsAuthenticatedOrReadOnly,)

    filter_backends = (SearchFilter,)
    search_fields = ('name', 'email')
