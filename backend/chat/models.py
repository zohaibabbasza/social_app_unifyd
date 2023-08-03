from django.db import models
from users.models import User


class Chat(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='to_user')

class ChatRequest(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    from_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='chat_from_user')
    is_accepted = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)