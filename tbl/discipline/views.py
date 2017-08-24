from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from .serializers import (
    DisciplineSerializer,
)
from .permissions import (
    OnlyLoggedTeacherCanCreateDiscipline,
    UpdateYourOwnDisciplines
)
from .models import Discipline


class DisciplineListCreateAPIView(ListCreateAPIView):
    """
    Controller that allows any logged teacher to create disciplines and
    any logged students to see all disciplines.
    """

    serializer_class = DisciplineSerializer

    permission_classes = (OnlyLoggedTeacherCanCreateDiscipline, )

    queryset = Discipline.objects.all()

    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'teacher')
    ordering_fields = ('title')


class DisciplineAPIView(RetrieveUpdateDestroyAPIView):
    """
    Controller that allows specific logged teacher to destroy and update the
    discipline and allow any logged user to see the discipline.
    """

    serializer_class = DisciplineSerializer

    permission_classes = (UpdateYourOwnDisciplines, )

    queryset = Discipline.objects.all()
