from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.compat import is_authenticated


class UpdateOwnProfile(BasePermission):
    """
    Allow users to edit their own profile.
    """

    @staticmethod
    def has_object_permission(request, view, obj):
        """
        Check user is trying to edit their own profile.
        """

        # Can view other peoples but can't edit
        if request.method in SAFE_METHODS:
            return True

        # It will check if the profile ID that they're trying to update
        # is the authenticated user profile, their own profile.
        return obj.id == request.user.id


class CreateListUserPermission(BasePermission):
    """
    Allow to register on system only if not authenticated
    or if user is admin.
    """

    @staticmethod
    def has_permission(request, view):
        only_list_users = request.method in SAFE_METHODS
        is_not_logged = not is_authenticated(request.user)
        is_logged = is_authenticated(request.user)
        has_user = request.user
        is_admin_user = request.user.is_staff

        if only_list_users or is_not_logged:
            return True

        if is_logged and has_user and is_admin_user:
            return True

        return False
