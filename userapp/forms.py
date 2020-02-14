from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm
)
from django import forms
from .models import User

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
