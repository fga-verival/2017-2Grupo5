from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(
        r'^$',
        views.UserListAPIView.as_view(),
        name='list'
    ),
    url(
        r'^register/$',
        views.UserRegisterAPIView.as_view(),
        name='register'
    ),
    url(
        r'^(?P<pk>[0-9]+)/$',
        views.UserAPIView.as_view(),
        name='details'
    ),
    url(
        r'^login/$',
        views.UserLoginAPIView.as_view(),
        name='login'
    ),
    url(
        r'^api-auth/',
        include('rest_framework.urls')
    )
]
