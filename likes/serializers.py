from rest_framework import serializers
from .models import Like

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        user = attrs['user']
        post = attrs['post']
        if Like.objects.filter(user=user, post=post).exists():
            raise serializers.ValidationError("You already liked this post.")
        return attrs
