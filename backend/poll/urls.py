from django.urls import path,include
from rest_framework import routers
from poll import views

router = routers.DefaultRouter()
router.register('poll', views.PollModelViewSet,basename='poll')

urlpatterns = [
    path('', include(router.urls))
]