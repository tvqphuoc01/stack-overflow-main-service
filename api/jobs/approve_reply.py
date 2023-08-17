from api.models import Reply
import requests

def approve_reply():
    replies = Reply.objects.filter(answer_status=0).all()
    authen_url = "http://stack-overflow-authen-authenticator-1:8000/api/get-user-by-id"
    for reply in replies:
        response = requests.get(authen_url, params={"user_id": reply.owner_id})
        if response.status_code != 200:
            reply.answer_status = 2
        else:
            res_json = response.json()
            user = res_json["data"]
            if (user["user_points"] >= 10):
                reply.answer_status = 1
        reply.save()