from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import TokenAuthentication
from notification import serializers,models


class NotificationModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.NotificationSerializer
    http_method_names = ['get']

    def get_queryset(self):
        return models.Notification.objects.filter(user=self.request.user)
