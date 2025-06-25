from django.urls import path
from .views import LikeListCreateAPIView, LikeDestroyAPIView

urlpatterns = [
    path('', LikeListCreateAPIView.as_view(), name='like-list-create'),
    path('<int:pk>/', LikeDestroyAPIView.as_view(), name='like-delete'),
]
