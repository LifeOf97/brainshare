from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.db import models
from .files import (
    AuthorImage, AuthorBanner,
    PostImage, PostBanner,
    MorePostImage
)
# Create your models here.


class Author(models.Model):
    """
    An author model that has a OneToOne field to the
    user model of this app, thereby getting more specific
    user details. Every author has a user model that contains
    bio data belonging to the author.
    """
    profile = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    slug = models.SlugField(
        _("Slug"),
        help_text=_('This field is prepopulated with the username of the profile')
    )
    banner = models.ImageField(
        _("Banner"), upload_to=AuthorBanner,
        blank=True, null=True,
        help_text=_('An image used as your banner')
    )
    image = models.ImageField(
        _("Profile picture"), upload_to=AuthorImage,
        blank=True, null=True,
        help_text=_('An image used as your Display picture')
    )
    number_of_post = models.IntegerField(
        _("Number of Posts"), blank=True, null=True
    )

    def __str__(self):
        return F"{self.profile.username}"

    def number_of_post(self):
        return Post.objects.filter(
            author__profile__username=self.profile.username
        ).count()


class Social(models.Model):
    """
    A social model used to add social media links to
    the author so their readers can follow them and more
    """
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    platform = models.CharField(
        _("Platform"), max_length=200,
        blank=True, null=True,
        help_text=_('The name of the social media platform')
    )
    handle = models.CharField(
        _("Handle"), max_length=200,
        blank=True, null=True,
        help_text=_('What is your username on this platform')
    )
    link = models.URLField(
        _("Link to your page"), max_length=200,
        blank=True, null=True,
        help_text=_('Full address (link) to your page')
    )

    def __str__(self):
        return F"{self.handle} @ {self.platform}"


class Post(models.Model):
    """
    A post model used to create post by an author
    """
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE
    )
    title = models.CharField(
        _("Title"), max_length=255,
        blank=True, null=True,
        help_text=_('The title of this post')
    )
    slug = models.SlugField(
        _("Slug"), blank=True, null=True,
        help_text=_('This field is prepopulated with the title field')
    )
    banner = models.ImageField(
        _("Banner"), upload_to=PostBanner,
        blank=True, null=True,
        help_text=_('An image displayed along side the title')
    )
    tags = models.TextField(
        _("Tags"), blank=True, null=True,
        help_text=_('Terms concerning this post. E.G. programming, politics')
    )
    heading = models.CharField(
        _("Heading"), max_length=255, blank=True, null=True,
        help_text=_('The main heading of this post')
    )
    text_content = models.TextField(
        _("Text Content"), blank=True, null=True,
        help_text=_('Text content of this post')
    )
    image = models.ImageField(
        _("Image"), upload_to=PostImage,
        blank=True, null=True,
        help_text=_(
            '<p>If the post requires an image, upload one here</p><p>More images can be uploaded from the more section</p>'
        )
    )
    # to add list to post
    STYLE = (
        (_('Ordered List (numeric)'), _('Ordered List (numeric)')),
        (_('Unordered List (bullet)'), _('Unordered List (bullet)'))
    )
    list_style = models.CharField(
        _("List Style"), max_length=100, choices=STYLE,
        default=_('Ordered List (numeric)'),
        help_text=_('How the list should be displayed')
    )
    list_content = models.TextField(
        _("List Content"), blank=True, null=True,
        help_text=_('This fields converts comma seperated texts into list')
    )
    #  to add programming code
    code = models.TextField(
        _("Code"), blank=True, null=True,
        help_text=_('Add code samples to post for better understanding')
    )
    date_to_publish = models.DateTimeField(
        _("Publish Date"), default=timezone.now,
        help_text=_('When should this post be published? Default is now.')
    )

    def __str__(self):
        return F"Title:{self.title} Author:{self.author.profile.username}"


class MoreContent(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    heading = models.CharField(
        _("Heading"), max_length=255, blank=True, null=True,
        help_text=_('Heading of this content if any')
    )
    text_content = models.TextField(
        _("Text Content"), blank=True, null=True,
        help_text=_('Text content if any')
    )
    image = models.ImageField(
        _("Image"), upload_to=MorePostImage,
        blank=True, null=True,
        help_text=_('Add more images to the post')
    )
    # to add list to post
    STYLE = (
        (_('Ordered List (numeric)'), _('Ordered List (numeric)')),
        (_('Unordered List (bullet)'), _('Unordered List (bullet)'))
    )
    list_style = models.CharField(
        _("List Style"), max_length=100, choices=STYLE,
        default=_('Ordered List (numeric)'),
        help_text=_('How the list should be displayed')
    )
    list_content = models.TextField(
        _("List Content"), blank=True, null=True,
        help_text=_('This fields converts comma seperated texts into list')
    )
    #  to add programming code
    code = models.TextField(
        _("Code"), blank=True, null=True,
        help_text=_('Add more code samples')
    )
