from django.contrib import admin
from groups import models

admin.site.register(models.Group)
admin.site.register(models.GroupCategory)
admin.site.register(models.Tags)