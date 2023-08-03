from rest_framework import serializers
from chat import models
from home.api.v1.serializers import UserSerializer

class ChatSerializerGET(serializers.ModelSerializer):
    user = UserSerializer()
    to_user = UserSerializer()

    class Meta:
        model = models.Chat
        fields = '__all__'

class ChatSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = models.Chat
        exclude = ('user',)

    def create(self, validated_data):
        user = self.context['request'].user
        to_user = validated_data['to_user']
        if to_user.is_private:
            models.ChatRequest.objects.create(
                models.ChatRequest.objects.create(user = to_user,from_user=user)

            )
            return serializers.ValidationError("Follow Request has been sent")
        chat = models.Chat.objects.filter(to_user=to_user,user=user)
        if chat.exists():
            return chat.first()
        chat = models.Chat.objects.create(**validated_data)
        return chat

class ChatRequestGET(serializers.ModelSerializer):
    from_user = UserSerializer()
    user = UserSerializer()
    class Meta:
        model = models.ChatRequest
        fields = '__all__'

class ChatRequestPOST(serializers.ModelSerializer):
    
    class Meta:
        model = models.ChatRequest
        exclude = ('from_user',)