import datetime
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import TokenAuthentication
from posts import serializers,models
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from filters.filters import RelatedOrderingFilter
from django.db.models import Count

class UserPostModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        return models.Post.objects.filter(user=self.request.user).order_by('-created')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AllUserPostModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PostSerializer
    http_method_names = ['get']
    filter_backends = [RelatedOrderingFilter,filters.SearchFilter,DjangoFilterBackend]
    ordering_fields = '__all__'
    filterset_fields=['user__id','share_link']
    search_fields = ['user__id','share_link']


    def get_queryset(self):
        return models.Post.objects.all().order_by('-created')

class PostCommentModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PostCommentSerializer
    filter_backends = [RelatedOrderingFilter,filters.SearchFilter,DjangoFilterBackend]
    ordering_fields = '__all__'
    filterset_fields=['post__id',]
    search_fields = ['post__id',]

    def get_queryset(self):
        if self.request.method == 'GET':
            return models.PostComment.objects.all()
        return models.PostComment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostLikeModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [RelatedOrderingFilter,filters.SearchFilter,DjangoFilterBackend]
    ordering_fields = '__all__'
    filterset_fields=['post__id',]
    search_fields = ['post__id',]

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PostLikeSerializerGET
        if self.action == 'retrieve':
            return serializers.PostLikeSerializerGET
        return serializers.PostLikeSerializerPOST

    def get_queryset(self):
        if self.request.method == 'GET':
            return models.PostLike.objects.all()
        return models.PostLike.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentLikeModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [RelatedOrderingFilter,filters.SearchFilter,DjangoFilterBackend]
    ordering_fields = '__all__'
    filterset_fields=['comment__id',]
    search_fields = ['comment__id',]

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.CommentLikeSerializerGET
        if self.action == 'retrieve':
            return serializers.CommentLikeSerializerGET
        return serializers.CommentLikeSerializerPOST

    def get_queryset(self):
        if self.request.method == 'GET':
            return models.CommentLike.objects.all()
        return models.CommentLike.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FlagPostModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.FlagPostSerializer
    http_method_names = ['post','delete']

    def get_queryset(self):
        return models.FlagPost.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
class TrendingPostViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PostSerializer
    http_method_names = ['get']

    def get_queryset(self):
        now = datetime.datetime.now()
        week_start = now - datetime.timedelta(days=now.weekday())
        trends = list(models.PostLike.objects.filter(post__created__date=
        week_start.date()).values('post').annotate(total=Count('post')
        ).order_by('-total'))
        trends_ids = [trend['post'] for trend in trends]
        posts = models.Post.objects.in_bulk(trends_ids)
        sorted_posts = [posts[id] for id in trends_ids]
        return sorted_posts

class ChatImageModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ChatImageSerializer

    def get_queryset(self):
        return models.ChatImage.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FollowingUserPostModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PostSerializer
    http_method_names = ['get']
    filter_backends = [RelatedOrderingFilter,filters.SearchFilter,DjangoFilterBackend]
    ordering_fields = '__all__'
    filterset_fields=['user__id',]
    search_fields = ['user__id',]


    def get_queryset(self):
        return models.Post.objects.filter(user__in=self.request.user.following.all()).order_by('-created')
    
class RePostAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        try:
            post = models.Post.objects.get(id=request.data['post_id'])
            text = request.data['text']
            post2 = models.Post.objects.create(original_post = post,user=request.user,text=text)
            post.shared_by.add(request.user)
            serializer = serializers.PostSerializer(post2)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
class ShareLinkAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        try:
            post = models.Post.objects.get(id=request.data['post_id'])
            post.share_count = post.share_count + 1
            post.save()
            return Response({'link':post.share_link}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)