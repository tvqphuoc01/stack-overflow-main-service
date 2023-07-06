from django.urls import path
from api.views.get_question import get_question_by_id, get_first_ten_question, update_question_status, delete_question
from api.views.get_category import get_list_category, create_category
from api.views.get_tag import get_list_tag, create_tag, add_tag, delete_tag
from api.views.notification import send_notification, get_user_notification
urlpatterns = [
    path('update-question-status', update_question_status, name='update_question_status'),
    path('delete-question', delete_question, name='delete_question'),
    path('get-question-by-id', get_question_by_id, name='get_question_by_id'),
    path('get-first-ten-question', get_first_ten_question, name='get_first_ten_question'),
    path('get-list-category', get_list_category, name='get_list_category'),
    path('get-list-tag', get_list_tag, name='get_list_tag'),
    path('send-notification', send_notification, name='send_notification'),
    path('get-user-notification', get_user_notification, name='get_user_notification'),
    path('create-tag', create_tag, name='create_tag'),
    path('add-tag', add_tag, name='add_tag'),
    path('delete-tag', delete_tag, name='delete_tag'),
    path('create-category', create_category, name='create_category')
]