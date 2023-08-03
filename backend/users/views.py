import math
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from core.utils import send_custom_email
from .models import PasswordReset,EmailTokenVerification
from core.utils import generateOTP
from users import serializers,models
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from filters.filters import RelatedOrderingFilter
from core.utils import send_push_notification
from rest_auth.views import LoginView


User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class SendPasswordToken(APIView):
    def post(self,request):
        try:
            email = request.data['email']
            password_reset = PasswordReset.objects.filter(user__email=email)
            if password_reset.exists():
                    password_reset=password_reset.first()
                    send_custom_email(
                    "Password Reset Token",
                    f"Your Token for Password reset is {password_reset.token}",
                    password_reset.user.email)
                    return Response({"message":"Successfully Token sent."},status=status.HTTP_201_CREATED)
            token = generateOTP()
            user= User.objects.filter(email=email)
            if user.exists():
                user = user.first()
                PasswordReset.objects.create(
                    user = user,
                    token =token 
                )
                send_custom_email(
                    "Password Reset Token",
                    f"Your Token for Password reset is {token}",
                    user.email)
                return Response({"message":"Successfully Token sent."},status=status.HTTP_201_CREATED)
            return Response({"message":"User not found."},status=status.HTTP_201_CREATED)
            
        except Exception as e:
             return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

class VerifyPasswordToken(APIView):
    def post(self,request):
        try:
            email = request.data['email']
            token = request.data['token']
            user_verify = PasswordReset.objects.filter(user__email = email)
            if user_verify.exists():
                user_verify = user_verify.first()
                if token == user_verify.token:
                    user = user_verify.user
                    user.set_password(request.data['password'])
                    user.save()
                    user_verify.delete()
                    return Response({"message":"Successfully resetted user password."},status=status.HTTP_201_CREATED)
            return Response({"message":"Wrong Token."},status=status.HTTP_201_CREATED)
            
        except Exception as e:
             return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)


class VerifyUserToken(APIView):
    def post(self,request):
        try:
            email = request.data['email']
            token = request.data['token']
            user_verify = EmailTokenVerification.objects.filter(user__email = email)
            if user_verify.exists():
                user_verify = user_verify.first()
                if token == user_verify.token:
                    user = user_verify.user
                    user.is_email_verified = True
                    user.save()
                    user_verify.delete()
                    token, created = Token.objects.get_or_create(user=user)
                    data = {}
                    data['message'] = "Successfully User Email activated"
                    data['token'] = token.key
                    return Response(data,status=status.HTTP_201_CREATED)
            return Response({"message":"Wrong Token."},status=status.HTTP_201_CREATED)
            
        except Exception as e:
             return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

class ResendUserToken(APIView):
    def post(self,request):
        try:
            email = request.data['email']
            user_verify = EmailTokenVerification.objects.filter(user__email = email)
            if user_verify.exists():
                user_verify = user_verify.first()
                send_custom_email(
                    "Email Verification Token",
                    f"Your Token for Email Verification is {user_verify.token}",
                    user_verify.user.email)
                return Response({"message":"Successfully resend Token"},status=status.HTTP_201_CREATED)
            return Response({"message":"User Doesn't exist"},status=status.HTTP_201_CREATED)
            
        except Exception as e:
             return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)



class ProfileModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['put','get']
    serializer_class = serializers.ProfileSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['email','username','first_name','last_name']
    search_fields = ['email','username','first_name','last_name']

    def get_queryset(self):
        if self.request.method == 'put':
            return User.objects.filter(id=self.request.user.id)
        return User.objects.all().order_by('-id')

    @action(detail=True, url_path="follow", methods=["GET"])
    def follow(self, request, pk):
        try:
            from notification.models import Notification
            user = request.user
            follow_user = self.get_object()
            follow_user.following.add(user)
            user.followers.add(follow_user)
            try:
                title = 'You received a follow request.'
                body = f'{user.first_name} {user.last_name} sent a request'
                Notification.objects.create(user=follow_user, title=title,
                body = body,data={'followId': follow_user.id,'routerName': 'followings','userid': user.id})
                fcm_token = models.FCMDevices.objects.filter(user__in=user)
                if fcm_token.exists():
                    for token in fcm_token:
                        send_push_notification([token.token],title,body)
            except Exception as e:
                print(e)
            return Response('Successfully Followed the User.', status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
      
    @action(detail=True, url_path="unfollow", methods=["GET"])
    def unfollow(self, request, pk):
        try:
            user = request.user
            follow_user = self.get_object()
            user.following.remove(follow_user)
            return Response('Successfully Unfollowed the User.', status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
      
class FriendsModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    serializer_class = serializers.ProfileSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['email','username','first_name','last_name']
    search_fields = ['email','username','first_name','last_name']

    def get_queryset(self):
        return self.request.user.friends.all()

class BlockedUserModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    serializer_class = serializers.ProfileSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['email','username','first_name','last_name']
    search_fields = ['email','username','first_name','last_name']

    def get_queryset(self):
        return self.request.user.blocked.all()

class ReportUserModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']
    serializer_class = serializers.ReportUserSerializer

    def get_queryset(self):
        return models.ReportUser.objects.all()

    def perform_create(self, serializer):
        serializer.save(reported_by=self.request.user)


class AcceptFriendRequest(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            friend_request = models.FriendRequests.objects.get(id=request.data['fr_id'],user=request.user)
            friend_request.user.friends.add(friend_request.sent_by)
            friend_request.sent_by.friends.add(friend_request.user)
            friend_request.delete()
            return Response({"message":"Successfully Friend Request Accepted."},status=status.HTTP_201_CREATED)
            
        except Exception as e:
             return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

class BlockFriend(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            user = request.user
            block_user = User.objects.get(id=request.data['b_id'])
            user.friends.remove(block_user)
            user.blocked.add(block_user)
            user.save()
            return Response({"message":"Successfully Blocked User."},status=status.HTTP_201_CREATED)
            
        except Exception as e:
             return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

class UnBlockFriend(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            user = request.user
            block_user = User.objects.get(id=request.data['b_id'])
            user.blocked.remove(block_user)
            return Response({"message":"Successfully UnBlocked User."},status=status.HTTP_201_CREATED)
            
        except Exception as e:
             return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

class FriendRequestModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['post','get','delete']

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.FriendRequestSerializerGET
        if self.action == 'retrieve':
            return serializers.FriendRequestSerializerGET
        return serializers.FriendRequestSerializerPOST

    def get_queryset(self):
        return models.FriendRequests.objects.filter(Q(user=self.request.user)
         | Q(sent_by=self.request.user))

    def perform_create(self, serializer):
        serializer.save(sent_by=self.request.user)

class GetFollowers(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            user_id = request.GET.get('u_id',None)
            if user_id:
                user = User.objects.get(id=user_id)
            else:
                user = request.user
            user_serializer = serializers.ProfileSerializer(user.followers,many=True).data
            return Response({'followers':user_serializer}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
class GetFollowing(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        try:
            user_id = request.GET.get('u_id',None)
            if user_id:
                user = User.objects.get(id=user_id)
            else:
                user = request.user
            user_serializer = serializers.ProfileSerializer(user.following,many=True).data
            return Response({'following':user_serializer}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            old_password = request.data['old_password']
            new_password1 = request.data['new_password1']
            new_password2 = request.data['new_password2']
            user = request.user
            if not user.check_password(old_password):
                return Response({"message":"Incorrect Password."},status=status.HTTP_201_CREATED)
            if new_password1 != new_password2:
                return Response({"message":"Please put same Password in bot fields."},status=status.HTTP_201_CREATED)
            user.set_password(new_password1)
            user.save()
            return Response({"message":"Successfully Password changed."},status=status.HTTP_201_CREATED)
        except Exception as e:
             return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)



class PreferenceModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['post','put','get']


    def get_queryset(self):
        return models.Preference.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AllPreferenceModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    serializer_class = serializers.PreferenceSerializer2
    filter_backends = [RelatedOrderingFilter,filters.SearchFilter,DjangoFilterBackend]
    ordering_fields = '__all__'
    filterset_fields=['user__id',]
    search_fields = ['user__id',]

    def get_queryset(self):
        return models.Preference.objects.all()


class NotificationPreferenceModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['post','put','get']
    serializer_class = serializers.NotificationPreferenceSerializer


    def get_queryset(self):
        return models.NotificationPreference.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FriendSuggestionModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.FriendSuggestionSerializerGET
        if self.action == 'retrieve':
            return serializers.FriendSuggestionSerializerGET
        return serializers.FriendSuggestionSerializerPOST
    
    def get_queryset(self):
        return models.FriendSuggestion.objects.all()
    
class AdminFriendSuggestionModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.FriendSuggestionSerializerGET
        if self.action == 'retrieve':
            return serializers.FriendSuggestionSerializerGET
        return serializers.FriendSuggestionSerializerPOST
    
    def get_queryset(self):
        return models.FriendSuggestion.objects.all()
    
class CheckUsernameAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        try:
            username = request.data['username']
            user = User.objects.filter(username=username)
            if user.exists():
                return Response({'msg':'Username exists.','status':False}, status=status.HTTP_201_CREATED)
            return Response({'msg':'Username does not exists.','status':True}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
class FCMDevicesViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','post','delete']
    serializer_class = serializers.FCMDevicesSerializer

    def get_queryset(self):
        return models.FCMDevices.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UnifynderAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        try:
            user = request.user
            long = user.longitude
            lat = user.latitude
            radiusInKm = 100
            if long is None and lat is None:
                return Response({'error': 'Please select a current location'}, status=status.HTTP_400_BAD_REQUEST)
            kmInLongitudeDegree = 111.320 * math.cos( lat / 180.0 * math.pi)
            deltaLat = radiusInKm / 111.1;
            deltaLong = radiusInKm / kmInLongitudeDegree;
            minLat = lat - deltaLat; 
            maxLat = lat + deltaLat
            minLong = long - deltaLong
            maxLong = long + deltaLong
            users=User.objects.filter(longitude__gte=minLong,
                                latitude__gte=minLat,
                                longitude__lte=maxLong,
                                latitude__lte=maxLat)
            serializer = serializers.ProfileSerializer(users,many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

class AdminUserModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]
    serializer_class = serializers.ProfileSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['email','username','first_name','last_name','location','date_of_birth']
    search_fields = ['email','username','first_name','last_name','location','date_of_birth']
    ordering_fields = ['email','username','first_name','last_name','location','date_of_birth']
    queryset = User.objects.all()