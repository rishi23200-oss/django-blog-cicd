import logging
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Author, Post, Comment
from .serializers import PostSerializer, CommentSerializer

logger = logging.getLogger(__name__)


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        author, created = Author.objects.get_or_create(user=self.request.user)
        serializer.save(author=author)
        logger.info(f"New post created by {self.request.user.username}: {serializer.instance.title}")


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs['post_id'])
        author, created = Author.objects.get_or_create(user=self.request.user)
        serializer.save(post=post, author=author)
        logger.info(f"New comment by {self.request.user.username} on post {post.id}")