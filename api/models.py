import uuid
from django.db import models

# Create your models here.
class Category(models.Model):
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    
class Tag(models.Model):
    tag_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField()
    title = models.CharField(max_length=1000, default='')
    content = models.TextField(default='')
    number_of_like = models.IntegerField(default=0)
    number_of_dislike = models.IntegerField(default=0)
    question_status = models.IntegerField(default=0)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    image_url = models.CharField(max_length=1000, default='')
    
    def __str__(self):
        return self.title
    
class QuestionCategory(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    
class QuestionTag(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField()
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField(default='')
    number_of_like = models.IntegerField(default=0)
    number_of_dislike = models.IntegerField(default=0)
    answer_status = models.IntegerField(default=0)
    image_url = models.CharField(max_length=1000, default='')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.content
    
class QuestionUser(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_id = models.UUIDField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    is_like = models.BooleanField(default=False)
    is_dislike = models.BooleanField(default=False)
    
    def __str__(self):
        return "User: " + str(self.user_id) + " - Question: " + str(self.question_id) + " - Like: " + str(self.is_like) + " - Dislike: " + str(self.is_dislike)
    
class AnswerUser(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_id = models.UUIDField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    is_like = models.BooleanField(default=False)
    is_dislike = models.BooleanField(default=False)
    
    def __str__(self):
        return "User: " + str(self.user_id) + " - Question: " + str(self.question_id) + " - Like: " + str(self.is_like) + " - Dislike: " + str(self.is_dislike)
    
class Notification(models.Model):
    noti_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    owner_id = models.UUIDField()
    create_date = models.DateTimeField(auto_now_add=True)
    is_checked = models.BooleanField(default=False)
    content = models.TextField(default='')
    
    def __str__(self):
        return "Noti: " + str(self.noti_id) + " - Question: " + str(self.question_id) + " - Owner: " + str(self.owner_id) + " - Checked: " + str(self.is_checked)

class Reply(models.Model):
    reply_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_id = models.ForeignKey(Answer, on_delete=models.CASCADE)
    content = models.TextField(default='')
    number_of_like = models.IntegerField(default=0)
    number_of_dislike = models.IntegerField(default=0)
    answer_status = models.IntegerField(default=0)
    image_url = models.CharField(max_length=1000, default='')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    owner_id = models.UUIDField()
    
    def __str__(self):
        return "Reply: " + str(self.reply_id) + " - Question: " + str(self.question_id) + " - Answer: " + str(self.answer_id) + " - Owner: " + str(self.owner_id) + " - Content: " + str(self.content) + " - Image: " + str(self.image_url) + " - Like: " + str(self.number_of_like) + " - Dislike: " + str(self.number_of_dislike) + " - Status: " + str(self.answer_status) + " - Create: " + str(self.create_date) + " - Update: " + str(self.update_date)

class ReplyUser(models.Model):
    reply_id = models.ForeignKey(Reply, on_delete=models.CASCADE)
    user_id = models.UUIDField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    is_like = models.BooleanField(default=False)
    is_dislike = models.BooleanField(default=False)
    
    def __str__(self):
        return "User: " + str(self.user_id) + " - Question: " + str(self.question_id) + " - Like: " + str(self.is_like) + " - Dislike: " + str(self.is_dislike)
