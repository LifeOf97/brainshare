from django.views.generic import TemplateView
from django.urls import path, include
from .views import (
    Home, SignUpView, SignInView, SignOutView, SignOutConfirm,
    JsonUserProfileView, ChangeUsernameView, ChangeEmailView,
    ChangePassView, ChangeBioView, ChangeSiteView,
    ChangeLocaleView, ChangeImageView, PasswordReset,
    PasswordResetDone, PasswordResetConfirm,
    PasswordResetComplete, SocialFormView,
)

app_name = 'userapp'

urlpatterns = [
    path('', Home, name='home-page'),
    path('accounts/', include([
        path('signup', SignUpView.as_view(), name='sign-up'),
        path('signin', SignInView.as_view(), name='sign-in'),
        path('signout', SignOutView.as_view(), name='sign-out'),
        path('signout-confirm', SignOutConfirm.as_view(), name='sign-out-confirm'),
    ])),

    # password reset urls, removed redundancy
    path('accounts/reset_password/', include([
        path('', PasswordReset.as_view(), name='reset-password'),
        path('done/', PasswordResetDone.as_view(), name='reset-password-done'),
        path('<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='reset-password-confirm'),
        path('complete/', PasswordResetComplete.as_view(), name='reset-password-complete'),
    ])),


    path('<slug:slug>/dashboard', JsonUserProfileView.as_view(), name='user-profile'),
    # user edit urls, removed redundancy
    path('<slug:slug>/profile/settings/', include([
        path('username/', ChangeUsernameView.as_view(), name='edit-username'),
        path('email/', ChangeEmailView.as_view(), name='edit-email'),
        path('password/', ChangePassView.as_view(), name='edit-password'),
        path('website/', ChangeSiteView.as_view(), name='edit-website'),
        path('bio/', ChangeBioView.as_view(), name='edit-bio'),
        path('locale/', ChangeLocaleView.as_view(), name='edit-locale'),
        path('avatar/', ChangeImageView.as_view(), name='edit-avatar'),
        path('socials/', SocialFormView, name='edit-social'),
        path('play/', TemplateView.as_view(template_name='accounts/play.html'), name='play'),
    ])),

]