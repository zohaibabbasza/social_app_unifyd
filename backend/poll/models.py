from django.db import models
from users.models import User
from posts.models import Post

class Poll(models.Model):
    name = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

        