import requests
from api.models import Reply, Answer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers.reply_serializers import ReplySerializer

@api_view(["POST"])
def create_reply(request):
    serializer = ReplySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data

    # answer data
    owner_id = validated_data.get('owner_id')
    answer = validated_data.get('answer')
    content = validated_data.get('content')
    image_url = validated_data.get('image_url', '')
    
    url = "http://stack-overflow-authen-authenticator-1:8000" + "/api/check-user"
    params = {'user_id': owner_id}

    response = requests.get(url, params=params)
    if (response.status_code == 200):
        res = response.json()
        if (res["message"] == True):
            try:
                reply, created = Reply.objects.get_or_create(owner_id=owner_id, question_id=answer.question_id, answer_id=answer, content=content, image_url=image_url)
                if created == False:
                    return Response(
                        {
                            'message': 'Create reply failed'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(
                    {
                        'message': 'Reply created'
                    }
                )
            except Exception as e:
                return Response(
                    {
                        'message': 'Internal server error',
                        'error': f'{e}'
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
    return Response(
            {
                'message': 'User not found',
            },
            status=status.HTTP_400_BAD_REQUEST
        )