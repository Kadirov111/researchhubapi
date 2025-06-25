from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at')
    list_filter = ('author', 'created_at')
    search_fields = ('title', 'body', 'author__username')
    ordering = ('-created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'short_content', 'created_at')
    list_filter = ('user', 'post', 'created_at')
    search_fields = ('content', 'user__username', 'post__title')
    ordering = ('-created_at',)

    def short_content(self, obj):
        return obj.content[:30] + ('...' if len(obj.content) > 30 else '')
    short_content.short_description = 'Content Preview'
