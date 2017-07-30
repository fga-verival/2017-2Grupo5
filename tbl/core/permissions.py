from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.compat import is_authenticated


class CreateUpdateDestroyAdminPermission(BasePermission):
    """
    Permission to only admin can edit, create and delete news.
    """

    @staticmethod
    def has_permission(request, view):
        # List and Retrieve method, only read mode (safe methods)
        if request.method in SAFE_METHODS:
            return True

        is_logged = is_authenticated(request.user)
        has_user = request.user
        is_admin = request.user.is_staff

        return has_user and is_logged and is_admin
