from django.urls import path, include
from .views import (
    Home, SignUpView, SignInView, SignOutView, SignOutConfirm,
    UserProfileView, ChangeUsernameView, ChangeEmailView,
    ChangePassView, ChangeBioView, ChangeSiteView,
    ChangeLocaleView, ChangeImageView, PasswordReset,
    PasswordResetDone, PasswordResetConfirm,
    PasswordResetComplete, SocialFormView,
)

app_name = 'userapp'

urlpatterns = [
    path('', Home, name='home-page'),
    path('accounts/', include([
        path('signup/', SignUpView.as_view(), name='sign-up'),
        path('signin/', SignInView.as_view(), name='sign-in'),
        path('signout/', SignOutView.as_view(), name='sign-out'),
        path('signout-confirm/', SignOutConfirm.as_view(), name='sign-out-confirm'),
    ])),

    # password reset urls, removed redundancy
    path('accounts/reset_password/', include([
        path('', PasswordReset.as_view(), name='reset-password'),
        path('done/', PasswordResetDone.as_view(), name='reset-password-done'),
        path('<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='reset-password-confirm'),
        path('complete/', PasswordResetComplete.as_view(), name='reset-password-complete'),
    ])),

    path('profile/<slug:slug>', UserProfileView.as_view(), name='user-profile'),
    # user edit urls, removed redundancy
    path('profile/<slug:slug>/settings/edit/', include([
        path('username/', ChangeUsernameView.as_view(), name='edit-username'),
        path('email/', ChangeEmailView.as_view(), name='edit-email'),
        path('password/', ChangePassView.as_view(), name='edit-password'),
        path('website/', ChangeSiteView.as_view(), name='edit-website'),
        path('bio/', ChangeBioView.as_view(), name='edit-bio'),
        path('locale/', ChangeLocaleView.as_view(), name='edit-locale'),
        path('images/', ChangeImageView.as_view(), name='edit-image'),
        path('socials/', SocialFormView, name='edit-social'),
    ])),

]
