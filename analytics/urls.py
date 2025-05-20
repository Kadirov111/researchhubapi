from django.urls import path
from .views import (
    PostViewCreateAPIView,
    UserActivityCreateAPIView,
    MostViewedPostsAPIView,
)

app_name = 'analytics'

urlpatterns = [
    path('post-views/', PostViewCreateAPIView.as_view(), name='post-view-create'),
    path('user-activities/', UserActivityCreateAPIView.as_view(), name='user-activity-create'),
    path('most-viewed-posts/', MostViewedPostsAPIView.as_view(), name='most-viewed-posts'),
]
