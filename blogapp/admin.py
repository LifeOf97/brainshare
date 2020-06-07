from django.template.defaultfilters import slugify
from django.utils import timezone
from django.contrib import admin
from .models import (
    Author, Social, Post,
    MoreContent
)


# Register your models here.
# Inline model admin
class SocialStacked(admin.StackedInline):
    model = Social
    extra = 0
    fieldsets = (
        (None, {'fields': (('platform', 'link'), 'handle')}),
    )


class MoreCotentStacked(admin.StackedInline):
    model = MoreContent
    extra = 0
    fieldsets = (
        (None, {
            "fields": (
                ('heading', 'text_content'), ('image', 'image_copyright', 'image_copyright_link'),
                ('list_content', 'list_style'), 'code'
            )
        }),
    )


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("profile", 'number_of_post', 'slug')
    list_display_links = ("profile",)
    inlines = [SocialStacked, ]
    ordering = ('profile',)

    fieldsets = (
        (None, {
            "fields": (
                'profile', 'slug', ('banner', 'image'),
                'number_of_post'
            ),
        }),
    )

    # model admin methods
    def get_list_filter(self, request):
        """
        filter the results based of certain fields and
        should be available only to superusers
        """
        if request.user.is_superuser:
            return ['profile', ]
        return []

    def get_readonly_fields(self, request, obj):
        """
        fields that should be rendered as readonly, (that is
        fields that cannot be edited) some for users with
        superuser permissions while some for other users
        """
        if request.user.is_superuser:
            return ['slug', 'number_of_post']
        return ['profile', 'slug', 'number_of_post']

    def get_search_fields(self, request):
        """
        what can be searched for on the user admin page
        and by who
        """
        if request.user.is_superuser:
            return ['profile']
        return []

    def get_queryset(self, request):
        """
        instances of the user model that should be visible
        to certain users based on permmissions
        """
        query_set = super().get_queryset(request)
        if request.user.is_superuser:
            return query_set
        return query_set.filter(
            profile=request.user
        )

    def save_model(self, request, obj, form, change):
        """
        users without superuser permissions automatically becomes
        the profile user, The slug field is prepopulated with data
        from the title field.
        """
        if not request.user.is_superuser:
            obj.profile = request.user
        obj.slug = slugify(obj.profile.username)
        super().save_model(request, obj, form, change)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'concern', 'author', 'date_to_publish', 'status')
    list_display_links = ('title', )
    ordering = ('date_to_publish', )
    inlines = [MoreCotentStacked, ]
    actions = ['make_publish', 'make_draft']

    fieldsets = (
        (None, {"fields": ('author', )}),
        ('Identifier', {"fields": (
            ('title', 'slug', 'concern'),
            ('banner', 'banner_copyright', 'banner_copyright_link'))
            }),
        ('Content', {"fields": (
            ('heading', 'text_content'), ('image', 'image_copyright', 'image_copyright_link'),
            ('list_content', 'list_style'), 'code'
        )}),
        ('Tags', {"fields": ('tags', )}),
        ('Status', {"fields": ('date_to_publish', 'status')})
    )


    # my custom model admin actions
    def make_publish(self, request, queryset):
        """
        action to publish selected post by changing the date_to_publish
        field to the current timezone. And also alerting the user
        of their actions
        """
        updated = queryset.update(date_to_publish=timezone.now(), status='Published')
        message = 'successfully marked as published.'
        if updated == 1:
            msg = "1 post was"
        else:
            msg = F"{updated} posts were"
        self.message_user(request, F"{msg} {message}")
    make_publish.short_description = 'Publish selected posts'


    def make_draft(self, request, queryset):
        """
        action to draft selected post by changing the date_to_publish
        field to 30 days in the future. And also alerting the user
        of their actions
        """
        date = timezone.now() + timezone.timedelta(30)
        updated = queryset.update(date_to_publish=date, status='Draft')
        message = "successfully marked as drafted"
        if updated == 1:
            msg = "1 post was"
        else:
            msg = F"{updated} posts were"
        self.message_user(request, F"{msg} {message}")
    make_draft.short_description = 'Draft selected posts'


    # post model admin methods
    def get_list_filter(self, request):
        """
        filter the results based of certain fields and
        should be available only to superusers
        """
        if request.user.is_superuser:
            return ['author', 'date_to_publish']
        return ['date_to_publish', ]


    def get_search_fields(self, request):
        """
        what can be searched for on the user admin page
        and by who
        """
        if request.user.is_superuser:
            return ['author', 'title', 'status']
        return ['status',]


    def get_readonly_fields(self, request, obj):
        """
        fields that should be rendered as readonly, (that is
        fields that cannot be edited) some for users with
        superuser permissions while some for other users
        """
        if request.user.is_superuser:
            return ['slug', 'status']
        return ['author', 'slug', 'status']


    def get_queryset(self, request):
        """
        instances of the user model that should be visible
        to certain users based on permmissions
        """
        query_set = super().get_queryset(request)
        if request.user.is_superuser:
            return query_set
        return query_set.filter(author__profile__username=request.user.username)


    def save_model(self, request, obj, form, change):
        """
        THe author field is filled with the current logged in
        user if the user does not have the superuser permission.
        while users with the superuser permission can explicitly
        select an author. The slug field is prepopulated with
        the data from the title field
        """
        if not request.user.is_superuser:
            obj.author = request.user.author

        if obj.date_to_publish <= timezone.now():
            obj.status = 'Published'
        else:
            obj.status = 'Draft'

        obj.slug = slugify(obj.title)
        super().save_model(request, obj, form, change)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
