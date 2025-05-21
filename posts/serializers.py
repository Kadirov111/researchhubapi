from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        max_length=255,
        required=True,
        allow_blank=False
    )
    content = serializers.CharField(
        required=True,
        allow_blank=False
    )

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_title(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Sarlavha kamida 5 ta belgidan iborat bo‘lishi kerak.")
        return value

    def validate_content(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Kontent kamida 10 ta belgidan iborat bo‘lishi kerak.")
        return value

    def validate(self, data):
        if data['title'].lower() in data['content'].lower():
            raise serializers.ValidationError({
                "content": "Kontent sarlavhani takrorlamasligi kerak."
            })
        return data
