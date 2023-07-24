from rest_framework import serializers
from api.models import Answer, Reply

class ReplySerializer(serializers.Serializer):
    owner_id = serializers.CharField(required=True)
    answer_id = serializers.PrimaryKeyRelatedField(
        queryset=Answer.objects.all(),
        source="answer",
        write_only=True
    )
    content = serializers.CharField(required=True)
    image_url = serializers.CharField(required=False)

class ReplyLikeSerializer(serializers.Serializer):
    reply_id=serializers.PrimaryKeyRelatedField(
        queryset=Reply.objects.all(),
        source="reply",
        write_only=True
    ),
    user_id = serializers.CharField(required=True),

class ReplyResponseDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ('reply_id', 'owner_id', 'answer_id', 'content', 'number_of_like', 'number_of_dislike', 'answer_status', 'image_url', 'create_date', 'update_date')
        read_only_fields = ('reply_id', 'number_of_like', 'number_of_dislike', 'answer_status', 'create_date', 'update_date')