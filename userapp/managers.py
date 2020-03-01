from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """
    custom user manager used along side my custom user model,
    to create users and superusers. this makes use of the
    email address as the required field.
    """

    def create_user(self, email, username, password, **other_fields):
        # create and save a user  whilest making the user active
        if not email:
            raise ValueError(_("An email address is needed"))

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **other_fields
        )
        user.is_active = True
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **other_fields):
        """
        superusers should have is_active, is_staff and is_superuser set.
        """
        other_fields['is_staff'] = True
        other_fields['is_superuser'] = True

        return self.create_user(email, username, password, **other_fields)
