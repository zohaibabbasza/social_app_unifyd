from django.contrib import admin
from posts import models

admin.site.register(models.PostLike)
admin.site.register(models.PostComment)
admin.site.register(models.Post)
admin.site.register(models.CommentLike)
admin.site.register(models.FlagPost)