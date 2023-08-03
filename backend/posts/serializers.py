from rest_framework import serializers
from posts import models
from home.api.v1.serializers import UserSerializer
from core.utils import get_file_path


class PostCommentSerializer(serializers.ModelSerializer):
    parent_id = serializers.CharField(required=False)
    user = UserSerializer(required=False)
    likes = serializers.SerializerMethodField()

    def get_likes(self, obj):
        try:
            queryset = models.CommentLike.objects.filter(comment=obj)
            data = UserSerializer([q.user for q in queryset], many=True).data
            return data
        except Exception as e:
            print(e)
            return 0

    class Meta:
        model = models.PostComment
        fields = '__all__'

    def create(self, validated_data):
        user = self.context["request"].user
        if "parent_id" in validated_data:
            parent = models.PostComment.objects.filter(
                id=validated_data.pop("parent_id"))
            if parent.exists():
                parent = parent.first()
            else:
                parent = None
            validated_data["parent"] = parent
            validated_data['user'] = user
        post_comment = models.PostComment.objects.create(**validated_data)
        return post_comment


class PostLikeSerializerGET(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.PostLike
        fields = '__all__'


class PostLikeSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = models.PostLike
        exclude = ('user',)

    def create(self, validated_data):
        user = self.context['request'].user
        like = models.PostLike.objects.filter(post=validated_data['post'], user=user)
        if like.exists():
            like = like.first()    
            like.delete()
            res = serializers.ValidationError({'message':'Unliked'})
            res.status_code = 200
            raise res
        validated_data['user'] = user
        post_like = models.PostLike.objects.create(**validated_data)
        return post_like


class CommentLikeSerializerGET(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.CommentLike
        fields = '__all__'


class CommentLikeSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = models.CommentLike
        exclude = ('user',)

    def create(self, validated_data):
        user = self.context['request'].user
        if models.CommentLike.objects.filter(comment=validated_data['comment'], user=user).exists():
            raise serializers.ValidationError("Already Liked by User")
        validated_data['user'] = user
        comment_like = models.CommentLike.objects.create(**validated_data)
        return comment_like


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    reactions = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    original_post = serializers.SerializerMethodField()

    def get_original_post(self,obj):
        if obj.original_post:
            return PostSerializer(obj.original_post).data
        else:
            return None
        
    def get_reactions(self, obj):
        try:
            queryset = models.PostLike.objects.filter(post=obj)
            data = UserSerializer([q.user for q in queryset], many=True).data
            return data
        except Exception as e:
            print(e)
            return None

    def get_comments(self, obj):
        try:
            queryset = models.PostComment.objects.filter(post=obj)
            return PostCommentSerializer(queryset, many=True).data
        except Exception as e:
            print(e)
            return None

    class Meta:
        model = models.Post
        fields = '__all__'


class FlagPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FlagPost
        exclude = ('user',)


class ChatImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChatImage
        exclude = ('user',)