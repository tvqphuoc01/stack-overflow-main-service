from django.urls import path
from api.views.get_question import get_question_by_id, get_first_ten_question, update_question_status
from api.views.get_category import get_list_category
from api.views.get_tag import get_list_tag

urlpatterns = [
    path('update-question-status', update_question_status, name='update_question_status'),
    path('get-question-by-id', get_question_by_id, name='get_question_by_id'),
    path('get-first-ten-question', get_first_ten_question, name='get_first_ten_question'),
    path('get-list-category', get_list_category, name='get_list_category'),
    path('get-list-tag', get_list_tag, name='get_list_tag'),
]