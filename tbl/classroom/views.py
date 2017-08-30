from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView
)
from .permissions import (
    ListCreateClassRoomPermission,
    UpdateRetrieveDestroyClassRoomPermission
)
from .serializers import (
    ClassRoomRegisterSerializer,
    ClassRoomSerializer,
    ClassRoomPasswordSerializer
)
from .models import ClassRoom
from discipline.models import Discipline


class ClassRoomListCreateAPIView(ListCreateAPIView):
    """
    Controller that allows any logged teacher to create classes of specific
    discipline and any logged students to see all classes
    """

    serializer_class = ClassRoomRegisterSerializer

    permission_classes = (ListCreateClassRoomPermission, )

    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title')
    ordering_fields = ('title')

    def get_queryset(self):
        """
        List of view items, query to the database
        """

        discipline = get_object_or_404(
            Discipline,
            pk=self.kwargs['discipline_id']
        )

        queryset = ClassRoom.objects.filter(
            discipline=discipline
        )

        return queryset

    def get_serializer_context(self):
        """
        Used to insert extra content into serialization classes.
        Default content: request, format, view
        """

        discipline = get_object_or_404(
            Discipline,
            pk=self.kwargs['discipline_id']
        )

        return {
            'request': self.request,
            'discipline': discipline
        }


class ClassRoomAPIView(RetrieveUpdateDestroyAPIView):
    """
    Controller that allows any logged teacher to update classes of specific
    discipline and any logged students to see the specific class
    """

    serializer_class = ClassRoomSerializer

    permission_classes = (UpdateRetrieveDestroyClassRoomPermission, )

    lookup_url_kwarg = 'class_id'

    def get_queryset(self):
        """
        List of view items, query to the database
        """

        queryset = ClassRoom.objects.filter(
            discipline=self.kwargs['discipline_id']
        )

        return queryset


    def get_serializer_context(self):
        """
        Used to insert extra content into serialization classes.
        Default content: request, format, view
        """

        discipline = get_object_or_404(
            Discipline,
            pk=self.kwargs['discipline_id']
        )

        return {
            'request': self.request,
            'discipline': discipline
        }


class ClassRoomPasswordAPIView(UpdateAPIView):
    """
    Controller that allows a logged-in teacher to edit discipline class
    password.
    """

    serializer_class = ClassRoomPasswordSerializer

    lookup_url_kwarg = 'class_id'

    queryset = ClassRoom.objects.all()

    permission_classes = (UpdateRetrieveDestroyClassRoomPermission, )
