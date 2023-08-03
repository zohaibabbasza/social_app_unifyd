from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q
from chat import serializers,models

class ChatModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ChatSerializerGET
        if self.action == 'retrieve':
            return serializers.ChatSerializerGET
        return serializers.ChatSerializerPOST

    def get_queryset(self):
       return models.Chat.objects.filter(Q(user=self.request.user) | 
                            Q(to_user=self.request.user)).distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ChatRequestViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.ChatRequest.objects.filter(Q(user=self.request.user) | 
                            Q(from_user=self.request.user)).distinct()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ChatRequestGET
        if self.action == 'retrieve':
            return serializers.ChatRequestGET
        return serializers.ChatRequestPOST
    
    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)