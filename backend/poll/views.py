from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from filters.filters import RelatedOrderingFilter
from poll import serializers,models

class PollModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [RelatedOrderingFilter,filters.SearchFilter,DjangoFilterBackend]
    ordering_fields = '__all__'
    filterset_fields=['post__id',]
    search_fields = ['post__id',]


    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PollSerializerGET
        if self.action == 'retrieve':
            return serializers.PollSerializerGET
        return serializers.PollSerializerPOST
    
    def get_queryset(self):
        if self.request.method in ['POST','GET']:
            return models.Poll.objects.all()
        else:
            return models.Poll.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)