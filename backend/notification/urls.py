from django.urls import path,include
from rest_framework import routers
from notification import views

router = routers.DefaultRouter()
router.register('notifications', views.NotificationModelViewSet,
                basename='notification')

urlpatterns = [
    path('', include(router.urls))

]