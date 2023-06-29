from django.urls import path
from api.views.get_question import get_question_by_id, get_first_ten_question

urlpatterns = [
    path('get-question-by-id', get_question_by_id, name='get_question_by_id'),
    path('get-first-ten-question', get_first_ten_question, name='get_first_ten_question'),
]