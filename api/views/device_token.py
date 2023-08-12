from api.models import DeviceToken

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

@api_view(["POST"])
def create_device_token(request):
    token = request.data.get("token")
    user_id = request.data.get("user_id")
    if not token:
       return Response(
            {
                'message': 'Token is required',
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not user_id:
       return Response(
            {
                'message': 'User id is required',
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    url = "http://stack-overflow-authen-authenticator-1:8000" + "/api/check-user"
    params = {'user_id': user_id}

    try:
        response = requests.get(url, params=params)
        if (response.status_code == 200):
            res = response.json()
            if (res["message"] == True):
                token = DeviceToken.objects.get_or_create(user_id=user_id, token=token)
                return Response(
                    {
                        'message': 'Create device token success'
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'message': 'User not found',
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
    except Exception as e:
        return Response(
            {
                'message': 'Internal server error',
                'error': f'{e}'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )