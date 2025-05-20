from rest_framework import generics, permissions
from django.db.models import Count
from .models import PostView, UserActivity
from posts.models import Post
from .serializers import PostViewSerializer, UserActivitySerializer
from rest_framework.response import Response

class PostViewCreateAPIView(generics.CreateAPIView):
    queryset = PostView.objects.all()
    serializer_class = PostViewSerializer
    permission_classes = [permissions.AllowAny]


class UserActivityCreateAPIView(generics.CreateAPIView):
    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer
    permission_classes = [permissions.AllowAny]


class MostViewedPostsAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        posts = Post.objects.annotate(view_count=Count('views')).order_by('-view_count')[:10]
        data = [
            {
                'id': post.id,
                'title': post.title,
                'view_count': post.view_count
            }
            for post in posts
        ]
        return Response(data)
