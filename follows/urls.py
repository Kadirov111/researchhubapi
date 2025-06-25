from django.urls import path
from .views import FollowListCreateAPIView, FollowDestroyAPIView

urlpatterns = [
    path('', FollowListCreateAPIView.as_view(), name='follow-list-create'),
    path('<int:pk>/', FollowDestroyAPIView.as_view(), name='follow-delete'),
]
