from api.models import Category

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger

@api_view(['GET'])
def get_list_category(request):
    list_category = Category.objects.all()
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    paginator = Paginator(list_category, page_size)
    categories = paginator.page(page_number)
    total = paginator.count

    try:
        
        return_data = []
        for category in categories:
            return_data.append({
                "id": category.category_id,
                "name": category.name
            })
        return Response(
            {
                "message": "Get categories successfully",
                "data": {
                    "total_pages": paginator.num_pages,
                    "categories": return_data,
                    "current_page": categories.number,
                    "total": total
                }
            },
            status=status.HTTP_200_OK
        )
    except PageNotAnInteger:
        return Response(
            {
                "message": "Invalid page number",
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    except EmptyPage:
        return Response(
            {
                "message": "Page out of range",
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {
                "message": "Get categories failed",
                "error": f"{e}"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
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

@api_view(['DELETE'])
def delete_category(request):
    category_id = request.data.get('category_id')
    requester_id = request.data.get('requester_id')

    if not requester_id:
        return Response(
            {
                "message": 'Requester id is required'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    authen_url = "http://stack-overflow-authen-authenticator-1:8000/api/get-user-by-id"
    response = request.get(authen_url, params={"user_id": requester_id})
    
    if response.status_code != 200:
        return Response(
            {
                "message": "Get user info failed",
                "data": {}
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    result_body = response.json()
    user = result_body["data"]
    if (user["role"] != "ADMIN"):
        return Response(
            {
                "message": "Permission denied"
            },
            status=status.HTTP_403_FORBIDDEN
        )
    
    if not category_id:
        return Response(
            {
                "message": "Category id is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    category = Category.objects.filter(id=category_id).first()
    if not category:
        return Response(
            {
                "message": "Category is not available"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    category.delete()
    return Response(
        {
            "message": "Delete category successfully",
        },
        status=status.HTTP_200_OK
    )