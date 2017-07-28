from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from . import views

app_name = 'accounts'
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
        r'^(?P<pk>[0-9]+)/password$',
        views.UserPasswordAPIView.as_view(),
        name='password'
    ),
    url(
        r'^login/',
        obtain_jwt_token,
        name='login'
    ),
]
