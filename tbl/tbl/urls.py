from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

# API Urls
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls')),
    # This url will display a system login form
    url(
        r'^api-auth/',
        include('rest_framework.urls')
    ),
]

# While in development mode we will use relative URL for static and average
# files. In production mode we will no longer need this folder as we will store
# everything on a server
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
