from api.models import Notification, DeviceToken, Question

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.utils.fcm_utils import FcmUtils
import requests

@api_view(['POST'])
def send_notification(request):
    sender_id = request.data.get('sender_id')
    user_id = request.data.get('user_id')
    content = request.data.get('content')
    question_id = request.data.get('question_id')
    if not user_id:
        return Response(
            {
                "message": "User id is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    if not content:
        return Response(
            {
                "message": "Content is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    question = Question.objects.filter(id=question_id).first()
    if not question:
        return Response(
            {
                "message": "Not found question"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    authen_url = "http://stack-overflow-authen-authenticator-1:8000/api/get-user-by-id"
    response = requests.get(authen_url, params={"user_id": sender_id})

    if response.status_code != 200:
        return Response(
            {
                "message": "Get user info failed",
                "data": {}
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    user = response.json()

    deviceTokens = DeviceToken.objects.filter(user_id=sender_id).all()
    deviceTokenList = []
    for token in deviceTokens:
        deviceTokenList.append(token.token)

    user_name = user["data"]["full_name"]

    messaging = FcmUtils()
    messaging.send_to_token_multicast(deviceTokenList, f"{user_name} has commented on your post.", content)

    notification = Notification.objects.create(
        owner_id=user_id,
        question_id=question,
        content=content
    )
    return Response(
        {
            "message": "Send notification successfully",
            "data": {
                "id": notification.noti_id,
                "user_id": notification.owner_id,
                "content": notification.content,
                "create_date": notification.create_date,
            }
        },
        status=status.HTTP_200_OK
    )
    
@api_view(['GET'])
def get_user_notification(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return Response(
            {
                "message": "User id is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
    notification_list = Notification.objects.filter(owner_id=user_id).order_by('-create_date').all()
    notification_list_data = []
    
    for notification in notification_list:
        notification_list_data.append(
            {
                "id": notification.noti_id,
                "user_id": notification.owner_id,
                "content": notification.content,
                "create_date": notification.create_date,
                "is_checked": notification.is_checked,
                "question_id": notification.question_id.id,
            }
        )
    return Response(
        {
            "message": "Get user notification successfully",
            "data": notification_list_data,
            "number_of_noti": len(notification_list_data)
        },
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
def check_notification(request):
    notification_id = request.data.get('notification_id')
    if not notification_id:
        return Response(
            {
                "message": "Notification id is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    notification = Notification.objects.filter(noti_id=notification_id).first()
    if not notification:
        return Response(
            {
                "message": "Notification not found"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    notification.is_checked = True
    notification.save()
    return Response(
        {
            "message": "Checked notification success",
        },
        status=status.HTTP_200_OK
    )