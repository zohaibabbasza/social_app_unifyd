import uuid
from users.models import User,FCMDevices
from django.db import models
from core.utils import get_file_path,send_push_notification
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver
from notification.models import Notification
from core.utils import compress_image

POST_TYPE = (
    ('Friends Only','Friends Only'),
    ('Everyone','Everyone'),
)

POST_SCHEDULE = (
    ('6 hours', '6 hours'),
    ('12 hours','12 hours'),
    ('24 hours','24 hours'),
)
POST_COMMUNITY = (
    ('Everyone', 'Everyone'),
    ('Following','Following')
)

class Post(models.Model):
    text = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    images = models.FileField(upload_to=get_file_path,null=True,blank=True)
    created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customization = JSONField(null=True,blank=True)
    original_post = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        blank=True,
        related_name="post_original",
    )
    video_file = models.FileField(upload_to=get_file_path,null=True)
    is_group_post = models.BooleanField(default=False)
    is_poll = models.BooleanField(default=False)
    is_multiple_poll = models.BooleanField(default=False)
    type = models.CharField(max_length=255,choices=POST_TYPE,null=True)
    community = models.CharField(max_length=255,choices=POST_COMMUNITY,null=True)
    shared_by = models.ManyToManyField(User,related_name='user_shared_by',null=True,blank=True)
    share_link = models.UUIDField(default=uuid.uuid4, editable=False)
    share_count  = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)
    scheduled_for = models.DateTimeField(null=True,blank=True)

    def save(self, *args, **kwargs):
        if self.images:
            if self.images.size > (300 * 1024):
                new_image = compress_image(self.images)
                self.images = new_image
                # save
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.text + ' | ' + self.user.email

class PostComment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    comment = models.TextField()
    image = models.FileField(upload_to=get_file_path,null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        blank=True,
        related_name="parent_comment",
    )
    date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.image:
            if self.image.size > (300 * 1024):
                new_image = compress_image(self.image)
                self.image = new_image
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.post.id) + ' | ' + self.user.email

class CommentLike(models.Model):
    comment = models.ForeignKey(PostComment,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)    

    def __str__(self) -> str:
        return str(self.comment.id) + ' | ' + self.user.email
class PostLike(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.post.id) + ' | ' + self.user.email

class FlagPost(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    reason = models.TextField()
    reason_type = models.CharField(max_length=255,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.post.id) + ' | ' + self.reason
    
class ChatImage(models.Model):
    image = models.ImageField(upload_to=get_file_path,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.image:
            if self.image.size > (300 * 1024):
                new_image = compress_image(self.image)
                self.image = new_image
        super().save(*args, **kwargs)


@receiver(post_save, sender=Post)
def post_notification(sender, instance, created, **kwargs):
        if created:
            try:
                user = instance.user
                for u in user.followers.all():
                    title = f'{instance.user.first_name} {instance.user.last_name} has created a post'
                    body = instance.title[:20]
                    Notification.objects.create(post=instance,user=u,sent_by=u, title=title,
                    body = body,data={'postId': instance.id,'routerName': 'post','userid': user.id})
                    fcm_token = FCMDevices.objects.filter(user__in=u)
                    if fcm_token.exists():
                        for token in fcm_token:
                            send_push_notification([token.fcm_token],title,body)
            except Exception as e:
                print(e)


@receiver(post_save, sender=PostLike)
def like_notification(sender, instance, created, **kwargs):
        if created:
            try:
                user = instance.post.user
                title = f'Your post was liked'
                body = f'{instance.user.first_name} {instance.user.last_name}  Liked your post'
                Notification.objects.create(post=instance.post,user=user,sent_by=instance.user, title=title,
                    body = body,data={'postId': instance.post.id,'routerName': 'post','userid': user.id})
                fcm_token = FCMDevices.objects.filter(user__in=user)
                if fcm_token.exists():
                    for token in fcm_token:
                        send_push_notification([token.fcm_token],title,body)
            except Exception as e:
                    print(e)

@receiver(post_save, sender=PostComment)
def comment_notification(sender, instance, created, **kwargs):
        if created:
            try:
                user = instance.post.user
                title = f'Your post was commented on.'
                body = f'{instance.user.first_name} {instance.user.last_name}  commented your post: {instance.comment[:50]}'
                Notification.objects.create(post=instance.post,user=user,sent_by=instance.user ,title=title,
                    body = body,data={'postId': instance.post.id,'routerName': 'post','userid': user.id})
                fcm_token = FCMDevices.objects.filter(user__in=user)
                if fcm_token.exists():
                    for token in fcm_token:
                        send_push_notification([token.fcm_token],title,body)
            except Exception as e:
                print(e)
