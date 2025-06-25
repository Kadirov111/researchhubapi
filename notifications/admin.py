from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'actor', 'verb', 'target_object_id', 'target_content_type', 'is_read', 'timestamp')
    list_filter = ('is_read', 'verb', 'timestamp')
    search_fields = ('actor__username', 'recipient__username', 'verb')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
