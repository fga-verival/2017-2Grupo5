import datetime

# Django Rest Framework
# http://www.django-rest-framework.org/
# http://getblimp.github.io/django-rest-framework-jwt/
REST_FRAMEWORK = {
    # Use the extension ModHeaders of Chrome to login
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ),
    # All tests with json format
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

JWT_AUTH = {
    # Expiration time of token: 30 min
    # When expirated we need to get another token
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=1800),
}
