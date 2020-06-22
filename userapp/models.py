from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from .managers import UserManager
from django.db import models
import uuid


# Create your models here.
class User(AbstractUser):
    """
    My custom user model which makes use of the email address
    field as the required field for authentication. It also
    specifies some more specific fields for users
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    slug = models.SlugField(
        _("Slug"), default="", blank=True, null=True
    )
    email = models.EmailField(
        _("Email"), max_length=255, unique=True
    )
    username = models.CharField(
        _("Username/Alias"), max_length=255, unique=True
    )
    other_name = models.CharField(
        _("Other name"), max_length=255, blank=True, null=True
    )
    dob = models.DateField(
        _("Date of Birth"), auto_now=False,
        auto_now_add=False, blank=True, null=True
    )
    about_me = models.TextField(
        _("About me"), blank=True, null=True, default="",
        help_text=_("Over here, write few things about yourself that you think will interest those that read your post and check out your profile.Feel free.")
    )
    website = models.URLField(
        _("My website"), max_length=255, blank=True, null=True
    )
    phone_1 = models.CharField(
        _("Phone number"), max_length=255, blank=True, null=True
    )
    phone_2 = models.CharField(
        _("Extra Phone number"), max_length=255, blank=True, null=True
    )
    country = CountryField(
        blank_label=_("Select Country"), blank=True, null=True
    )
    state = models.CharField(
        _("State"), max_length=255, blank=True, null=True
    )
    postal = models.CharField(
        _("ZIP/Postal code"), max_length=255, blank=True, null=True
    )
    SEX = (
        (_('Male'), _('Male')), (_('Female'), _('Female'))
    )
    gender = models.CharField(
        _("Gender"), max_length=50, choices=SEX, default='Select Gender'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return F"{self.username}"
