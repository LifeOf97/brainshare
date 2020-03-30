from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.db import models
from .files import (
    AuthorImage, AuthorBanner,
    PostImage, PostBanner,
    MorePostImage
)
import uuid
# Create your models here.


class Author(models.Model):
    """
    An author model that has a OneToOne field to the
    user model of this app, thereby getting more specific
    user details. Every author has a user model that contains
    bio data belonging to the author.
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
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

    def get_absolute_url(self):
        return reverse("blogapp:author-detail", kwargs={"slug": self.slug})

    def number_of_post(self):
        return Post.objects.filter(
            author__profile__username=self.profile.username
        ).count()

    def get_full_name(self):
        return F"{self.profile.first_name} {self.profile.last_name} {self.profile.other_name}"


class Social(models.Model):
    """
    A social model used to add social media links to
    the author so their readers can follow them and more
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    OPTIONS = (
        ('Brainshare', 'Brainshare'), ('Facebook', 'Facebook'),
        ('Twitter', 'Twitter'), ('Instagram', 'Instagram'),
        ('Tumblr', 'Tumblr'), ('LinkedIn', 'LinkedIn'),
        ('Pinterest', 'Pinterest'), ('Telegram', 'Telegram'),
        ('YouTube', 'YouTube'), ('Discord', 'Discord'),
        ('Github', 'Github')
    )
    platform = models.CharField(
        _("Platform"), max_length=100, choices=OPTIONS,
        blank=True, null=True,
        help_text=_('Select a social media platform')
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
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
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
    banner_copyright = models.CharField(
        _("Copyright"), max_length=255, default='',
        blank=True, null=True,
        help_text=_('Where this image was gotten from')
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
    image_copyright = models.CharField(
        _("Copyright"), max_length=255, default='',
        blank=True, null=True,
        help_text=_('Where this image was gotten from')
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
        return F"Title: {self.title} Author: {self.author.profile.username}"

    def get_absolute_url(self):
        return reverse("blogapp:post-detail", kwargs={"slug": self.slug})


class MoreContent(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
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
    copy_right = models.CharField(
        _("Copyright"), max_length=255, default='',
        blank=True, null=True,
        help_text=_('Where this image was gotten from')
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
