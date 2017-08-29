from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.compat import is_authenticated
from core.permissions import (
    is_read_mode, is_logged, has_user, is_admin, is_owner
)


class UpdateOwnProfile(BasePermission):
    """
    Allow users to edit their own profile.
    """

    @staticmethod
    def has_object_permission(request, view, obj):
        """
        Check user is trying to edit their own profile.
        """

        if is_read_mode(request):
            return True

        return is_owner(request, obj)


class CreateListUserPermission(BasePermission):
    """
    Allow to register on system only if not authenticated
    or if user is admin.
    """

    @staticmethod
    def has_permission(request, view):

        if is_read_mode(request) or not is_logged(request):
            return True

        if is_logged(request) and has_user(request) and is_admin(request):
            return True

        return False
