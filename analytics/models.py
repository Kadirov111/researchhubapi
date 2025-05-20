from django.db import models
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()

class PostView(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='post_views')
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']
        indexes = [
            models.Index(fields=['post', 'viewed_at']),
            models.Index(fields=['user', 'viewed_at']),
        ]
        verbose_name = "Post View"
        verbose_name_plural = "Post Views"

    def __str__(self):
        return f"View: {self.post.title} by {self.user or 'Anonymous'} at {self.viewed_at}"

class UserActivity(models.Model):
    ACTION_CHOICES = [
        ('view', 'View'),
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('share', 'Share'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['post', 'timestamp']),
        ]
        verbose_name = "User Activity"
        verbose_name_plural = "User Activities"

    def __str__(self):
        return f"{self.user} {self.action} on {self.post.title} at {self.timestamp}"
