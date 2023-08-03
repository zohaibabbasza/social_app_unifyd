from rest_framework import serializers
from notification import models
from posts.serializers import PostSerializer
from users.serializers import ProfileSerializer

class NotificationSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    sent_by  = ProfileSerializer()
    class Meta:
        model = models.Notification
        fields = '__all__'