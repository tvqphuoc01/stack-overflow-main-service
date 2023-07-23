from rest_framework import serializers
from api.models import Tag, Category, Question

class QuestionSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=100)
    content = serializers.CharField(required=True)
    user_id = serializers.CharField(required=True)

class QuestionLikeSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)
    question_id = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all(),
        source='question',
        write_only=True
    )

