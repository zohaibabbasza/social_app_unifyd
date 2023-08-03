from distutils.command import upload
from re import M
from django.db import models
from groups.models import Group
from users.models import User
from core.utils import get_file_path,compress_image

PRIVACY_CHOICES =(
    ('public', 'public'),
    ('following', 'following'),
    ('only me','only me')
)

class Album(models.Model):
    name = models.CharField(max_length=100)
    privacy = models.CharField(max_length=100,choices=PRIVACY_CHOICES,default='public',null=True)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self) -> str:
        return self.name


class AlbumMedia(models.Model):
    images = models.ImageField(upload_to=get_file_path)
    album = models.ForeignKey(Album,on_delete=models.CASCADE)
    

    def save(self, *args, **kwargs):
        if self.images:
            if self.images.size > (300 * 1024):
                new_image = compress_image(self.images)
                self.images = new_image
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.album.name


class Photo(models.Model):
    image = models.ImageField(upload_to=get_file_path)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

