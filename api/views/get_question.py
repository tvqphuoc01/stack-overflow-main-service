from api.models import Question, Answer
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
    tag_id = validated_data.get('tag_id')
    category_id = validated_data.get('category_id')
    user_id = validated_data.get('user_id')

    url = "http://stack-overflow-authen-authenticator-1:8006" + "/api/check-user"
    params = {'user_id': user_id}

    try:
        response = requests.get(url, params=params)
        # response.raise_for_status()  # Raise an exception for non-2xx status codes
        res = response.json()
        print(res)
    except requests.exceptions.RequestException as e:
        return Response(
            {
                'message': f'Error: {e}'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        question, created = Question.objects.get_or_create(title=name, content=content)
        if created == False:
            return Response(
                {
                    'message': 'Create question failed'
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