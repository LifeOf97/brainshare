from django.views.generic.detail import BaseDetailView, SingleObjectTemplateResponseMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.utils.decorators import method_decorator
from userapp.mixins import JsonResponseMixin
from django.shortcuts import render, reverse
from django.utils import timezone
from .models import Author, Post
from django.views.generic import (
    ListView, DetailView,
)
from django.db.models import Q
# Create your views here.

# cache the post and author data to reduce the number of times
# the database is hit per request, by accessing the database thereby
# evaluating it. if the entire queryset has already been evaluated,
# the cache will be checked instead: REFERRE TO THE OFFICIAL DJANGO DOC.
# using the list method
POST_DATA, AUTHOR_DATA = Post.objects.all(), Author.objects.all()
[data for data in POST_DATA]
[data for data in AUTHOR_DATA]


def Home(request):
    # if a user is authenticated return the dashboard of that user else:
    # return the sites homepage
    if request.user.is_authenticated:
        return HttpResponseRedirect(
            reverse('userapp:user-profile', kwargs={'slug': request.user.slug})
        )
    else:
        return render(request, 'blog/index.html')


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
        # return only posts that have been published
        return super().get_queryset().filter(
            date_to_publish__lte=timezone.now()
        )


class PostConcernView(ListView):
    model = Post
    template_name = 'blog/postlist.html'
    context_object_name = 'postlist'

    # here i added the concern phrase of all posts that is published.
    # Also make sure to add the distinct query so as to return unique values
    # as for mysql.
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['concerns'] = POST_DATA.filter(
            date_to_publish__lte=timezone.now()
        ).values('concern').distinct()
        return context

    def get_queryset(self, *args, **kwargs):
        # return only posts that have been published
        return POST_DATA.filter(
            concern=self.kwargs['concern'],
            date_to_publish__lte=timezone.now()
        )


class PostTagView(ListView):
    # classView to return posts with similar tags
    model = Post
    template_name = 'blog/filter.html'
    context_object_name = 'posts'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tag'] = self.kwargs['tag']
        return context

    def get_queryset(self, *args, **kwargs):
        return POST_DATA.filter(
            tags__icontains=self.kwargs['tag'],
            date_to_publish__lte=timezone.now()
        )


class PostSearchView(ListView):
    # classview to query the database and return search results
    model = Post
    template_name = 'blog/filter.html'
    context_object_name = 'posts'

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('q')
        return POST_DATA.filter(
            Q(concern__icontains=query) | Q(tags__icontains=query) |
            Q(title__icontains=query)
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


class AuthorDetailView(JsonResponseMixin, SingleObjectTemplateResponseMixin, BaseDetailView):
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

    def render_to_response(self, context, **response_kwargs):
        # if the request was ajax, return a json data else return standartd html
        if self.request.GET.get('format') == 'json':
            return self.render_to_json_response(context, **response_kwargs)
        else:
            return super().render_to_response(context)
