from api.models import Tag, QuestionTag

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
import requests

@api_view(['GET'])
def get_list_tag(request):
    list_tag = Tag.objects.all()
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    paginator = Paginator(list_tag, page_size)
    tags = paginator.page(page_number)
    total = paginator.count
    
    try:
        return_data = []
        for tag in tags:
            return_data.append({
                "id": tag.tag_id,
                "name": tag.name
            })
        return Response(
            {
                "message": "Get tags successfully",
                "data": {
                    "tags": return_data,
                    "current_page": tags.number,
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

@api_view(['PUT'])
def update_tag(request):
    tag_id = request.data.get("tag_id")
    tag_name = request.data.get("tag_name")
    if not tag_id:
        return Response(
            {
                "message": "Tag id is required"
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )
    if not tag_name:
        return Response(
            {
                "message": "Tag name is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    tag = Tag.objects.filter(tag_id=tag_id).first()
    dupTag = Tag.objects.filter(name=tag_name).first()

    if not tag:
        return Response(
            {
                "message": "Tag not found"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    if dupTag:
        return Response(
            {
                "message": "Tag name already used"
            }
        )
    tag.name = tag_name
    tag.save()

    return Response(
        {
            "message": "Update tag successfully"
        },
        status=status.HTTP_200_OK
    )

@api_view(['DELETE'])
def delete_tag(request):
    tag_id = request.data.get("tag_id")
    requester_id = request.data.get('requester_id')

    if not requester_id:
        return Response(
            {
                "message": 'Requester id is required'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    authen_url = "http://stack-overflow-authen-authenticator-1:8000/api/get-user-by-id"
    response = requests.get(authen_url, params={"user_id": requester_id})
    
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

    if not tag_id:
        return Response(
            {
                "message": "Tag id is required"
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )

    tag = Tag.objects.filter(tag_id=tag_id).first()
    if not tag:
        return Response(
            {
                "message": "Tag not found"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    tag.delete()
    return Response(
        {
            "message": "Delete tag successfully",
        },
        status=status.HTTP_200_OK
    )

@api_view(["POST"])
def create_tag(request):
    tag_name = request.data.get('tag_name')
    if not tag_name:
        return Response(
            {
                "message": "Tag name is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    tag, created = Tag.objects.get_or_create(name=tag_name)
    if created == False:
        return Response(
            {
                "message": "Tag already created"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    else:
        return Response(
            {
                "message": "Tag created"
            },
            status=status.HTTP_201_CREATED
        )

@api_view(["GET"])
def get_top_five_tag(request):
    question_tags = QuestionTag.objects.select_related('tag_id').values('tag_id').annotate(tag_count=Count('tag_id')).order_by("tag_count").all()
    list_tag = []
    list_tag_name = []
    for question_tag in question_tags:
        tag = Tag.objects.get(tag_id=question_tag["tag_id"])
        list_tag.append({
            "tag_id": tag.tag_id,
            "tag_name": tag.name
        })
        list_tag_name.append(tag.name)
    total = 5 - len(question_tags)
    tags = Tag.objects.exclude(name__in=list_tag_name).all()[:total]
    for tag in tags:
        list_tag.append({
            "tag_id": tag.tag_id,
            "tag_name": tag.name
        })
    return Response(
        {
            "message": "Get list tag successfully",
            "data": list_tag
        },
        status=status.HTTP_200_OK
    )