from rest_framework.permissions import BasePermission
from core.permissions import (
    is_read_mode, is_teacher
)
from accounts.models import Teacher


class ListCreateClassRoomPermission(BasePermission):
    """
    Allow only logged teacher to create classes to your own disciplines and
    allow any users to see the classes.
    """

    @staticmethod
    def has_permission(request, view):

        if (is_teacher(request) and
            is_discipline_owner(request, view) or
            is_read_mode(request)):

            return True

        return False


class UpdateRetrieveDestroyClassRoomPermission(BasePermission):
    """
    Allow only logged teacher to update or delete classes to your own
    disciplines and allow any users to see the classes.
    """

    @staticmethod
    def has_object_permission(request, view, obj):

        if (is_teacher(request) and
            is_discipline_owner(request, view) and
            is_class_owner(view, obj) or
            is_read_mode(request)):

            return True

        return False


def is_discipline_owner(request, view):
    """
    It will check if the discipline class that they're trying
    to create is your own discipline.
    """
    is_owner = False

    teacher = Teacher.objects.get(id=request.user.id)

    for discipline in teacher.disciplines.all():
        if view.kwargs['discipline_id'] == str(discipline.id):
            is_owner = True

    return is_owner


def is_class_owner(view, obj):
    """
    It will check if the discipline class that they're trying
    to update or delete is your own discipline
    """

    if (str(obj.discipline.id) == view.kwargs['discipline_id'] and
        str(obj.id) == view.kwargs['class_id']):

        return True

    return False
