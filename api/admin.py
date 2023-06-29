from django.contrib import admin
from .models import Category, Tag, Question, QuestionCategory, QuestionTag, Answer, QuestionUser, Reply, ReplyUser, AnswerUser, Notification
# Register your models here.

# generate admin site for all models
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(QuestionCategory)
admin.site.register(QuestionTag)
admin.site.register(Answer)
admin.site.register(QuestionUser)
admin.site.register(Reply)
admin.site.register(ReplyUser)
admin.site.register(AnswerUser)
admin.site.register(Notification)