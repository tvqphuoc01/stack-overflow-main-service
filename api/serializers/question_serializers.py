from rest_framework import serializers
from api.models import Tag, Category

class QuestionSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=100)
    tag_id = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        source='tag',
        write_only=True
    )
    content = serializers.CharField(required=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    user_id = serializers.CharField(required=True)