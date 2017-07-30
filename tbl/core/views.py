from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)
from .serializers import NewsSerializer
from .models import News
from .permissions import CreateUpdateDestroyAdminPermission


class NewsListCreateAPIView(ListCreateAPIView):
    """
    Controller that allows any user to see all news.
    """

    serializer_class = NewsSerializer

    queryset = News.objects.all()

    permission_classes = [CreateUpdateDestroyAdminPermission]

    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'tags')
    ordering_fields = ('created_at', )


class KeepNewsAPIView(RetrieveUpdateDestroyAPIView):
    """
    Controller that allows any user to see specific news.
    """

    serializer_class = NewsSerializer

    queryset = News.objects.all()

    permission_classes = [CreateUpdateDestroyAdminPermission]
