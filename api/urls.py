from django.urls import path
from api.views.get_question import get_question_by_id, get_list_question, update_question_status, delete_question, get_top_three_question, create_question, create_question_like
from api.views.get_category import get_list_category, create_category
from api.views.get_tag import get_list_tag, create_tag, delete_tag, get_top_five_tag
from api.views.notification import send_notification, get_user_notification
from api.views.get_answer import get_answer_of_question_by_id, create_answer
from api.views.get_user import get_top_user
from api.views.reply import create_reply, create_reply_like, get_reply_by_answer_id, get_reply_by_question_id

urlpatterns = [
    path('update-question-status', update_question_status, name='update_question_status'),
    path('delete-question', delete_question, name='delete_question'),
    path('get-question-by-id', get_question_by_id, name='get_question_by_id'),
    path('get-list-question', get_list_question, name='get_list_question'),
    path('get-list-category', get_list_category, name='get_list_category'),
    path('get-list-tag', get_list_tag, name='get_list_tag'),
    path('send-notification', send_notification, name='send_notification'),
    path('get-user-notification', get_user_notification, name='get_user_notification'),
    path('create-tag', create_tag, name='create_tag'),
    # path('add-tag', add_tag, name='add_tag'),
    path('delete-tag', delete_tag, name='delete_tag'),
    path('create-category', create_category, name='create_category'),
    path('get-top-three-question', get_top_three_question, name= 'get_top_three_question'),
    path('get-top-five-tag', get_top_five_tag, name='get_top_five_tag'),
    path('create-question', create_question, name='create_question'),
    path('get-answer-of-question-by-id', get_answer_of_question_by_id, name='get_answer_of_question_by_id'),
    path('get-top-user', get_top_user, name="get_top_user"),
    path('create-answer', create_answer, name='create_answer'),
    path('create-reply', create_reply, name='create_reply'),
    path('create-question-like', create_question_like, name='create_question_like'),
    path('create-reply-like', create_reply_like, name='create_reply_like'),
    path('get-reply-by-answer-id', get_reply_by_answer_id, name='get_reply_by_answer_id'),
    path('get-reply-by-question-id', get_reply_by_question_id, name='get_reply_by_question_id')
]