from api.models import Notification

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def send_notification(request):
    user_id = request.GET.get('user_id')
    content = request.GET.get('content')
    question_id = request.GET.get('question_id')
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
    
    notification = Notification.objects.create(
        owner_id=user_id,
        question_id=question_id,
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
        
    notification_list = Notification.objects.filter(user_id=user_id).order_by('-create_date')
    notification_list_data = []
    
    for notification in notification_list:
        notification_list_data.append(
            {
                "id": notification.noti_id,
                "user_id": notification.owner_id,
                "content": notification.content,
                "create_date": notification.create_date,
                "is_checked": notification.is_checked
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