from django.urls import path,include
from rest_framework import routers
from posts import views

router = routers.DefaultRouter()
router.register('all-posts', views.AllUserPostModelViewSet,basename='all-posts')
router.register('user-posts', views.UserPostModelViewSet,basename='user-post')
router.register('comments', views.PostCommentModelViewSet,basename='comment')
router.register('like', views.PostLikeModelViewSet,basename='like')
router.register('following-posts', views.FollowingUserPostModelViewSet,basename='follow-post')
router.register('comment-like', views.CommentLikeModelViewSet,basename='comment-like')
router.register('flag-post', views.FlagPostModelViewSet,basename='flag-post')
router.register('trending-post', views.TrendingPostViewSet,basename='trending-post')
router.register('chat-image', views.ChatImageModelViewSet,basename='chat-image')

urlpatterns = [
    path('', include(router.urls)),
    path('re-post/',views.RePostAPI.as_view()),
    path('share-link/',views.ShareLinkAPI.as_view())
]