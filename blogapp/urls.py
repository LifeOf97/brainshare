from django.views.decorators.cache import cache_page
from django.urls import path
from .views import (
    PostListView, PostDetailView,
    AuthorDetailView,
)

app_name = 'blogapp'

# Your urls here
urlpatterns = [
    path('blog', PostListView.as_view(), name='post-list'),
    path('blog/read/<slug:slug>', PostDetailView.as_view(), name='post-detail'),
    path('author/<slug:slug>', AuthorDetailView.as_view(), name='author-detail'),
]
