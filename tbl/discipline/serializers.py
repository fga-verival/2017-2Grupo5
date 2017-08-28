from rest_framework.serializers import (
    ModelSerializer
)
from accounts.models import Teacher
from .models import Discipline


class DisciplineSerializer(ModelSerializer):
    """
    A serializer to list and register a new discipline.
    """

    class Meta:
        model = Discipline
        fields = (
            'id', 'title', 'description', 'course', 'teacher'
        )
        extra_kwargs = {'teacher': {'read_only': True}}

    def current_user(self):
        """
        Method to get the current teacher logged.
        """

        teacher = self.context['request'].user.id
        return teacher

    def create(self, validated_data):
        """
        Create and return a new discipline
        """

        teacher = Teacher.objects.get(id=self.current_user())

        discipline = Discipline(
          title=validated_data['title'],
          description=validated_data['description'],
          course=validated_data['course'],
          teacher=teacher
        )

        discipline.save()

        return discipline
