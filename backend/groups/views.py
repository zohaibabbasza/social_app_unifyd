from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import filters
from django.db.models import Count
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from filters.filters import RelatedOrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from groups import models,serializers

class GroupCategoryModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return serializers.GroupCategorySerializer

    def get_queryset(self):
        return models.GroupCategory.objects.all()


class TagsModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return serializers.TagSerializer

    def get_queryset(self):
        return models.Tags.objects.all()


class GroupModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.GroupSerializerGET
        if self.action == 'retrieve':
            return serializers.GroupSerializerGET
        return serializers.GroupSerializerPOST

    def get_queryset(self):
        return models.Group.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AllGroupModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['name','tags__name']
    search_fields = ['name','tags__name']
    http_method_names = ['get']

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.GroupSerializerGET
        if self.action == 'retrieve':
            return serializers.GroupSerializerGET
        return serializers.GroupSerializerPOST

    def get_queryset(self):
        return models.Group.objects.all()

class GroupPostModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.GroupPostSerializerGET
        if self.action == 'retrieve':
            return serializers.GroupPostSerializerGET
        return serializers.GroupPostSerializerPOST

    def get_queryset(self):
        return models.GroupPost.objects.filter(post__is_group_post=True,
            post__user = self.request.user)

class AllGroupPostModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    filter_backends = [RelatedOrderingFilter,filters.SearchFilter,DjangoFilterBackend]
    ordering_fields = '__all__'
    filterset_fields=['group__id',]
    search_fields = ['group__id',]

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.GroupPostSerializerGET
        if self.action == 'retrieve':
            return serializers.GroupPostSerializerGET
        return serializers.GroupPostSerializerPOST

    def get_queryset(self):
        return models.GroupPost.objects.all()


class RemoveUserGroup(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            user = request.user
            removed_user = models.User.objects.filter(id = request.data['u_id']).first()
            group = models.Group.objects.filter(id = request.data['group_id']).first()
            if group.user != user:
                return Response({'error': 'You are not the owner of this group'}, status=status.HTTP_400_BAD_REQUEST)
            group.members.remove(removed_user)
            return Response({'msg':"Successfully removed user"},status=status.HTTP_201_CREATED)
        except Exception as e:
             return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
class JoinGroup(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            user = request.user
            group = models.Group.objects.filter(id = request.data['group_id']).first()
            group.members.add(user)
            return Response({'msg':"Successfully added user in group"},status=status.HTTP_201_CREATED)
        except Exception as e:
             return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        

class GroupNotificationModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return serializers.GroupNotificationSerializer

    def get_queryset(self):
        return models.GroupNotification.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
