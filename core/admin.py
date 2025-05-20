from django.contrib import admin
from .models import SystemCheckLog

@admin.register(SystemCheckLog)
class SystemCheckLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'status', 'database_status', 'cache_status', 'response_time_ms')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
