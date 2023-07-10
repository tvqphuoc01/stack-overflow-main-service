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
    user_id_list = []
    for ans in answer:
        answer_data.append({
            "id": ans.id,
            "user_id": ans.user_id,
            "question_id": ans.question_id,
            "content": ans.content,
            "number_of_like": ans.number_of_like,
            "number_of_dislike": ans.number_of_dislike,
            "create_date": ans.create_date,
        })
        user_id_list.append(ans.user_id)
        
    authen_url = "http://localhost:8000/api/authen/get_user_by_id"
    
    response = requests.get(authen_url, params={"user_id": user_id_list})
    
    if response.status_code != 200:
        return Response(
            {
                "message": "Get user info failed",
                "data": answer_data
            },
            status=status.HTTP_200_OK
        )
    
    response_data = response.json()

    # TODO HANDLE ADD USER INFO TO ANSWER DATA
    
    return Response(
        {
            "message": "Get answer successfully",
            "data": answer_data
        },
        status=status.HTTP_200_OK
    )