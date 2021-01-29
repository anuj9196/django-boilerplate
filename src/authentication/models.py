from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from authentication.managers import CustomUserManager


class User(AbstractUser):
    """
    An extended model of the AbstractUser to serve base User model.
    It is always recommended to use custom user model by extending AbstractUser
    provided by Django.
    More: https://docs.djangoproject.com/en/2.1/topics/auth/customizing/
    """

    # Is user is a shared user, this field will be True, False otherwise
    email = models.EmailField(_('email address'), blank=True, unique=True)

    objects = CustomUserManager()

    class Meta(AbstractUser.Meta):
        ordering = ['-date_joined', 'email']

    def __str__(self):
        return self.email

    def avatar(self):
        """
        Get avatar image from Gravatar based on the email of the user
        :return: Gravatar image url
        """
        # Check if avatar exists in profile
        # try:
        #     if self.profile.avatar:
        #         return self.profile.avatar.url
        # except Profile.DoesNotExist:
        #     Profile.objects.create_for_user(self)

        # # Default return gravatar
        # return gravatar_url(self.email)
        # return self.profile.profile_pic
        return None

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)
