from django.urls import path,include
from rest_framework import routers
from users.views import (
    user_redirect_view,
    user_update_view,
    user_detail_view,
    VerifyPasswordToken,
    ResendUserToken,
    VerifyUserToken,
    SendPasswordToken,
    ProfileModelViewSet,
    FriendsModelViewSet,
    BlockedUserModelViewSet,FriendRequestModelViewSet,
    FriendSuggestionModelViewSet,
    AcceptFriendRequest,
    BlockFriend,
    UnBlockFriend,
    GetFollowers,
    GetFollowing,
    ChangePassword,
    PreferenceModelViewSet,
    NotificationPreferenceModelViewSet,
    CheckUsernameAPI,
    AllPreferenceModelViewSet,
    FCMDevicesViewSet,UnifynderAPI,
    AdminUserModelViewSet,
    AdminFriendSuggestionModelViewSet
)
router = routers.DefaultRouter()
router.register('profile', ProfileModelViewSet,basename='profile')
router.register('friends', FriendsModelViewSet,basename='friend')
router.register('blocked', BlockedUserModelViewSet,basename='blocked')
router.register('friend-request', FriendRequestModelViewSet,basename='friend-request')
router.register('preference', PreferenceModelViewSet,basename='preference')
router.register('all-preference', AllPreferenceModelViewSet,basename='all-preference')
router.register('notification-preference', NotificationPreferenceModelViewSet,basename='notification-preference')
router.register('friend-suggestion', FriendSuggestionModelViewSet,basename='friend-suggestion')
router.register('fcm-devices', FCMDevicesViewSet,basename='fcm-device')
router.register('admin-all-users', AdminUserModelViewSet,basename='admin-users')
router.register('admin-friend-suggestion', AdminFriendSuggestionModelViewSet,basename='admin-friend-suggestion')


app_name = "users"
urlpatterns = [
    path('', include(router.urls)),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path('email/verify-user/',VerifyUserToken.as_view()),
    path('email/resend-token/',ResendUserToken.as_view()),
    path('reset-password/send/',SendPasswordToken.as_view()),
    path('reset-password/verify/',VerifyPasswordToken.as_view()),
    path('accept/friend-request/',AcceptFriendRequest.as_view()),
    path('block/user/',BlockFriend.as_view()),
    path('unblock/user/',UnBlockFriend.as_view()),
    path('follow/get-followers/',GetFollowers.as_view()),
    path('follow/get-following/',GetFollowing.as_view()),
    path('password/change/',ChangePassword.as_view()),
    path('username/check/',CheckUsernameAPI.as_view()),
    path('find/unifynder/',UnifynderAPI.as_view()),
]
