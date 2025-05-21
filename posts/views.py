from rest_framework import generics, permissions
from django.db.models import Q

from .models import Post
from .serializers import PostSerializer


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]


class PostSearchView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            )
        return Post.objects.none()
