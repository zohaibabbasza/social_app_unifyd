from rest_framework import serializers
from poll import models
from home.api.v1.serializers import UserSerializer

class PollSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = models.Poll
        exclude = ('user',)

    def create(self,validated_data):
        user = self.context['request'].user
        poll = models.Poll.objects.filter(user = user, post = validated_data['post'])
        if poll.exists():
            poll = poll.first()
            if not poll.post.is_multiple_poll:
                poll.text = validated_data['text']
                poll.name = validated_data['name']
                poll.save()
        else:
            poll = models.Poll.objects.create(**validated_data)
        return poll
    
class PollSerializerGET(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = models.Poll
        fields = '__all__'

