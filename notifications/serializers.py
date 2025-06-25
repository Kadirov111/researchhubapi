from rest_framework import serializers
from .models import Notification
from django.contrib.contenttypes.models import ContentType


class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    target_object = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id',
            'recipient',
            'actor',
            'actor_username',
            'verb',
            'target_content_type',
            'target_object_id',
            'target_object',
            'is_read',
            'timestamp',
        ]
        read_only_fields = ['id', 'timestamp', 'actor_username', 'target_object']

    def get_target_object(self, obj):
        """
        Target ob'ektdan qisqa ma'lumot qaytaradi.
        Masalan: comment text, post title, message preview
        """
        if obj.target:
            if hasattr(obj.target, 'content'):
                return obj.target.content[:30] + '...' if len(obj.target.content) > 30 else obj.target.content
            elif hasattr(obj.target, 'title'):
                return obj.target.title
            return str(obj.target)
        return None

    def to_representation(self, instance):

        rep = super().to_representation(instance)
        rep['message'] = f"{instance.actor.username} {instance.verb} you."
        return rep
