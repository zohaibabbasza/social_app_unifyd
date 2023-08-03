from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q
from albums import serializers,models
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from filters.filters import RelatedOrderingFilter

class AlbumModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AlbumSerializer

    def get_queryset(self):
        return models.Album.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GroupAlbumModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AlbumSerializer
    http_method_names = ['get']
    filter_backends = [RelatedOrderingFilter,filters.SearchFilter,DjangoFilterBackend]
    ordering_fields = '__all__'
    filterset_fields=['group__id',]
    search_fields = ['group__id',]

    def get_queryset(self):
        return models.Album.objects.all()

class PhotoModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PhotoSerializerGET
        if self.action == 'retrieve':
            return serializers.PhotoSerializerGET
        return serializers.PhotoSerializer
    
    def get_queryset(self):
        return models.Photo.objects.filter(user=self.request.user)