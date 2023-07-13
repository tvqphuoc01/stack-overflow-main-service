import requests
from api.models import Answer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

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