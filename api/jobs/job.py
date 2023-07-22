from api.models import Question, Answer, Reply
import requests

def approve_question_auto():
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

def approve_answer_auto():
    answers = Answer.objects.filter(answer_status=0).all()
    authen_url = "http://stack-overflow-authen-authenticator-1:8000/api/get-user-by-id"
    for answer in answers:
        response = requests.get(authen_url, params={"user_id": answer.user_id})
        if response.status_code != 200:
            answer.answer_status = 2
        else:
            res_json = response.json()
            user = res_json["data"]
            if (user["user_points"] >= 10):
                answer.answer_status = 1
        answer.save()

def approve_reply_auto():
    replies = Reply.objects.filter(answer_status=0).all()
    authen_url = "http://stack-overflow-authen-authenticator-1:8000/api/get-user-by-id"
    for reply in replies:
        response = requests.get(authen_url, params={"user_id": reply.user_id})
        if response.status_code != 200:
            reply.answer_status = 2
        else:
            res_json = response.json()
            user = res_json["data"]
            if (user["user_points"] >= 10):
                reply.answer_status = 1
        reply.save()