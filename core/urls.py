from django.urls import path
from .views import (
    HealthCheckLogAPIView,
    SystemCheckLogCreateAPIView,
    SystemCheckLogListAPIView,
    SystemCheckLogDetailAPIView,
)

app_name = 'core'

urlpatterns = [
    path('health/', HealthCheckLogAPIView.as_view(), name='health-check'),
    path('logs/create/', SystemCheckLogCreateAPIView.as_view(), name='log-create'),
    path('logs/', SystemCheckLogListAPIView.as_view(), name='log-list'),
    path('logs/<int:id>/', SystemCheckLogDetailAPIView.as_view(), name='log-detail'),
]
