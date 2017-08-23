from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (
    ListCreateAPIView
)
from .serializers import (
    DisciplineListCreateSerializer
)
from .permissions import (
    OnlyLoggedTeacherCanCreateDiscipline,
)
from .models import Discipline


class DisciplineListCreateAPIView(ListCreateAPIView):
    """
    Controller that allows any logged teacher to create disciplines and
    any logged students to see all disciplines.
    """

    serializer_class = DisciplineListCreateSerializer

    permission_classes = (OnlyLoggedTeacherCanCreateDiscipline, )

    queryset = Discipline.objects.all()

    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'teacher')
    ordering_fields = ('title')
