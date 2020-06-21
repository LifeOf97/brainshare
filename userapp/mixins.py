from blogapp.models import Author, Post, Social
from django.contrib.auth import get_user_model
from django_countries import countries
from django.http import JsonResponse
from django.urls import reverse
import datetime

# user model instanciation
users = get_user_model()

USER = users.objects.all()
AUTHOR = Author.objects.all()
SOCIAL = Social.objects.all()
POST = Post.objects.all()
# cache the User queryset
[data for data in USER]
[data for data in AUTHOR]
[data for data in SOCIAL]
[data for data in POST]


class JsonResponseMixin:
    """
    mixin to parse json data to the frontend instead of html
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        return JsonResponse parsing context as the data
        """
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        """
        return an object that will be serialized
        """
        # get the users primary key field and filter for that pk
        # in the USER model queryset in order to make the values
        # method available so fields will be in dictionary format for
        slug = context['object'].slug
        context = USER.filter(slug=slug).values(
            'first_name', 'last_name', 'other_name', 'email', 'username', 'about_me',
            'dob', 'website', 'country', 'state', 'postal', 'gender', 'date_joined'
        ).first()
        
        
        # add other neccessary info
        context['author_url'] = reverse("blogapp:author-detail", kwargs={"slug": slug})
        context['user_url'] = reverse("userapp:user-profile", kwargs={"slug": slug})
        context['number_of_post'] = POST.filter(author__profile__slug=slug).count()

        # add neccessary data from other models belonging to the user
        more_details_author = AUTHOR.filter(profile__slug=slug).values('banner', 'image').first()
        update_context = context.update(more_details_author)

        # social media accounts: i created a dictionary with the key 'social' containing
        # a list of all the social accounts that will later be appended to it belonging to the
        # requesting user
        more_details_social = SOCIAL.filter(author__profile__slug=slug).values('platform', 'handle', 'link')
        social = {'social': []}
        for data in list(range(more_details_social.count())):
            social['social'].append(more_details_social[data])
        context.update(social)
        
        
        # convert the country code to return the full country name
        # convert the dates to return a strftime format
        if context['dob'] is not None:
            dob_data = str(context['dob']).rsplit("-")
            context['dob'] = datetime.date(int(dob_data[0]), int(dob_data[1]), int(dob_data[2])).strftime("%b %d, %Y")

        if context['date_joined'] is not None:
            joined_data = str(context['date_joined'])[:10].rsplit("-")
            context['date_joined'] = datetime.date(int(joined_data[0]), int(joined_data[1]), int(joined_data[2])).strftime("%b %d, %Y")

        if context['country'] is not None:
            country = countries.countries[context['country']]
            context['country'] = country

        if context['first_name'] is None:
            context['first_name'] = ""

        if context['last_name'] is None:
            context['last_name'] = ""

        if context['other_name'] is None:
            context['other_name'] = ""

        return context
