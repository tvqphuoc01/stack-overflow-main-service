import requests
from api.models import Reply, ReplyUser

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers.reply_serializers import ReplySerializer, ReplyResponseDataSerializer, ReplyLikeSerializer
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger

@api_view(["POST"])
def create_reply(request):
    serializer = ReplySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data

    # answer data
    owner_id = validated_data.get('owner_id')
    answer = validated_data.get('answer')
    content = validated_data.get('content')
    image_url = validated_data.get('image_url', '')
    
    url = "http://stack-overflow-authen-authenticator-1:8000" + "/api/check-user"
    params = {'user_id': owner_id}

    response = requests.get(url, params=params)
    if (response.status_code == 200):
        res = response.json()
        if (res["message"] == True):
            try:
                reply, created = Reply.objects.get_or_create(owner_id=owner_id, question_id=answer.question_id, answer_id=answer, content=content, image_url=image_url)
                if created == False:
                    return Response(
                        {
                            'message': 'Create reply failed'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(
                    {
                        'message': 'Reply created'
                    }
                )
            except Exception as e:
                return Response(
                    {
                        'message': 'Internal server error',
                        'error': f'{e}'
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
    return Response(
            {
                'message': 'User not found',
            },
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(["GET"])
def get_reply_by_answer_id(request):
    answer_id = request.GET.get('answer_id')
    if not answer_id:
        return Response(
            {
                "message": "Answer id is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
    reply = Reply.objects.filter(answer_id=answer_id, answer_status=True).all()
    
    reply_data = []
    
    for rep in reply:
        authen_url = "http://stack-overflow-authen-authenticator-1:8000/api/get-user-by-id"
        response = requests.get(authen_url, params={"user_id": rep.owner_id})
        
        if response.status_code != 200:
            return Response(
                {
                    "message": "Get user info failed",
                    "data": reply_data
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        reply_like = ReplyUser.objects.filter(reply_id=rep.reply_id, is_like=True)
        reply_dislike = ReplyUser.objects.filter(reply_id=rep.reply_id, is_like=False)
        reply_data.append({
            "id": rep.reply_id,
            "user_data": response.json(),
            "content": rep.content,
            "number_of_like": len(reply_like),
            "number_of_dislike": len(reply_dislike),
            "create_date": rep.create_date,
        })
        
    return Response(
        {
            "message": "Get reply successfully",
            "data": reply_data
        },
        status=status.HTTP_200_OK
    )

@api_view(["GET"])
def get_reply_by_question_id(request):
    question_id = request.GET.get('question_id')
    if not question_id:
        return Response(
            {
                "message": "Question id is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
    reply = Reply.objects.filter(question_id=question_id, answer_status=True).all()
    
    reply_data = []
    
    for rep in reply:
        authen_url = "http://stack-overflow-authen-authenticator-1:8000/api/get-user-by-id"
        response = requests.get(authen_url, params={"user_id": rep.owner_id})
        
        if response.status_code != 200:
            return Response(
                {
                    "message": "Get user info failed",
                    "data": reply_data
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        reply_data.append({
            "id": rep.reply_id,
            "user_data": response.json(),
            "content": rep.content,
            "number_of_like": rep.number_of_like,
            "number_of_dislike": rep.number_of_dislike,
            "create_date": rep.create_date,
            "answer_id": rep.answer_id.id
        })
        
    return Response(
        {
            "message": "Get reply successfully",
            "data": reply_data
        },
        status=status.HTTP_200_OK
    )

@api_view(["POST"])
def create_reply_like(request):
    # check request data is valid
    serializer = ReplyLikeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data

    # reply like data
    reply = validated_data.get('reply')
    user_id = validated_data.get('user_id')
    is_like = request.data.get('is_like')
    print(user_id)

    url = "http://stack-overflow-authen-authenticator-1:8000" + "/api/check-user"
    params = {'user_id': user_id}

    response = requests.get(url, params=params)
    res = response.json()
    print(res)
    if (response.status_code == 200):
        if (res["message"] == True):
            try:
                reply_like = ReplyUser.objects.filter(reply_id=reply , user_id=user_id).first()
                if reply_like:
                    reply_like.is_like = is_like
                    reply_like.save()
                else:
                    reply_like = ReplyUser.objects.create(reply_id=reply, user_id=user_id, is_like=is_like)
                if is_like:
                    return Response(
                        {
                            'message': 'Like reply success'
                        }
                    )
                return Response(
                    {
                        'message': 'Dislike reply success'
                    }
                )
            except Exception as e:
                return Response(
                    {
                        'message': 'Internal server error',
                        'error': f'{e}'
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
    return Response(
            {
                'message': 'User not found',
            },
    )

@api_view(['PUT'])
def update_reply_status(request):
    reply_id = request.data.get('reply_id')
    answer_status = request.data.get('answer_status')
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
    if not reply_id:
        return Response(
            {
                "message": "Reply id is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
    reply = Reply.objects.filter(reply_id=reply_id).first()
    if not reply:
        return Response(
            {
                "message": "Reply is not available"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    if answer_status:
        reply.answer_status = answer_status
        reply.save()
    return Response(
        {
            "message": "Update answer successfully",
        },
        status=status.HTTP_200_OK
    )

@api_view(['DELETE'])
def delete_reply(request):
    reply_id = request.data.get('reply_id')
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
    
    if not reply_id:
        return Response(
            {
                "message": "Reply id is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
    reply = Reply.objects.filter(reply_id=reply_id).first()
    if not reply:
        return Response(
            {
                "message": "Reply is not available"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    reply.delete()
    return Response(
        {
            "message": "Delete reply successfully",
        },
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
def get_all_replies_for_admin(request):
    requester_id = request.GET.get('requester_id')
    
    if not requester_id:
        return Response(
            {
                "message": 'Requester id is required'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # check requester role
    # check if requestor is admin
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
        
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    reply = Reply.objects.order_by("-create_date").all()
    paginator = Paginator(reply, limit)
    
    try:
        reply = paginator.page(page)
        serialized_reply = ReplyResponseDataSerializer(reply, many=True)
        
        return Response(
            {
                "message": "Get all replies successfully",
                "data": {
                    "total_pages": paginator.num_pages,
                    "total_records": paginator.count,
                    "data": serialized_reply.data,
                }
            },
            status=status.HTTP_200_OK
        )
    except PageNotAnInteger:
        return Response(
            {
                "message": "Page not an integer"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    except EmptyPage:
        return Response(
            {
                "message": "Empty page"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {
                "message": "Internal server error",
                "error": f"{e}"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_reply_like_by_user_id(request):
    user_id = request.GET.get("user_id")
    reply_id= request.GET.get("reply_id")

    if not user_id:
        return Response(
            {
                'message': 'User id is required',
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not reply_id:
        return Response(
            {
                'message': 'Reply id is required',
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    authen_url = "http://stack-overflow-authen-authenticator-1:8000/api/check-user"
    response = requests.get(authen_url, params={"user_id": user_id})

    if (response.status_code == 200):
        res = response.json()
        if (res["message"] == True):
            replyUser = ReplyUser.objects.filter(reply_id=reply_id, user_id=user_id).first()
            if replyUser:
                return Response(
                    {
                        'message': 'Get reply like success',
                        'data': replyUser.is_like
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                    {
                        'message': 'Get reply like success',
                        'data': None
                    },
                    status=status.HTTP_200_OK
                )
    return Response(
            {
                'message': 'User not found',
            },
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
def get_reply_by_id(request):
    reply_id = request.GET.get('reply_id')

    if not reply_id:
        return Response(
            {
                "message": "Reply id is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
    reply = Reply.objects.filter(reply_id=reply_id).first()
    reply_like = ReplyUser.objects.filter(reply_id=reply_id, is_like=True)
    reply_dislike = ReplyUser.objects.filter(reply_id=reply_id, is_like=False)

    if not reply:
        return Response(
            {
                "message": "Reply is not available"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    authen_url = "http://stack-overflow-authen-authenticator-1:8000/api/get-user-by-id"
    response = requests.get(authen_url, params={"user_id": reply.owner_id})
    user_data = response.json()
    return Response(
        {
            "message": "Get reply successfully",
            "data": {
                "id": reply.reply_id,
                "user_id": reply.owner_id,
                "content": reply.content,
                "number_of_like": len(reply_like),
                "number_of_dislike": len(reply_dislike),
                "image_url": reply.image_url,
                "create_date": reply.create_date,
                "user_data": user_data
            }
        },
        status=status.HTTP_200_OK
    )