from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model
from django.utils.timesince import timesince

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'author', 'author_username', 'created_at']
        read_only_fields = ['id', 'created_at', 'author_username']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['created_ago'] = timesince(instance.created_at) + " ago"
        return rep

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title should be at least 5 characters.")
        return value

    def validate_body(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Body should be at least 10 characters.")
        return value


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.IntegerField()
    post = serializers.IntegerField()
    content = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)

    def to_internal_value(self, data):
        internal_data = super().to_internal_value(data)

        try:
            internal_data['user'] = User.objects.get(id=internal_data['user'])
        except User.DoesNotExist:
            raise serializers.ValidationError({'user': 'User not found.'})

        from .models import Post
        try:
            internal_data['post'] = Post.objects.get(id=internal_data['post'])
        except Post.DoesNotExist:
            raise serializers.ValidationError({'post': 'Post not found.'})

        return internal_data

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'content': instance.content,
            'user': {
                'id': instance.user.id,
                'username': instance.user.username
            },
            'post': {
                'id': instance.post.id,
                'title': instance.post.title
            },
            'created_at': instance.created_at.isoformat(),
            'created_ago': timesince(instance.created_at) + " ago"
        }

    def validate_content(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Comment must be at least 5 characters.")
        return value

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)
