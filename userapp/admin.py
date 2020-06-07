from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.template.defaultfilters import slugify
from .forms import CreateUserForm, ChangeUserForm
from django.contrib import admin
from .models import User


# Register your models here.
class UserAdmin(BaseUserAdmin):
    add_form = CreateUserForm
    form = ChangeUserForm

    list_display = ('username', 'email', 'country', 'is_active', 'is_staff', 'is_superuser')
    list_display_links = ('username', )

    # fieldset is used to display fields during changing (editing)
    # a model
    fieldsets = (
        (None, {'fields': ('username', 'email', 'slug')}),
        ('Personal Info', {'fields': (
            ('first_name', 'last_name', 'other_name'), ('gender', 'dob'))
        }),
        ('Contact', {'fields': ('website', ('phone_1', 'phone_2'), 'about_me')}),
        ('Location', {'fields': (('country', 'state'), 'postal')}),
        ('Important Dates', {'fields': ('date_joined', 'last_login')}),
        ('Permissions', {'fields': (
            'is_active', 'is_staff', 'is_superuser', ('groups', 'user_permissions')
        )}),
    )
    # add_fieldset is used to create new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')
        }),
    )

    ordering = ('-username',)

    # user admin methods
    def get_search_fields(self, request):
        """
        what can be searched for on the user admin page
        and by who
        """
        if request.user.is_superuser:
            return ['username', 'country']
        return []

    def get_list_filter(self, request):
        """
        filter the results based of certain fields and
        should be available only to superusers
        """
        if request.user.is_superuser:
            return ['is_active', 'is_staff', 'is_superuser', 'date_joined']
        return []

    def get_readonly_fields(self, request, obj):
        """
        fields that should be rendered as readonly, (that is
        fields that cannot be edited) some for users with
        superuser permissions while some for other users
        """
        if obj:
            if request.user.is_superuser:
                return ['last_login', 'date_joined', 'slug']
            return [
                'is_active', 'is_staff', 'is_superuser', 'date_joined',
                'slug', 'last_login', 'groups', 'user_permissions'
            ]
        return []

    def get_queryset(self, request):
        """
        instances of the user model that should be visible
        to certain users based on permmissions
        """
        query_set = super().get_queryset(request)
        if request.user.is_superuser:
            return query_set
        return query_set.filter(username=request.user.username)

    def save_model(self, request, obj, form, change):
        obj.slug = slugify(obj.username)
        return super().save_model(request, obj, form, change)


admin.site.register(User, UserAdmin)
