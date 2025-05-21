from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import connection
from django.core.cache import cache
import time

from .models import SystemCheckLog
from .serializers import SystemCheckLogSerializer


class SystemCheckLogCreateAPIView(generics.CreateAPIView):
    queryset = SystemCheckLog.objects.all()
    serializer_class = SystemCheckLogSerializer
    permission_classes = [permissions.AllowAny]


class SystemCheckLogListAPIView(generics.ListAPIView):
    queryset = SystemCheckLog.objects.all().order_by('-timestamp')
    serializer_class = SystemCheckLogSerializer
    permission_classes = [permissions.IsAdminUser]


class SystemCheckLogDetailAPIView(generics.RetrieveAPIView):
    queryset = SystemCheckLog.objects.all()
    serializer_class = SystemCheckLogSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'


class HealthCheckLogAPIView(generics.GenericAPIView):
    serializer_class = SystemCheckLogSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        start_time = time.time()

        # Database status check
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            db_status = "connected"
        except Exception:
            db_status = "error"

        # Cache status check
        try:
            cache.set("health_check", "ok", timeout=2)
            result = cache.get("health_check")
            cache_status = "connected" if result == "ok" else "error"
        except Exception:
            cache_status = "error"

        response_time_ms = round((time.time() - start_time) * 1000, 2)
        overall_status = "ok" if db_status == "connected" and cache_status == "connected" else "error"

        log_data = {
            "status": overall_status,
            "database_status": db_status,
            "cache_status": cache_status,
            "response_time_ms": response_time_ms,
        }

        serializer = self.get_serializer(data=log_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(log_data, status=status.HTTP_200_OK)
