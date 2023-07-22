from api.models import Question
import requests

def approve_question():
    # print("approve_question")
    questions = Question.objects.filter(question_status=0).all()
    authen_url = "http://stack-overflow-authen-authenticator-1:8000/api/get-user-by-id"
    for question in questions:
        response = requests.get(authen_url, params={"user_id": question.user_id})
        if response.status_code != 200:
            question.question_status = 2
        else:
            res_json = response.json()
            user = res_json["data"]
            if (user["user_points"] >= 10):
                question.question_status = 1
        question.save()