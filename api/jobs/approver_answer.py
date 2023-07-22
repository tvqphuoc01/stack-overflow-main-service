from api.models import Answer
import requests

def approve_answer():
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