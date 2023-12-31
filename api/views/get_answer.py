import requests
from api.models import Answer, AnswerUser, Reply

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers.answer_serializers import AnswerSerializer, AnswerResponseDataSerializer, AnswerLikeSerializer
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger

@api_view(['GET'])
def get_answer_of_question_by_id(request):
    question_id = request.GET.get('question_id')
    requester_id = request.GET.get('requester_id')

    if not question_id:
        return Response(
            {
                "message": "Question id is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    authen_url = "http://stack-overflow-authen-authenticator-1:8000/api/get-user-by-id"
    response = requests.get(authen_url, params={"user_id": requester_id})
    
    answer = []
    if response.status_code == 200:
        result_body = response.json()
        user = result_body["data"]
        if (user["role"] == "ADMIN"):
            answer = Answer.objects.filter(question_id=question_id).order_by("-create_date").all()
        else:
            answer = Answer.objects.filter(question_id=question_id, answer_status=1).order_by("-create_date").all()
    else:
        answer = Answer.objects.filter(question_id=question_id, answer_status=1).order_by("-create_date").all()

    answer_data = []

    for ans in answer:
        response = requests.get(authen_url, params={"user_id": ans.user_id})
        
        if response.status_code != 200:
            return Response(
                {
                    "message": "Get user info failed",
                    "data": answer_data
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        answer_like = AnswerUser.objects.filter(answer_id=ans.id, is_like=True)
        answer_dislike = AnswerUser.objects.filter(answer_id=ans.id, is_like=False)
        answer_data.append({
            "id": ans.id,
            "user_data": response.json(),
            "content": ans.content,
            "number_of_like": len(answer_like),
            "number_of_dislike": len(answer_dislike),
            "create_date": ans.create_date,
            "image_url": ans.image_url
        })
    return Response(
        {
            "message": "Get answer successfully",
            "data": answer_data
        },
        status=status.HTTP_200_OK
    )

@api_view(["POST"])
def create_answer(request):
    serializer = AnswerSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data

    # answer data
    user_id = validated_data.get('user_id')
    image_url = validated_data.get('image_url', '')
    content = validated_data.get('content')
    question_id = validated_data.get('question_id')

    url = "http://stack-overflow-authen-authenticator-1:8000" + "/api/check-user"
    params = {'user_id': user_id}

    response = requests.get(url, params=params)
    if (response.status_code == 200):
        res = response.json()
        if (res["message"] == True):
            try:
                answer, created = Answer.objects.get_or_create(question_id=question_id, content=content, user_id=user_id, image_url=image_url)
                if created == False:
                    return Response(
                        {
                            'message': 'Create answer failed'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(
                    {
                        'message': 'Answer created'
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

@api_view(["POST"])
def create_answer_like(request):
    # check request data is valid
    serializer = AnswerLikeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data

    # answer like data
    answer = validated_data.get('answer')
    user_id = validated_data.get('user_id')
    is_like = request.data.get('is_like')

    url = "http://stack-overflow-authen-authenticator-1:8000" + "/api/check-user"
    params = {'user_id': user_id}

    response = requests.get(url, params=params)
    res = response.json()
    if (response.status_code == 200):
        if (res["message"] == True):
            try:
                answer_like = AnswerUser.objects.filter(answer_id=answer , user_id=user_id).first()
                if answer_like:
                    answer_like.is_like = is_like
                    answer_like.save()
                else:
                    answer_like = AnswerUser.objects.create(answer_id=answer, user_id=user_id, is_like=is_like)
                if is_like:
                    return Response(
                        {
                            'message': 'Like answer success'
                        }
                    )
                return Response(
                    {
                        'message': 'Dislike answer success'
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
def update_answer_status(request):
    answer_id = request.data.get('answer_id')
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
    if not answer_id:
        return Response(
            {
                "message": "Answer id is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
    answer = Answer.objects.filter(id=answer_id).first()
    if not answer:
        return Response(
            {
                "message": "Answer is not available"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    if answer_status:
        answer.answer_status = answer_status
        answer.save()
    return Response(
        {
            "message": "Update answer successfully",
        },
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
def get_answer_by_id(request):
    answer_id = request.GET.get('answer_id')

    if not answer_id:
        return Response(
            {
                "message": "Answer id is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
    answer = Answer.objects.filter(id=answer_id).first()
    answer_like = AnswerUser.objects.filter(answer_id=answer_id, is_like=True)
    answer_dislike = AnswerUser.objects.filter(answer_id=answer_id, is_like=False)

    if not answer:
        return Response(
            {
                "message": "Answer is not available"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    authen_url = "http://stack-overflow-authen-authenticator-1:8000/api/get-user-by-id"
    response = requests.get(authen_url, params={"user_id": answer.user_id})
    user_data = response.json()
    return Response(
        {
            "message": "Get answer successfully",
            "data": {
                "id": answer.id,
                "user_id": answer.user_id,
                "content": answer.content,
                "number_of_like": len(answer_like),
                "number_of_dislike": len(answer_dislike),
                "image_url": answer.image_url,
                "create_date": answer.create_date,
                "user_data": user_data
            }
        },
        status=status.HTTP_200_OK
    )

@api_view(['DELETE'])
def delete_answer(request):
    answer_id = request.data.get('answer_id')
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
    
    if not answer_id:
        return Response(
            {
                "message": "Answer id is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
    answer = Answer.objects.filter(id=answer_id).first()
    if not answer:
        return Response(
            {
                "message": "Answer is not available"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    answer.delete()
    return Response(
        {
            "message": "Delete answer successfully",
        },
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
def get_answer_by_user_id(request):
    user_id = request.GET.get("user_id")

    if not user_id:
        return Response(
            {
                'message': 'User id is required',
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    authen_url = "http://stack-overflow-authen-authenticator-1:8000/api/check-user"
    response = requests.get(authen_url, params={"user_id": user_id})
    
    if (response.status_code == 200):
        res = response.json()
        if (res["message"] == True):
            reply_objs = Reply.objects.filter(owner_id=user_id).all()
            answer_objs = Answer.objects.filter(user_id=user_id).all()
            answer_list_data = []
            for answer in answer_objs:
                answer_list_data.append(
                    {
                        "id": answer.id,
                        "content": answer.content,
                        "number_of_like": answer.number_of_like,
                        "number_of_dislike": answer.number_of_dislike,
                        "image_url": answer.image_url,
                        "create_date": answer.create_date,
                        "status": answer.answer_status
                    }
                )

            for reply in reply_objs:
                answer_list_data.append(
                    {
                        "id": reply.reply_id,
                        "content": reply.content,
                        "number_of_like": reply.number_of_like,
                        "number_of_dislike": reply.number_of_dislike,
                        "image_url": reply.image_url,
                        "create_date": reply.create_date,
                        "status": reply.answer_status
                    }
                )

            return Response(
                {
                    "message": "Get answer successfully",
                    "data": answer_list_data
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
def get_all_answer_for_admin(request):
    requester_id = request.GET.get("requestor_id")
    
    if not requester_id:
        return Response(
            {
                "message": 'Requester id is required'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
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
    
    # Pagination
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)

    answer_objs = Answer.objects.order_by("-create_date").all()
    paginator = Paginator(answer_objs, page_size)
    total = paginator.count
    
    try:
        answers = paginator.page(page_number)

        serialized_answers = AnswerResponseDataSerializer(
            answers, many=True)
        return Response(
            {
                "message": "Get answers successfully",
                "data": {
                    "total_pages": paginator.num_pages,
                    "answers": serialized_answers.data,
                    "current_page": answers.number,
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
                "message": "Get answers failed",
                "error": f"{e}"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_answer_like_by_user_id(request):
    user_id = request.GET.get("user_id")
    answer_id= request.GET.get("answer_id")

    if not user_id:
        return Response(
            {
                'message': 'User id is required',
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not answer_id:
        return Response(
            {
                'message': 'Answer id is required',
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    authen_url = "http://stack-overflow-authen-authenticator-1:8000/api/check-user"
    response = requests.get(authen_url, params={"user_id": user_id})

    if (response.status_code == 200):
        res = response.json()
        if (res["message"] == True):
            answerUser = AnswerUser.objects.filter(answer_id=answer_id, user_id=user_id).first()
            if answerUser:
                return Response(
                    {
                        'message': 'Get answer like success',
                        'data': answerUser.is_like
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                    {
                        'message': 'Get answer like success',
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
    