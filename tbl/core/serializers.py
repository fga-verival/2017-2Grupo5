from rest_framework.serializers import ModelSerializer
from .models import News


class NewsSerializer(ModelSerializer):
    """
    A serializer for our news objects.
    """

    class Meta:
        model = News
        fields = '__all__'
