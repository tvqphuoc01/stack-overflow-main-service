from api.models import Question, ForbiddenWord
import requests
import re

def approve_question():
    # print("approve_question")
    questions = Question.objects.filter(question_status=0).all()
    authen_url = "http://stack-overflow-authen-authenticator-1:8000/api/get-user-by-id"

    forbidden_words = ForbiddenWord.objects.values_list('word', flat=True)
    for question in questions:
        content = question.content.lower()
        title = question.title.lower()
        checkContent = any(re.search(r'\b' + re.escape(word) + r'\b', content) for word in forbidden_words)
        checkTitle = any(re.search(r'\b' + re.escape(word) + r'\b', title) for word in forbidden_words)
        if checkContent or checkTitle:
            question.question_status = 2
        else:
            response = requests.get(authen_url, params={"user_id": question.user_id})
            if response.status_code != 200:
                question.question_status = 2
            else:
                res_json = response.json()
                user = res_json["data"]
                if (user["user_points"] >= 10):
                    question.question_status = 1
        question.save()