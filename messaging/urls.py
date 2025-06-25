from django.urls import path
from .views import MessageListCreateAPIView, MessageRetrieveAPIView

urlpatterns = [
    path('', MessageListCreateAPIView.as_view(), name='message-list-create'),
    path('<int:pk>/', MessageRetrieveAPIView.as_view(), name='message-detail'),
]
