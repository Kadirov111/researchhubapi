from django.db import models
from django.utils.timezone import now

class SystemCheckLog(models.Model):
    STATUS_CHOICES = [
        ('ok', 'OK'),
        ('error', 'Error'),
    ]

    timestamp = models.DateTimeField(default=now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    database_status = models.TextField()
    cache_status = models.TextField()
    response_time_ms = models.FloatField()

    def __str__(self):
        return f"{self.timestamp} - {self.status.upper()}"
