from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm
)
from blogapp.models import Author, Social
from django import forms
from .models import User
from django.db import models
#instantiate the user model
USER = get_user_model()


##########################################
#forms to create users on the admin page
##########################################
class CreateUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = '__all__'


class ChangeUserForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = '__all__'


###########################################
# forms to create new users
###########################################
class SignUpForm(forms.Form):
    fname = forms.CharField(label=_('First Name'), max_length=255, required=True)
    lname = forms.CharField(label=_('Last Name'), max_length=255, required=True)
    uname = forms.CharField(label=_('Username'), max_length=200, required=True)
    email = forms.EmailField(label=_('Email Address'), required=True)
    SEX = ((_('Male'), _('Male')), (_('Female'), _('Female')))
    gender = forms.ChoiceField(
        label=_('Gender'), widget=forms.RadioSelect, choices=SEX, required=True
    )
    pass1 = forms.CharField(
        label=_('Password'), widget=forms.PasswordInput,
        min_length=8, required=True
    )
    pass2 = forms.CharField(
        label=_('Confirm Password'), widget=forms.PasswordInput,
        min_length=8, required=True
    )

    def clean_uname(self):
        uname = self.cleaned_data.get('uname')

        if USER.objects.filter(username=uname).count() > 0:
            raise forms.ValidationError(
                _('Username "%(value)s" already exists'),
                code='UserExists',
                params={'value': uname}
            )
        return uname

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if USER.objects.filter(email=email).count() > 0:
            raise forms.ValidationError(
                _('An account with that email already exists'),
                code='EmailExists',
                params={}
            )
        return email

    def clean_pass2(self):
        pass1 = self.cleaned_data.get('pass1')
        pass2 = self.cleaned_data.get('pass2')

        if pass1 and pass2:
            if pass2 != pass1:
                raise forms.ValidationError(
                    _('Passwords must match'),
                    code='WrongPass',
                    params={}
                )
        return pass2


###########################################
# forms to sign in users
###########################################
class SignInForm(forms.Form):
    email = forms.EmailField(label=_('Email'), required=True)
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput, required=True
    )
    # add specific field attribute detials via widget update
    email.widget.attrs.update({
        "class": "txt w-full outline-none h-12 p-2 text-ph text-lg bg-body-500 border-b-2 border-button transition-all duration-300 focus:border-white rounded-lg"
    })
    password.widget.attrs.update({
        "class": "txt w-full outline-none h-12 p-2 text-ph text-lg bg-body-500 border-b-2 border-button transition-all duration-300 focus:border-white rounded-lg"
    })

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            user = USER.objects.get(email=email)
        except USER.DoesNotExist:
            raise forms.ValidationError(
                _('This email address does not exist'),
                code='WrongEmail',
                params={}
            )
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')

        if USER.objects.filter(email=email).count() > 0:
            if not authenticate(email=email, password=password):
                raise forms.ValidationError(
                    _('Wrong password, try again'),
                    code='WrongPass',
                    params={}
                )
        else:
            pass
        return password


###########################################
# form to change username
###########################################
class ChangeUsernameForm(forms.Form):
    current_username = forms.CharField(
        label=_('Current Username'), max_length=100, required=False,
        disabled=True, widget=forms.HiddenInput
    )
    new_username = forms.CharField(
        label=_('New Username'), max_length=100, required=True
    )
    # update fields with the widget attribute
    new_username.widget.attrs.update({
        "class": "txt w-full outline-none h-12 p-2 text-ph text-lg bg-body-500 border-b-2 border-button transition-all duration-300 focus:border-white rounded-lg"
    })

    def clean_new_username(self):
        new_username = self.cleaned_data.get('new_username').lower()
        current_username = self.cleaned_data.get('current_username').lower()

        if USER.objects.filter(username=new_username).count() > 0:
            if new_username == current_username:
                raise forms.ValidationError(
                    _('%(value)s is already your username'),
                    code='UserExists',
                    params={'value': new_username}
                )
            else:
                raise forms.ValidationError(
                    _('Username %(value)s already exists'),
                    code='UserExists',
                    params={'value': new_username}
                )
        return new_username


###########################################
# form to change email
###########################################
class ChangeEmailForm(forms.Form):
    current_email = forms.EmailField(
        label=_('Current Email'), required=False, disabled=True,
        widget=forms.HiddenInput
    )
    new_email = forms.EmailField(label=_('New Email'), required=True)

    new_email.widget.attrs.update({
        "class": "txt w-full outline-none h-12 p-2 text-ph text-lg bg-body-500 border-b-2 border-button transition-all duration-300 focus:border-white rounded-lg"
    })

    def clean_new_email(self):
        new_email = self.cleaned_data.get('new_email')
        current_email = self.cleaned_data.get('current_email')

        if USER.objects.filter(email=new_email).count() > 0:
            if new_email == current_email:
                raise forms.ValidationError(
                    _('This is your current email address'),
                    code='EmailExists',
                    params={}
                )
            else:
                raise forms.ValidationError(
                    _("An account with that email address exists"),
                    code="EmailExists",
                    params={}
                )
        return new_email


###########################################
# form to change users basic info
###########################################
class ChangeBioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # adding attributs to form fields
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            "class": "txt w-full outline-none h-12 p-2 text-ph text-lg bg-body-500 border-b-2 border-button transition-all duration-300 focus:border-white rounded-lg"
        })
        self.fields['last_name'].widget.attrs.update({
            "class": "txt w-full outline-none h-12 p-2 text-ph text-lg bg-body-500 border-b-2 border-button transition-all duration-300 focus:border-white rounded-lg"
        })
        self.fields['other_name'].widget.attrs.update({
            "class": "txt w-full outline-none h-12 p-2 text-ph text-lg bg-body-500 border-b-2 border-button transition-all duration-300 focus:border-white rounded-lg"
        })
        self.fields['dob'].widget.attrs.update({
            "class": "txt w-full outline-none h-12 p-2 text-ph text-lg bg-body-500 border-b-2 border-button transition-all duration-300 focus:border-white rounded-lg",
            "type": "date"
        })
        self.fields['about_me'].widget.attrs.update({
            "class": "txt w-full outline-none h-32 p-2 text-ph text-lg bg-body-500 border-b-2 border-button transition-all duration-300 focus:border-white rounded-lg resize-none"
        })

    class Meta:
        model = USER
        fields = (
            'first_name', 'last_name', 'other_name',
            'dob', 'gender', 'about_me'
        )
        # widgets are used to change how a specific field
        # should be rendered
        widgets = {
            'gender': forms.RadioSelect
        }


class ChangePasswordForm(PasswordChangeForm):
    # i subclassed the PasswordChangeForm in order to edit certain attribute
    old_password = forms.CharField(
        label=_("Old password"), required=True, widget=forms.PasswordInput
    )
    new_password1 = forms.CharField(
        label=_("New password"), required=True, widget=forms.PasswordInput
    )
    new_password2 = forms.CharField(
        label=_("Confirm new password"), required=True, widget=forms.PasswordInput
    )

    # use widget update to add specific field attr
    old_password.widget.attrs.update({
        "class": "txt w-full outline-none h-12 p-2 text-ph text-lg bg-body-500 border-b-2 border-button transition-all duration-300 focus:border-white rounded-lg"
    })
    new_password1.widget.attrs.update({
        "class": "txt w-full outline-none h-12 p-2 text-ph text-lg bg-body-500 border-b-2 border-button transition-all duration-300 focus:border-white rounded-lg"
    })
    new_password2.widget.attrs.update({
        "class": "txt w-full outline-none h-12 p-2 text-ph text-lg bg-body-500 border-b-2 border-button transition-all duration-300 focus:border-white rounded-lg"
    })


###########################################
# form to change users location info
###########################################
class ChangeLocationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].widget.attrs.update({
            "class": "txt w-full outline-none h-12 p-2 text-ph text-lg bg-body-500 border-b-2 border-button transition-all duration-300 focus:border-white rounded-lg"
        })
        self.fields['state'].widget.attrs.update({
            "class": "txt w-full outline-none h-12 p-2 text-ph text-lg bg-body-500 border-b-2 border-button transition-all duration-300 focus:border-white rounded-lg"
        })
        self.fields['postal'].widget.attrs.update({
            "class": "txt w-full outline-none h-12 p-2 text-ph text-lg bg-body-500 border-b-2 border-button transition-all duration-300 focus:border-white rounded-lg"
        })

    class Meta:
        model = USER
        fields = ('country', 'state', 'postal')


###########################################
# form to change users added website
###########################################
class WebsiteForm(forms.Form):
    new_website = forms.URLField(
        label=_('New Website'), required=False,
    )
  
    # update form widget
    new_website.widget.attrs.update({
        "class": "txt w-full outline-none h-12 p-2 text-ph text-lg bg-body-500 border-b-2 border-button transition-all duration-300 focus:border-white rounded-lg"
    })


###########################################
# form to reset forgotten passwords
###########################################
class ResetPassForm(PasswordResetForm):
    # here i subclassed the PasswordResetForm which handle
    # all of the work for us except returning an error message
    # if the email address entered is incorrect. Which i will
    # fix now
    email = forms.EmailField(label=_('Enter email address'), required=True)

    email.widget.attrs.update({
        "class": "txt w-full outline-none h-12 p-2 text-ph text-lg bg-body-500 border-b-2 border-button transition-all duration-300 focus:border-white rounded-lg"
    })

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            user = USER.objects.get(email=email)
        except USER.DoesNotExist:
            raise forms.ValidationError(
                _('Could not find that email address'),
                code='WrongEmail',
                params={}
            )
        return email


###########################################
# form to set newpasswords
###########################################
class SetNewPassForm(SetPasswordForm):
    # we subclassed the biult in SetPasswordForm in order to specify
    # certian field attributes using the widget
    new_password1 = forms.CharField(
        label=_('New Password'), required=True, widget=forms.PasswordInput
    )
    new_password2 = forms.CharField(
        label=_('New Password Confirmation'), required=True, widget=forms.PasswordInput
    )

    # use widget update to add specific field attr
    new_password1.widget.attrs.update({
        "class": "txt w-full outline-none h-12 p-2 text-ph text-lg bg-body-500 border-b-2 border-button transition-all duration-300 focus:border-white rounded-lg"
    })
    new_password2.widget.attrs.update({
        "class": "txt w-full outline-none h-12 p-2 text-ph text-lg bg-body-500 border-b-2 border-button transition-all duration-300 focus:border-white rounded-lg"
    })


###########################################
# form to add/edit several social media
# account
###########################################
class SocialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['platform'].widget.attrs.update({
            "class": "txt w-full outline-none h-12 p-2 text-ph text-lg bg-body-500 border-b-2 border-button transition-all duration-300 focus:border-white rounded-lg"
        })
        self.fields['handle'].widget.attrs.update({
            "class": "txt w-full outline-none h-12 p-2 text-ph text-lg bg-body-500 border-b-2 border-button transition-all duration-300 focus:border-white rounded-lg"
        })
        self.fields['link'].widget.attrs.update({
            "class": "txt w-full outline-none h-12 p-2 text-ph text-lg bg-body-500 border-b-2 border-button transition-all duration-300 focus:border-white rounded-lg"
        })

    class Meta:
        model = Social
        fields = ['platform', 'handle', 'link']


###########################################
# form to change authors image and banner
###########################################
class AvatarForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['image', 'banner']
