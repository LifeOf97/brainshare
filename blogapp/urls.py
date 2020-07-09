from django.views.decorators.cache import cache_page
from django.urls import path, include
from .views import (
    Home,
    PostListView, PostConcernView, PostDetailView,
    AuthorDetailView, PostSearchView, PostTagView,
)

app_name = 'blogapp'

# Your urls here
urlpatterns = [
    path('', Home, name='home-page'),
    path('blog/', include([
        path('', PostListView.as_view(), name='post-list'),
        path('search/', PostSearchView.as_view(), name='post-search'),
        path('tagged/<tag>', PostTagView.as_view(), name='post-tag'),
        path('concerning_only/<str:concern>', PostConcernView.as_view(), name='post-concern'),
        path('read/<slug:slug>', cache_page(900)(PostDetailView.as_view()), name='post-detail'),
    ])),
    path('author/<slug:slug>', AuthorDetailView.as_view(), name='author-detail'),
]
