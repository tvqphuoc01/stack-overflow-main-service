from rest_framework import serializers
from api.models import Answer, Question

class AnswerSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)
    question_id =serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all(),
        write_only=True
    )
    content = serializers.CharField(required=True)
    image_url = serializers.CharField(required=False)

class AnswerLikeSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)
    answer_id = serializers.PrimaryKeyRelatedField(
        queryset=Answer.objects.all(),
        source='answer',
        write_only=True
    )
