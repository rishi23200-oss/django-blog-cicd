from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Author, Post, Comment


class AuthorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'username', 'bio', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author_username', 'created_at']
        read_only_fields = ['author_username', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.user.username', read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author_username', 'comment_count', 'created_at', 'updated_at']
        read_only_fields = ['author_username', 'created_at', 'updated_at']
