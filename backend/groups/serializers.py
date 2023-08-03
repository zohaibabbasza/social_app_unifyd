from rest_framework import serializers
from posts.serializers import PostSerializer
from groups import models
from users.serializers import ProfileSerializer


class GroupCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.GroupCategory
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tags
        fields = '__all__'


class GroupSerializerGET(serializers.ModelSerializer):
    tags = TagSerializer()

    class Meta:
        model = models.GroupCategory
        fields = '__all__'

class GroupSerializerGET(serializers.ModelSerializer):
    tags = TagSerializer()
    members = ProfileSerializer(many=True)

    class Meta:
        model = models.Group
        fields = '__all__'

class GroupSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = models.Group
        extra_kwargs = {'members': {'required': False, "allow_null": True},
                        'picture': {'required': False, "allow_null": True},
                        'tags': {'required': False, "allow_null": True}
                        }
        exclude = ('user',)


class GroupPostSerializerGET(serializers.ModelSerializer):
    group = GroupSerializerGET()
    post = PostSerializer()

    class Meta:
        model = models.GroupPost
        fields = '__all__'

class GroupPostSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = models.GroupPost
        fields = '__all__'

class GroupNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.GroupNotification
        exclude = ('user',)