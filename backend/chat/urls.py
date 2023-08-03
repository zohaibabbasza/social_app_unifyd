from django.urls import path,include
from rest_framework import routers
from chat import views

router = routers.DefaultRouter()
router.register('chats', views.ChatModelViewSet,basename='chat')
router.register('chat-request', views.ChatRequestViewSet,basename='chat-request')

urlpatterns = [
    path('', include(router.urls))

]