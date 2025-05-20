from rest_framework import serializers
from .models import PostView, UserActivity
from posts.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()

class PostViewSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = PostView
        fields = ['id', 'post', 'user', 'viewed_at']
        read_only_fields = ['id', 'viewed_at']

    def validate_post(self, value):
        if not Post.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Bunday post mavjud emas.")
        return value

    def validate(self, data):
        user = data.get('user', None)
        post = data.get('post')

        if user:
            recent = PostView.objects.filter(user=user, post=post).order_by('-viewed_at').first()
            from datetime import timedelta
            from django.utils import timezone
            if recent and timezone.now() - recent.viewed_at < timedelta(seconds=10):
                raise serializers.ValidationError("Siz ushbu postni yaqinda ko‘rgansiz.")
        return data


class UserActivitySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    action = serializers.ChoiceField(choices=UserActivity.ACTION_CHOICES)

    class Meta:
        model = UserActivity
        fields = ['id', 'user', 'post', 'action', 'timestamp']
        read_only_fields = ['id', 'timestamp']

    def validate_action(self, value):
        allowed_actions = [choice[0] for choice in UserActivity.ACTION_CHOICES]
        if value not in allowed_actions:
            raise serializers.ValidationError("Noto‘g‘ri action turi.")
        return value

    def validate(self, data):
        user = data.get('user')
        post = data.get('post')
        action = data.get('action')

        if not Post.objects.filter(id=post.id).exists():
            raise serializers.ValidationError("Post mavjud emas.")

        if action == 'like':
            from datetime import timedelta
            from django.utils import timezone
            one_minute_ago = timezone.now() - timedelta(minutes=1)
            recent_like = UserActivity.objects.filter(
                user=user,
                post=post,
                action='like',
                timestamp__gte=one_minute_ago
            ).exists()
            if recent_like:
                raise serializers.ValidationError("Siz bu postni yaqinda 'like' qilgansiz.")

        return data
