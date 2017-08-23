from django.conf.urls import url
from . import views

app_name = 'discipline'
urlpatterns = [
    url(
        r'^$',
        views.DisciplineListCreateAPIView.as_view(),
        name='list-create'
    ),
]
