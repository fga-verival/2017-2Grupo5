from django.conf.urls import url, include
from django.contrib import admin

# API Urls
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls')),
    # Include the login and logout views for the browsable API
    url(r'api-auth', include('rest_framework.urls', namespace='rest_framework'))
]
