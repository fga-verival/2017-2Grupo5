from rest_framework.permissions import BasePermission, SAFE_METHODS


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
