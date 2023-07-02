from api.models import Tag

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_list_tag(request):
    list_tag = Tag.objects.all()
    return Response(
        {
            "message": "Get list tag successfully",
            "data": list_tag
        },
        status=status.HTTP_200_OK
    )