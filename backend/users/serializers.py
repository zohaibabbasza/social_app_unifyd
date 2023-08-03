
from rest_framework import serializers
from users import models
from rest_auth.models import TokenModel



class ProfileSerializer(serializers.ModelSerializer):
    follow_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    def get_follow_count(self,obj):
        return obj.followers.all().count()
    
    def get_following_count(self,obj):
        return obj.following.all().count()

    class Meta:
        model = models.User
        fields = ('id','first_name','last_name',
        'email','username','zip_code',
        'location','date_of_birth',
        'profile_image','cover_picture','profile_progress','bio','longitude','latitude','is_first_login',
        'follow_count','following_count')

class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """
    user = ProfileSerializer(many=False, read_only=True)  # this is add by myself.
    class Meta:
        model = TokenModel
        fields = ('key', 'user') 
class ReportUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ReportUser
        exclude = ('added_by',)

class FriendRequestSerializerPOST(serializers.ModelSerializer):

    class Meta:
        model = models.FriendRequests
        exclude = ('sent_by',)

class FriendRequestSerializerGET(serializers.ModelSerializer):
    user = ProfileSerializer()
    sent_by = ProfileSerializer()

    class Meta:
        model = models.FriendRequests
        fields = '__all__'

class PreferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Preference
        exclude = ('user',)
class PreferenceSerializer2(serializers.ModelSerializer):

    class Meta:
        model = models.Preference
        fields = '__all__'
class NotificationPreferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.NotificationPreference
        exclude = ('user',)

class FriendSuggestionSerializerGET(serializers.ModelSerializer):
    suggestions = ProfileSerializer(many=True)
    class Meta:
        model = models.FriendSuggestion
        fields = '__all__'
class FriendSuggestionSerializerPOST(serializers.ModelSerializer):

    class Meta:
        model = models.FriendSuggestion
        fields = '__all__'

class FCMDevicesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.FCMDevices
        exclude = ('user',)