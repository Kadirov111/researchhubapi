from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'short_content', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender__username', 'receiver__username', 'content')
    ordering = ('-created_at',)

    def short_content(self, obj):
        return obj.content[:30] + ('...' if len(obj.content) > 30 else '')

    short_content.short_description = 'Preview'
