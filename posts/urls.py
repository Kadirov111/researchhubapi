from django.urls import path
from .views import PostListCreateView, PostSearchView

app_name = 'posts'

urlpatterns = [
    path('', PostListCreateView.as_view(), name='list-create'),
    path('search/', PostSearchView.as_view(), name='search'),
]
