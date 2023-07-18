from rest_framework import serializers
from api.models import Answer, Question, Reply

class ReplySerializer(serializers.Serializer):
    owner_id = serializers.CharField(required=True)
    answer_id = serializers.PrimaryKeyRelatedField(
        queryset=Answer.objects.all(),
        source="answer",
        write_only=True
    )
    content = serializers.CharField(required=True)
    image_url = serializers.CharField(required=False)