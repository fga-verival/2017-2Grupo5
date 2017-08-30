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

        return is_logged(request) and is_admin(request)


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

    return request.user and is_authenticated(request.user)


def is_admin(request):
    """
    Verify if user is admin
    """

    return request.user.is_staff


def is_teacher(request):
    """
    Verify if logged user is teacher.
    """
    is_teacher = False

    if is_logged(request):
        is_teacher = request.user.is_teacher

    return is_teacher
