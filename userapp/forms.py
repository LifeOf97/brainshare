from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import PasswordResetForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm
)
from blogapp.models import Author
from django import forms
from .models import User
# instantiate the user model
USER = get_user_model()


###########################################
# forms to create users on the admin page
###########################################
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

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            user = USER.objects.get(email=email)
        except USER.DoesNotExist:
            raise forms.ValidationError(
                _('Email address does not exist'),
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

    def clean_new_username(self):
        new_username = self.cleaned_data.get('new_username')
        current_username = self.cleaned_data.get('current_username')

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
    class Meta:
        model = USER
        fields = (
            'first_name', 'last_name', 'other_name',
            'dob', 'gender'
        )
        # widgets are used to change how a specific field
        # should be rendered
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.RadioSelect,
        }


###########################################
# form to change users basic info
###########################################
class ChangeLocationForm(forms.ModelForm):
    class Meta:
        model = USER
        fields = ('country', 'state', 'postal')


###########################################
# form to change email
###########################################
class ChangeImageForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('image', 'banner')


###########################################
# form to change email
###########################################
class WebsiteForm(forms.Form):
    remove = forms.BooleanField(
        label=_('Remove Website'), required=False
    )
    website = forms.URLField(
        label=_('New Website'), required=False,
    )
    # update form widget
    website.widget.attrs.update({'placeholder': 'http://www.site.com'})


class ResetPassForm(PasswordResetForm):

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
