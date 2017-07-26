from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    # Determine automatically the routes by router
    url(r'^', include(router.urls)),
]
