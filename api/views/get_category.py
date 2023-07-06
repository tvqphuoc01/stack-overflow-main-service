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

@api_view(['POST'])
def create_category(request):
    category_name = request.data.get('category_name')
    if not category_name:
        return Response(
            {
                "message": "Category name is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    category, created = Category.objects.get_or_create(name=category_name)
    if created == False:
        return Response(
            {
                "message": "Category already created"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    else:
        return Response(
            {
                "message": "Category created"
            },
            status=status.HTTP_201_CREATED
        )