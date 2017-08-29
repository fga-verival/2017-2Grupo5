from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.compat import is_authenticated


class CreateUpdateDestroyAdminPermission(BasePermission):
    """
    Permission to only admin can edit, create and delete news.
    """

    @staticmethod
    def has_permission(request, view):
        if is_read_mode(request):
            return True

        return has_user(request) and is_logged(request) and is_admin(request)


def is_read_mode(request):
    """
    List and Retrieve method, only read mode (safe methods)
    """

    if request.method in SAFE_METHODS:
        return True

    return False


def is_logged(request):
    """
    Verify if user is logged or not
    """

    return is_authenticated(request.user)


def has_user(request):
    """
    Verify if has a user in the system.
    """

    return request.user


def is_admin(request):
    """
    Verify if user is admin
    """

    return request.user.is_staff


def is_owner(request, obj):
    """
    It will check if the object ID that they're trying to update
    is the authenticated user object, their own object.
    """

    return obj.id == request.user.id
