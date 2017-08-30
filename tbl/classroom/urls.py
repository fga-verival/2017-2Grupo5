from django.conf.urls import url
from . import views

app_name = 'classroom'
urlpatterns = [
    url(
        r'^disciplines/(?P<discipline_id>[0-9]+)/classes/$',
        views.ClassRoomListCreateAPIView.as_view(),
        name='list-create'
    ),
    url(
        r'^disciplines/(?P<discipline_id>[0-9]+)/classes/(?P<class_id>[0-9]+)/$',
        views.ClassRoomAPIView.as_view(),
        name='details'
    ),
    url(
        r'^disciplines/(?P<discipline_id>[0-9]+)/classes/(?P<class_id>[0-9]+)/password/$',
        views.ClassRoomPasswordAPIView.as_view(),
        name='password'
    ),
]
