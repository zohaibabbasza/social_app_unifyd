from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from core.utils import get_file_path,compress_image
from django.contrib.postgres.fields import JSONField


class User(AbstractUser):
    cover_picture = models.ImageField(upload_to=get_file_path,null=True)
    profile_image = models.ImageField(upload_to=get_file_path,null=True)
    friends = models.ManyToManyField('User', related_name='user_friends',blank=False)
    blocked = models.ManyToManyField('User', related_name='user_blocked',blank=False)
    followers = models.ManyToManyField('User',related_name='users_followers',blank=True)
    following = models.ManyToManyField('User',related_name='users_following',blank=True)
    is_private = models.BooleanField(default=False)
    zip_code = models.CharField(max_length=10,null=True)
    location = models.CharField(max_length=255,null=True)
    date_of_birth = models.DateField(null=True)
    longitude = models.FloatField(null=True,blank=True)
    latitude = models.FloatField(null=True,blank=True)
    is_email_verified = models.BooleanField(default=False)
    profile_progress = models.CharField(max_length=255,null=True, blank=True)
    bio = models.TextField(null=True)
    walkthrough = JSONField(null=True,blank=True)
    display_name = models.CharField(max_length=255,null=True, blank=True)
    is_first_login = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.profile_image:
            if self.profile_image.size > (300 * 1024):
                new_image = compress_image(self.profile_image)
                self.profile_image = new_image
        if self.cover_picture:
            if self.cover_picture.size > (300 * 1024):
                new_image = compress_image(self.cover_picture)
                self.cover_picture = new_image

        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

class Preference(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    is_like_profile = models.BooleanField(default=True)
    is_hide_birthday = models.BooleanField(default=False)
    who_can_see_profile = models.CharField(max_length=255,default='Public')
    is_online_status = models.BooleanField(default=True)
    timezone = models.CharField(max_length=255,null=True)
    is_enable_chat = models.BooleanField(default=True)
    allow_new_message_friends = models.BooleanField(default=True)
    first_name = models.BooleanField(default=True)
    last_name = models.BooleanField(default=True)
    bio = models.BooleanField(default=True)
    is_date_of_birth = models.BooleanField(default=True)
    is_location = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.user.email

class NotificationPreference(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    post_comment = models.BooleanField(default=True)
    post_reaction = models.BooleanField(default=True)
    comment_reaction = models.BooleanField(default=True)
    comment_reply = models.BooleanField(default=True)
    share_post = models.BooleanField(default=True)
    liked_my_profile = models.BooleanField(default=True)
    mention = models.BooleanField(default=True)
    new_message = models.BooleanField(default=True)
    friend_request = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.user.email

class EmailTokenVerification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    token = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.user.email

class PasswordReset(EmailTokenVerification):
    pass


class ReportUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    reported_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='reported_user')


class FriendRequests(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    sent_by = models.ForeignKey('User',on_delete=models.CASCADE,related_name='sent_by')

class FriendSuggestion(models.Model):
    suggestions = models.ManyToManyField(User, related_name='user_suggestions')
    
class FCMDevices(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    fcm_token = models.CharField(max_length=255,unique=True)

    def __str__(self) -> str:
        return self.user.email


