from api.models import Category

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_list_category(request):
    list_category = Category.objects.all()
    return Response(
        {
            "message": "Get list category successfully",
            "data": list_category
        },
        status=status.HTTP_200_OK
    )