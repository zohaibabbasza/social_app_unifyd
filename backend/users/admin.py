from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from users import models


admin.site.register(models.User)
admin.site.register(models.PasswordReset)
admin.site.register(models.EmailTokenVerification)
admin.site.register(models.ReportUser)
admin.site.register(models.FriendRequests)
admin.site.register(models.FriendSuggestion)
admin.site.register(models.Preference)
admin.site.register(models.NotificationPreference)