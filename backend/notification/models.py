from django.db import models
from django.contrib.postgres.fields import JSONField
from users.models import User

class Notification(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(max_length=255)
    data = JSONField(null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    sent_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_sent_by',null=True)
    is_read = models.BooleanField(default=False)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self) -> str:
        return self.title