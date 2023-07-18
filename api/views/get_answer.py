import requests
from api.models import Answer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers.answer_serializers import AnswerSerializer

@api_view(['GET'])
def get_answer_of_question_by_id(request):
    question_id = request.GET.get('question_id')
    if not question_id:
        return Response(
            {
                "message": "Question id is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
    answer = Answer.objects.filter(question_id=question_id, answer_status=True).all()
    if not answer:
        return Response(
            {
                "message": "Answer is not available"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    answer_data = []
    
    for ans in answer:
        authen_url = "http://authenticator-authenticator-1:8000/api/get-user-by-id"
        response = requests.get(authen_url, params={"user_id": ans.user_id})
        
        if response.status_code != 200:
            return Response(
                {
                    "message": "Get user info failed",
                    "data": answer_data
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        answer_data.append({
            "id": ans.id,
            "user_data": response.json(),
            "content": ans.content,
            "number_of_like": ans.number_of_like,
            "number_of_dislike": ans.number_of_dislike,
            "create_date": ans.create_date,
        })
        
    return Response(
        {
            "message": "Get answer successfully",
            "data": answer_data
        },
        status=status.HTTP_200_OK
    )

@api_view(["POST"])
def create_answer(request):
    serializer = AnswerSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data

    # answer data
    user_id = validated_data.get('user_id')
    image_url = validated_data.get('image_url', '')
    content = validated_data.get('content')
    question_id = validated_data.get('question_id')

    url = "http://stack-overflow-authen-authenticator-1:8000" + "/api/check-user"
    params = {'user_id': user_id}

    response = requests.get(url, params=params)
    if (response.status_code == 200):
        res = response.json()
        if (res["message"] == True):
            try:
                answer, created = Answer.objects.get_or_create(question_id=question_id, content=content, user_id=user_id, image_url=image_url)
                if created == False:
                    return Response(
                        {
                            'message': 'Create answer failed'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(
                    {
                        'message': 'Answer created'
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