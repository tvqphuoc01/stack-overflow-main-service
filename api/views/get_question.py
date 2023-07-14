from api.models import Question, Answer, QuestionTag, QuestionCategory
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers.question_serializers import QuestionSerializer
from django.db.models import Count
import os
import requests


@api_view(['GET'])
def get_question_by_id(request):
    question_id = request.GET.get('question_id')
    if not question_id:
        return Response(
            {
                "message": "Question id is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
    question = Question.objects.filter(id=question_id).first()
    if not question:
        return Response(
            {
                "message": "Question is not available"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if question.question_status != True:
        return Response(
            {
                "message": "Question is not available"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(
        {
            "message": "Get question successfully",
            "data": {
                "id": question.id,
                "user_id": question.user_id,
                "title": question.title,
                "content": question.content,
                "number_of_like": question.number_of_like,
                "number_of_dislike": question.number_of_dislike,
                "image_url": question.image_url,
                "create_date": question.create_date,
            }
        },
        status=status.HTTP_200_OK
    )
    
@api_view(['GET'])
def get_first_ten_question(request):
    number_of_page = request.GET.get('page' , 1)
    
    question = Question.objects.filter(question_status=True).order_by('-create_date').all()
    question_list = Paginator(question, 10)
    question_objs = question_list.page(number_of_page)
    
    question_list_data = []
    
    for question in question_objs:
        question_list_data.append(
            {
                "id": question.id,
                "user_id": question.user_id,
                "title": question.title,
                "content": question.content,
                "number_of_like": question.number_of_like,
                "number_of_dislike": question.number_of_dislike,
                "image_url": question.image_url,
                "create_date": question.create_date,
            }
        )
    
    return Response(
        {
            "message": "Get question successfully",
            "data": question_list_data
        },
        status=status.HTTP_200_OK
    )
    
@api_view(['PUT'])
def update_question_status(request):
    question_id = request.data.get('question_id')
    question_status = request.data.get('question_status')
    
    # TODO ADD PERMISSION CHECK
    
    if not question_id:
        return Response(
            {
                "message": "Question id is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
    question = Question.objects.filter(id=question_id).first()
    if not question:
        return Response(
            {
                "message": "Question is not available"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    question.question_status = question_status
    question.save()
    return Response(
        {
            "message": "Update question successfully",
        },
        status=status.HTTP_200_OK
    )
    
@api_view(['DELETE'])
def delete_question(request):
    question_id = request.data.get('question_id')
    
    # TODO ADD PERMISSION CHECK
    
    if not question_id:
        return Response(
            {
                "message": "Question id is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
    question = Question.objects.filter(id=question_id).first()
    if not question:
        return Response(
            {
                "message": "Question is not available"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    question.delete()
    return Response(
        {
            "message": "Delete question successfully",
        },
        status=status.HTTP_200_OK
    )

@api_view(["GET"])
def get_top_three_question(request):
    queryset = Question.objects.annotate(num_answers=Count('answers')).order_by('-num_answers','-create_date','number_of_like').all()[:3]
    question_list_data = []
    for question in queryset:
        question_list_data.append(
            {
                "id": question.id,
                "user_id": question.user_id,
                "title": question.title,
                "content": question.content,
                "number_of_like": question.number_of_like,
                "number_of_dislike": question.number_of_dislike,
                "image_url": question.image_url,
                "create_date": question.create_date,
                "num_answers": question.num_answers,
            }
        )
    return Response(
        {
            "message": "Get question successfully",
            "data": question_list_data
        },
        status=status.HTTP_200_OK
    )

@api_view(["POST"])
def create_question(request):
     # check request data is valid
    serializer = QuestionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data

    # question data
    title = validated_data.get('title')
    content = validated_data.get('content')
    tag = validated_data.get('tag')
    category = validated_data.get('category')
    user_id = validated_data.get('user_id')
    image_url = request.data.get('image_url', '')

    url = "http://stack-overflow-authen-authenticator-1:8000" + "/api/check-user"
    params = {'user_id': user_id}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        res = response.json()
    except requests.exceptions.RequestException as e:
        return Response(
            {
                'message': f'Error: {e}'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    print(res["message"])
    if (res["message"] == True):
        try:
            question, created = Question.objects.get_or_create(title=title, content=content, user_id=user_id, image_url=image_url)
            if created == False:
                return Response(
                    {
                        'message': 'Create question failed'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            question_tag, question_tag_created = QuestionTag.objects.get_or_create(question_id=question, tag_id=tag)
            if question_tag_created == False:
                return Response(
                    {
                        'message': 'Create questionTag failed'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            question_category, question_category_created = QuestionCategory.objects.get_or_create(question_id=question, category_id=category)
            if question_category_created == False:
                return Response(
                    {
                        'message': 'Create questionCategory failed'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {
                    'message': 'Question created'
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
    else: 
        return Response(
                {
                    'message': 'User not found',
                },
                status=status.HTTP_400_BAD_REQUEST
            )