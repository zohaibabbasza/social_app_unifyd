from django.urls import path,include
from rest_framework import routers
from albums import views

router = routers.DefaultRouter()
router.register('albums', views.AlbumModelViewSet,basename='album')
router.register('albums-group', views.GroupAlbumModelViewSet,basename='group-album-data')
router.register('photo', views.PhotoModelViewSet,basename='photo')

urlpatterns = [
    path('', include(router.urls))

]