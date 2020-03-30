from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.utils import timezone
from .models import Author, Post
from django.views.generic import (
    ListView, DetailView,
)
# Create your views here.


class PostListView(ListView):
    model = Post
    template_name = 'blog/postlist.html'
    context_object_name = 'postlist'

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
        # deny access to the post. That is if the date_to_publish
        # field is greater than the current date and time.
        now = timezone.now()
        if Post.objects.filter(slug=kwargs['slug'], date_to_publish__gt=now).count() > 0:
            return HttpResponseForbidden("Post not available.")
        return super().get(request, *args, **kwargs)


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'blog/author.html'
    context_object_name = 'authordetail'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['posts'] = Post.objects.filter(
            author__slug=self.kwargs['slug'],
            date_to_publish__lte=timezone.now()
        )
        return context
