from django.views.decorators.cache import cache_page
from django.urls import path, include
from .views import (
    PostListView, PostConcernView, PostDetailView,
    AuthorDetailView, PostSearchView, PostTagView,
)

app_name = 'blogapp'

# Your urls here
urlpatterns = [
    path('blog/', include([
        path('', PostListView.as_view(), name='post-list'),
        path('search/', PostSearchView, name='post-search'),
        path('tagged/<tag>', PostTagView.as_view(), name='post-tag'),
        path('concerning_only/<str:concern>', PostConcernView.as_view(), name='post-concern'),
        path('read/<slug:slug>', PostDetailView.as_view(), name='post-detail'),
    ])),
    path('author/<slug:slug>', AuthorDetailView.as_view(), name='author-detail'),
]
