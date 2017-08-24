from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.compat import is_authenticated


class OnlyLoggedTeacherCanCreateDiscipline(BasePermission):
    """
    Allow only teacher to create disciplines.
    """

    @staticmethod
    def has_permission(request, view):
        only_list_disciplines = request.method in SAFE_METHODS
        is_logged = is_authenticated(request.user)
        has_user = request.user
        is_teacher = False

        if has_user and is_logged:
            is_teacher = request.user.is_teacher

        if is_teacher or only_list_disciplines:
            return True

        return False


class UpdateYourOwnDisciplines(BasePermission):
    """
    Allow only the specific teacher that created a discipline to update or
    delete it.
    """

    @staticmethod
    def has_object_permission(request, view, obj):
        only_list_disciplines = request.method in SAFE_METHODS
        is_logged = is_authenticated(request.user)
        has_user = request.user
        can_update = False

        if has_user and is_logged:
            can_update = (obj.teacher.id == request.user.id)

        if can_update or only_list_disciplines:
            return True

        return False
