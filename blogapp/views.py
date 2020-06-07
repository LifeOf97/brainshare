from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.utils import timezone
from .models import Author, Post
from django.views.generic import (
    ListView, DetailView,
)
# Create your views here.

# cache the post and author data to reduce the number of times
# the database is hit per request, by accessing the database thereby
# evaluating it. if the entire queryset has already been evaluated,
# the cache will be checked instead: REFERRE TO THE OFFICIAL DJANGO DOC.
# using the list method
POST_DATA, AUTHOR_DATA = Post.objects.all(), Author.objects.all()
[data for data in POST_DATA]
[data for data in AUTHOR_DATA]


class PostListView(ListView):
    model = Post
    template_name = 'blog/postlist.html'
    context_object_name = 'postlist'
    # paginate_by = 2

    # here i added the concern phrase of all posts that is published.
    # Also make sure to add the distinct query so as to return unique values
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['concerns'] = POST_DATA.filter(
            date_to_publish__lte=timezone.now()
        ).values('concern').distinct()
        return context

    def get_queryset(self):
        return super().get_queryset().filter(
            date_to_publish__lte=timezone.now()
        )


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/postdetail.html'
    context_object_name = 'postdetail'

    def get(self, request, *args, **kwargs):
        # check if the post requested for has been published, if not,
        # deny access to the post. That is, if the date_to_publish
        # field is greater than the current date and time.
        if POST_DATA.filter(slug=kwargs['slug'], date_to_publish__gte=timezone.now()).count() > 0:
            return HttpResponseForbidden("Post not available.")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        # here, we also parse other published posts of the author of the post
        # that was clicked to be read by the viewer to the template.
        context = super().get_context_data(*args, **kwargs)
        post = POST_DATA.get(slug=self.kwargs['slug'])
        context['morepost'] = POST_DATA.filter(
            author=post.author, date_to_publish__lte=timezone.now()
        ).exclude(slug=self.kwargs['slug'])
        return context


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'blog/author.html'
    context_object_name = 'authordetail'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['posts'] = POST_DATA.filter(
            author__slug=self.kwargs['slug'],
            date_to_publish__lte=timezone.now()
        )
        return context
