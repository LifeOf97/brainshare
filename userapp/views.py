from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import Group
from django.views.generic import FormView
from blogapp.models import Author
from django.contrib.auth import (
    get_user_model, authenticate,
    login,
)
from .forms import (
    SignUpForm, SignInForm, ChangeUsernameForm,
    ChangeEmailForm, ChangeBioForm, WebsiteForm,
    ChangeLocationForm, ChangeImageForm,
)

# instantiate the user model
USER = get_user_model()


def Home(request):
    return render(request, 'basement.html')


# Create your views here.
class SignUpView(FormView):
    """
    this view creates a new user and makes that user an
    author, it also makes sure the new brainshare group
    permissions gets added to the new author.
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
    next_page = 'userapp:sign-in'


class UserProfileView(LoginRequiredMixin, DetailView):
    model = USER
    template_name = 'accounts/userdetail.html'
    context_object_name = 'userdetail'
    login_url = 'userapp:sign-in'

    def get(self, request, **kwargs):
        # Firstly check if the user who made this request
        # is the logged in user. You can make use of the
        # UserPassesTestMixin, but i never tried it so..
        if request.user.slug != kwargs['slug']:
            return HttpResponseForbidden("What are you doing?")
        return super().get(request, **kwargs)


class ChangeUsernameView(LoginRequiredMixin, FormView):
    """
    form to change the username of the logged in user. This also
    makes sure the slug field of both the user and author models
    are changed as expected. Because their slug fields are created
    from the username.
    """
    form_class = ChangeUsernameForm
    template_name = 'accounts/edit.html'
    login_url = 'userapp:sign-in'

    def get(self, request, *args, **kwargs):
        # Firstly check if the user who made this request
        # is the logged in user. You can make use of the
        # UserPassesTestMixin, but i never tried it so..
        if request.user.slug != kwargs['slug']:
            return HttpResponseForbidden("What are you doing??")

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
            # initialize the author
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
    template_name = 'accounts/edit.html'
    login_url = 'userapp:sign-in'

    def get(self, request, *args, **kwargs):
        # Firstly check if the user who made this request
        # is the logged in user. You can make use of the
        # UserPassesTestMixin, but i never tried it so..
        if request.user.slug != kwargs['slug']:
            return HttpResponseForbidden("What are you doing")

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
    template_name = 'accounts/editwebsite.html'
    login_url = 'userapp:sign-in'

    def get(self, request, *args, **kwargs):
        # Firstly check if the user who made this request
        # is the logged in user. You can make use of the
        # UserPassesTestMixin, but i never tried it so. :)
        if request.user.slug != kwargs['slug']:
            return HttpResponseForbidden("What are you doing")

        form = self.get_form()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            remove = form.cleaned_data['remove']
            website = form.cleaned_data['website']
            # check if remove is true, meaning the user just
            # wants to remove the website.
            user = USER.objects.get(slug=kwargs['slug'])
            if remove:
                user.website = None
            else:
                user.website = website
            # save the user data
            user.save()

            return HttpResponseRedirect(
                reverse(
                    'userapp:user-profile',
                    kwargs={'slug': user.slug}
                )
            )
        return super().post(request, *args, **kwargs)


class ChangePassView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'accounts/edit.html'
    login_url = 'userapp:sign-in'

    def get(self, request, *args, **kwargs):
        # Firstly check if the user who made this request
        # is the logged in user. You can make use of the
        # UserPassesTestMixin, but i never tried it so. :)
        if request.user.slug != kwargs['slug']:
            return HttpResponseForbidden("What are you doing")
        form = self.get_form()
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'userapp:user-profile',
            kwargs={'slug': self.request.user.slug}
        )


class ChangeBioView(LoginRequiredMixin, FormView):
    """
    This view is to edit basic users data such as first name.
    So it is mandatry to pass the user as an instance to the
    post form. But passing initial data as a fall back for
    fields that where not edited to remain the same is your
    choice.
    """
    form_class = ChangeBioForm
    template_name = 'accounts/edit.html'
    login_url = 'userapp:sign-in'

    def get(self, request, *args, **kwargs):
        # Firstly check if the user who made this request
        # is the logged in user. You can make use of the
        # UserPassesTestMixin, but i never tried it so. :)
        if request.user.slug != kwargs['slug']:
            return HttpResponseForbidden("What are you doing")

        # initialize the user
        user = USER.objects.get(slug=kwargs['slug'])
        # reference all necessary fields
        self.initial = {
            'first_name': user.first_name, 'last_name': user.last_name,
            'other_name': user.other_name, 'dob': user.dob,
            'gender': user.gender
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
    So it is mandatry to pass the user as an instance to the
    post form. But passing initial data as a fall back for
    fields that where not edited to remain the same is your
    choice.
    """
    form_class = ChangeLocationForm
    template_name = 'accounts/edit.html'
    login_url = 'userapp:sign-in'

    def get(self, request, *args, **kwargs):
        # Firstly check if the user who made this request
        # is the logged in user. You can make use of the
        # UserPassesTestMixin, but i never tried it so. :)
        if request.user.slug != kwargs['slug']:
            return HttpResponseForbidden("What are you doing")

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
    template_name = 'accounts/edit.html'
    login_url = 'userapp:sign-in'

    def get(self, request, *args, **kwargs):
        # Firstly check if the user who made this request
        # is the logged in user. You can make use of the
        # UserPassesTestMixin, but i never tried it so. :)
        if request.user.slug != kwargs['slug']:
            return HttpResponseForbidden("What are you doing")

        form = self.form_class()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # initialize the user
        author = Author.objects.get(slug=kwargs['slug'])
        print(author)
        form = self.form_class(request.POST, request.FILES, instance=author)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse(
                    'userapp:user-profile',
                    kwargs={'slug': kwargs['slug']}
                )
            )
