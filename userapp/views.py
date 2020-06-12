from django.views.generic.detail import SingleObjectTemplateResponseMixin, BaseDetailView
from django.views.generic import FormView, TemplateView, DetailView
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.forms import inlineformset_factory, BaseInlineFormSet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.views.generic.edit import FormMixin
from blogapp.models import Author, Social, Post
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import Group
from django.contrib.auth.views import (
    LogoutView, PasswordChangeView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
)
from django.contrib.auth import (
    get_user_model, authenticate,
    login,
)
from .forms import (
    SignUpForm, SignInForm, ChangeUsernameForm,
    ChangeEmailForm, ChangeBioForm, ChangeLocationForm,
    ChangeImageForm, ResetPassForm, SocialForm,
    WebsiteForm, SetNewPassForm, ChangePasswordForm,
    AvatarForm,
)
from django.shortcuts import render, redirect
from .mixins import JsonResponseMixin
from django.utils import timezone  
from django import forms

# instantiate the user model
USER = get_user_model()
# cache th user model
USER_ALL = USER.objects.all()
POST_ALL = Post.objects.all()
[data for data in USER_ALL]
[data for data in POST_ALL]



def Home(request):
    # if a user is authenticated return the dashboard of that user else:
    # return the sites homepage
    if request.user.is_authenticated:
        return HttpResponseRedirect(
            reverse('userapp:user-profile', kwargs={'slug': request.user.slug})
        )
    else:
        return render(request, 'basement.html')


# Create your views here.
class SignUpView(FormView):
    """
    this view creates a new user and makes that user an
    author, it also makes sure the new user gets added
    to the brainshare group.
    """
    form_class = SignUpForm
    template_name = 'accounts/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        if form.is_valid():
            fname = form.cleaned_data['fname']
            lname = form.cleaned_data['lname']
            uname = form.cleaned_data['uname']
            email = form.cleaned_data['email']
            gender = form.cleaned_data['gender']
            password = form.cleaned_data['pass2']
            # create a new user with all data collected
            user = USER()
            user.first_name, user.last_name = fname, lname
            user.username, user.email = uname, email
            user.gender, user.slug = gender, slugify(uname)
            user.set_password(password)
            user.save()
            # after successfully creating the user, make that user
            # an author.
            author = Author()
            author.profile, author.slug = user, slugify(uname)
            author.save()
            # create a mandatery social account for authors on
            # the brainshare platform.
            social = Social()
            social.author, social.platform = author, 'Brainshare'
            social.handle = user.username
            social.link = F'https://www.brainshare.com/profile/{user.username}'
            social.save()
            # get the barinshare author group and add the
            # new user to the group
            BSgroup = Group.objects.get(name='BRAINSHARE AUTHORS')
            user.groups.add(BSgroup)
            # redirect to the sign in page on successful sign up
            return HttpResponseRedirect(reverse('userapp:sign-in'))
        return super().post(request, *args, **kwargs)


class SignInView(FormView):
    form_class = SignInForm
    template_name = 'accounts/signin.html'

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        next = request.GET.get('next')
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # authenticate the user
            user = authenticate(request, email=email, password=password)
            if user:
                # login the user if authentication passed
                login(request, user)
                if next:
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect(reverse('userapp:home-page'))
        return super().post(request, *args, **kwargs)


class SignOutView(TemplateView):
    template_name = 'accounts/signout.html'
class SignOutConfirm(LogoutView):
    next_page = 'userapp:home-page'


class JsonUserProfileView(LoginRequiredMixin, JsonResponseMixin, SingleObjectTemplateResponseMixin, BaseDetailView):
    # if you look at the parameters, you will notice we made use of both  SingleObjectTemplateResponseMixin
    # and BaseDetailView. SingleObjectTemplateResponseMixin is a class mixin that performs template-based
    # response rendering for views that operate upon a single object instance. while BaseDetailView is
    # a view that does not render template response, that is, a detailview before the templatemixin was added
    model = USER
    login_url = 'userapp:sign-in'
    template_name = 'accounts/dashboard.html'
    context_object_name = 'profile'

    def get(self, request, **kwargs):
        # First make sure the user who made this request
        # is the logged in user. You can make use of the
        # UserPassesTestMixin, but i never tried it so..
        if request.user.slug != kwargs['slug']:
            return HttpResponseForbidden("Who the hell are you?")
        return super().get(request, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        # if the request was ajax, return a json data else return standartd html
        if self.request.GET.get('format') == 'json':
            return self.render_to_json_response(context, **response_kwargs)
        else:
            return super().render_to_response(context)


class ChangeUsernameView(LoginRequiredMixin, FormView):
    """
    form to change the username of the logged in user. This also
    makes sure the slug field of both the user and author models
    are changed as expected. Because the slug fields are created
    from the username.
    """
    form_class = ChangeUsernameForm
    template_name = 'accounts/settings.html'
    login_url = 'userapp:sign-in'

    def get(self, request, *args, **kwargs):
        # First make sure the user who made this request
        # is the logged in user. You can make use of the
        # UserPassesTestMixin, but i never tried it so..
        if request.user.slug != kwargs['slug']:
            return HttpResponseForbidden("Who the hell are you??")

        # initialize the user
        user = USER.objects.get(slug=kwargs['slug'])
        # set the field(s) that should have an initial data
        self.initial = {'current_username': user.username}
        form = self.form_class(initial=self.initial)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # initiallize the user
        user = USER.objects.get(slug=kwargs['slug'])
        # set the field(s) that should have an initial data.
        # it also has to be passed to the post request also
        self.initial = {'current_username': user.username}
        form = self.form_class(request.POST, initial=self.initial)

        if form.is_valid():
            new_username = form.cleaned_data['new_username']
            # initialize the user
            user = USER.objects.get(slug=request.user.slug)
            user.username, user.slug = new_username, slugify(new_username)
            user.save()
            # initialize the author model so as to update the slug field
            author = Author.objects.get(profile=request.user)
            author.slug = slugify(new_username)
            author.save()
            return HttpResponseRedirect(
                reverse('userapp:user-profile', kwargs={'slug': user.slug})
            )
        return super().post(request, *args, **kwargs)


class ChangeEmailView(LoginRequiredMixin, FormView):
    """
    view to change users email address
    """
    form_class = ChangeEmailForm
    template_name = 'accounts/settings.html'
    login_url = 'userapp:sign-in'

    def get(self, request, *args, **kwargs):
        # First make sure the user who made this request
        # is the logged in user. You can make use of the
        # UserPassesTestMixin, but i never tried it so..
        if request.user.slug != kwargs['slug']:
            return HttpResponseForbidden("Who the hell are you")

        # initialize the user to get the email address
        user = USER.objects.get(slug=kwargs['slug'])
        self.initial = {'current_email': user.email}

        form = self.form_class(initial=self.initial)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = USER.objects.get(slug=request.user.slug)
        self.initial = {'current_email': user.email}
        form = self.form_class(request.POST, initial=self.initial)

        if form.is_valid():
            email = form.cleaned_data['new_email']
            # change email and save.
            user.email = email
            user.save()

            return HttpResponseRedirect(
                reverse('userapp:user-profile', kwargs={'slug': user.slug})
            )
        return super().post(request, *args, **kwargs)


class ChangeSiteView(LoginRequiredMixin, FormView):
    """
    form to add or edit a users website as part of
    the user data form. Always make sure to pass the
    user as an instance.
    """
    form_class = WebsiteForm
    template_name = 'accounts/settings.html'
    login_url = 'userapp:sign-in'

    def get(self, request, *args, **kwargs):
        # First make sure the user who made this request
        # is the logged in user.
        if request.user.slug != kwargs['slug']:
            return HttpResponseForbidden("Who the hell are you")

        form = self.get_form()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = USER.objects.get(slug=kwargs['slug'])
        form = self.form_class(request.POST)

        if form.is_valid():
            website = form.cleaned_data['new_website']
            user.website = website
            user.save()

            return HttpResponseRedirect(
                reverse(
                    'userapp:user-profile',
                    kwargs={'slug': user.slug}
                )
            )
        return super().post(request, *args, **kwargs)


class ChangePassView(LoginRequiredMixin, PasswordChangeView):
    # NOTE: the post request is handled by the PasswordChangeForm
    # provided by django
    form_class = ChangePasswordForm
    template_name = 'accounts/settings.html'
    login_url = 'userapp:sign-in'

    def get(self, request, *args, **kwargs):
        # First make sure the user who made this request
        # is the logged in user.
        if request.user.slug != kwargs['slug']:
            return HttpResponseForbidden("Who the hell are you")
        form = self.get_form()
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'userapp:user-profile',
            kwargs={'slug': self.request.user.slug}
        )


class ChangeBioView(LoginRequiredMixin, FormView):
    """
    This view is to edit basic users data such as first name. i am
    passing initial data as a fall back for fields that where not
    edited to remain the same.
    """
    form_class = ChangeBioForm
    template_name = 'accounts/settings.html'
    login_url = 'userapp:sign-in'

    def get(self, request, *args, **kwargs):
        # First make sure the user who made this request
        # is the logged in user.
        if kwargs['slug'] != request.user.slug:
            return HttpResponseForbidden("Who the hell are you")

        # initialize the user
        user = USER.objects.get(slug=kwargs['slug'])
        # reference all necessary fields
        self.initial = {
            'first_name': user.first_name, 'last_name': user.last_name,
            'other_name': user.other_name, 'dob': user.dob,
            'gender': user.gender, 'about_me': user.about_me
        }
        form = self.form_class(initial=self.initial)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # initialize the user
        user = USER.objects.get(slug=kwargs['slug'])
        form = self.form_class(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse(
                    'userapp:user-profile',
                    kwargs={'slug': user.slug}
                )
            )


class ChangeLocaleView(LoginRequiredMixin, FormView):
    """
    This view is to edit users location details.
    passing initial data as a fall back for fields
    that where not edited
    """
    form_class = ChangeLocationForm
    template_name = 'accounts/settings.html'
    login_url = 'userapp:sign-in'

    def get(self, request, *args, **kwargs):
        # First make sure the user who made this request
        # is the logged in user.
        if request.user.slug != kwargs['slug']:
            return HttpResponseForbidden("Who the hell are you")

        # initialize the user
        user = USER.objects.get(slug=kwargs['slug'])
        # reference all necessary fields
        self.initial = {
            'country': user.country, 'state': user.state,
            'postal': user.postal
        }
        form = self.form_class(initial=self.initial)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # initialize the user
        user = USER.objects.get(slug=kwargs['slug'])
        form = self.form_class(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse(
                    'userapp:user-profile',
                    kwargs={'slug': user.slug}
                )
            )


class ChangeImageView(LoginRequiredMixin, FormView):
    """
    This view is to edit  profile picture and banner of
    users who are authors. So it is mandatry to pass the
    Author as an instance to the form on post request.
    """
    form_class = ChangeImageForm
    template_name = 'accounts/settings.html'
    login_url = 'userapp:sign-in'

    def get(self, request, *args, **kwargs):
        # First make sure the user who made this request
        # is the logged in user.
        if request.user.slug != kwargs['slug']:
            return HttpResponseForbidden("Who the hell are you")

        form = self.form_class()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # initialize the user
        author = Author.objects.get(slug=kwargs['slug'])
        form = self.form_class(request.POST, request.FILES, instance=author)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse(
                    'userapp:user-profile',
                    kwargs={'slug': kwargs['slug']}
                )
            )


class ChangeAvatarView(LoginRequiredMixin, FormView):
    form_class = AvatarForm
    template_name = "accounts/settings.html"
    login_url = 'userapp:sign-in'

    def get(self, request, *args, **kwargs):
        # First make sure the user who made this request
        # is the logged in user.
        if request.user.slug != kwargs['slug']:
            return HttpResponseForbidden("Who the hell are you")

        form = self.form_class()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(
                reverse("userapp:user-profile", kwargs={'slug': request.user.slug})
            )


# View to add/edit social media accounts for users
class BaseSocialForm(BaseInlineFormSet):
    # class to create custom validation. To ensure one
    # platform does not occure twice and any field with
    # data must have a platform
    def clean(self):
        super().clean()

        # list of platforms
        platforms = []

        for form in self.forms:
            # this ensure that forms marked for deletion shoule be
            # deleted before futher checks for validation errors
            if self.can_delete and self._should_delete_form(form):
                continue

            # get necessary fields
            platform = form.cleaned_data.get('platform')
            handle = form.cleaned_data.get('handle')
            link = form.cleaned_data.get('link')

            # if the handle and link fields has data while the platform
            # is None return an error, as a platform must be present
            # before an handle and link can be available.
            # and if the platform already exists return an error
            if handle and link:
                if platform is None:
                    raise forms.ValidationError(
                        _('A handle and link is missing a platform')
                    )

                if platform in platforms:
                    raise forms.ValidationError(
                        _('Duplicate platforms not allowed.')
                    )

                # and if the platform passes all the checks
                # add the platform into the platforms list
                platforms.append(platform)


@login_required
def SocialFormView(request, slug):
    """
    View to add/edit social media accounts. This uses
    inlineformset factory to render more than one form.
    for the currently logged in user
    """
    # First make sure the user who made this request
    # is the logged in user.
    if slug != request.user.slug:
        return HttpResponseForbidden("Who the hell are you")

    formset = inlineformset_factory(
        Author, Social, form=SocialForm, max_num=11, extra=11,
        validate_max=True, formset=BaseSocialForm
    )
    # get the author instance
    author = Author.objects.get(slug=slug)

    if request.method == "POST":
        forms = formset(request.POST or None, instance=author)

        if forms.is_valid():
            # commit the form. But do not save yet
            instances = forms.save(commit=False)
            # then loop over the forms (instances) to make sure
            # all fields are filled before saving
            for instance in instances:
                platform = instance.platform
                handle = instance.handle
                link = instance.link

                if platform and handle and link:
                    instance.save()

            # for forms that are marked for deletion, loop over the
            # deleted_objects attribute on the form and delete them
            # manually.
            for to_delete in forms.deleted_objects:
                to_delete.delete()

            # redirect to the users profile page after all is done.
            return HttpResponseRedirect(
                reverse('userapp:user-profile', kwargs={'slug': slug})
            )

    else:
        forms = formset(instance=author)

    return render(request, 'accounts/settings.html', {'forms': forms})


# views to reset passwords
class PasswordReset(PasswordResetView):
    # i subclassed the built in PasswordResetForm in the resetpassword class
    # in forms.py file in order to edit it to provide custom errors when
    # an email address does not exist. And import the form here.
    form_class = ResetPassForm
    template_name = 'accounts/resetform.html'
    email_template_name = 'accounts/resetmail.html'
    subject_template_name = 'accounts/resetsubject.txt'

    # If the email supplied is correct redirect to passwordresetdone view
    def get_success_url(self):
        return reverse_lazy('userapp:reset-password-done')


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'accounts/resetpassdone.html'

    def get_email(self, request, *args, **kwargs):
        email_address = request.POST.get("email")
        print("hello")
        print(email_address)
        # return super().get_email(request, *args, **kwargs)


class PasswordResetConfirm(PasswordResetConfirmView):
    # view to render password change form, you can omit
    # the form_class field if using the default form which
    # but i explicitly set it. Or totally create your own form.
    form_class = SetNewPassForm
    template_name = 'accounts/newpassform.html'

    def get_success_url(self):
        return reverse_lazy('userapp:reset-password-complete')


class PasswordResetComplete(PasswordResetCompleteView):
    # view to return template after successful password rest.
    template_name = 'accounts/resetcomplete.html'
