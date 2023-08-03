from django.db import models
from core.utils import get_file_path,compress_image
from posts.models import Post
from users.views import User

GROUP_CHOICES = (
    ('Open','Open'),
    ('Close','Close')
)
GROUP_NOTIFICATION_CHOICES = (
    ('Follow','Follow'),
    ('Be Notified','Be Notified'),
    ('Receive Email','Receive Email'),
)

class GroupCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class Tags(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    picture = models.ImageField(upload_to=get_file_path)
    cover_photo = models.ImageField(upload_to=get_file_path,null=True,blank=True)
    tags = models.ManyToManyField(Tags,null=True)
    date = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User,null=True,related_name='group_members')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
            if self.picture:
                if self.picture.size > (300 * 1024):
                    new_image = compress_image(self.picture)
                    self.picture = new_image
            if self.cover_photo:
                if self.cover_photo.size > (300 * 1024):
                    new_image = compress_image(self.cover_photo)
                    self.cover_photo = new_image

            super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

class GroupPost(models.Model):
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)

class GroupNotification(models.Model):
    group_notification = models.CharField(max_length=255,null=True,blank=True,choices=GROUP_NOTIFICATION_CHOICES)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
