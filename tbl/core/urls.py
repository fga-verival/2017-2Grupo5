from django.conf.urls import url
from . import views

app_name = 'news'
urlpatterns = [
    url(
        r'^$',
        views.NewsListCreateAPIView.as_view(),
        name='list-create'
    ),
    url(
        r'^(?P<pk>[0-9]+)/$',
        views.KeepNewsAPIView.as_view(),
        name='keep-news'
    )
]
