from django.urls import path,include
from rest_framework import routers
from groups import views

router = routers.DefaultRouter()
router.register('group-category', views.GroupCategoryModelViewSet,basename='group-category')
router.register('tags', views.TagsModelViewSet,basename='tags')
router.register('group', views.GroupModelViewSet,basename='group')
router.register('all-group', views.AllGroupModelViewSet,basename='all-group')
router.register('group-post', views.GroupPostModelViewSet,basename='all-group')
router.register('all-group-post', views.AllGroupPostModelViewSet,basename='all-group-post')
router.register('group-notification', views.GroupNotificationModelViewSet,basename='group-notification')

urlpatterns = [
    path('', include(router.urls)),
    path('group-remove-member/',views.RemoveUserGroup.as_view()),
    path('group-join-member/',views.JoinGroup.as_view())
]