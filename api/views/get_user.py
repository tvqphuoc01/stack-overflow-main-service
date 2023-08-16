from api.models import Question, Answer, Reply
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
import requests

@api_view(["GET"])
def get_top_user(request):
    amount = request.GET.get("amount", 10)
    filter_data = request.GET.get("filter", "question")

    queryset = []
    querysetReply = []
    if (filter_data == "question"):
        queryset = Question.objects.filter(question_status=1).values("user_id").annotate(question_count=Count('user_id')).order_by('-question_count').all()[:amount]
    else:
        queryset = Answer.objects.filter(answer_status=1).values("user_id").annotate(answer_count=Count('user_id')).order_by('-answer_count').all()[:amount]

    url = "http://stack-overflow-authen-authenticator-1:8000" + "/api/get-user-by-id-for-ranking-table"
    
    list_data = []
    for item in queryset:
        params = {'user_id': item["user_id"]}
    
        response = requests.get(url, params=params)
        res = response.json()
        
        if (response.ok):
            if (filter_data == "question"):
                answer_count = Answer.objects.filter(user_id=item["user_id"], answer_status=1).count()       
                list_data.append(
                    {
                        "user":{
                            "id": item["user_id"],
                            "image_url": res["data"]["image_url"],
                            "full_name": res["data"]["full_name"],
                        },
                        "question_count": item["question_count"],
                        "answer_count": answer_count
                    }
                )
            else:
                question_count = Question.objects.filter(user_id=item["user_id"], question_status=1).count()
                list_data.append(
                    {
                        "user":{
                            "id": item["user_id"],
                            "image_url": res["data"]["image_url"],
                            "full_name": res["data"]["full_name"],
                        },
                        "question_count": question_count,
                        "answer_count": item["answer_count"]
                    }
                )
    return Response(
        {
            "message": "Get question successfully",
            "data": list_data
        },
        status=status.HTTP_200_OK
    )