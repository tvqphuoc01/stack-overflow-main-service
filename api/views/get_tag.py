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
    
    