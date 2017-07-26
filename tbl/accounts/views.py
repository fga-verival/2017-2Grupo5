from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter
from .models import User
from .serializers import UserSerializer
from .permissions import UpdateOwnProfile


class UserViewSet(ModelViewSet):
    """
    Handles creating, heading, delete and update profiles
    """

    serializer_class = UserSerializer

    queryset = User.objects.all()

    # It will only allow them to update, create and modify if they're
    # logged in or it will restrict them to read-only and it will
    # restrict to only their own profile.
    permission_classes = (UpdateOwnProfile, IsAuthenticatedOrReadOnly)

    filter_backends = (SearchFilter,)
    search_fields = ('name', 'email')
