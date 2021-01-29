from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    """
    CustomUserManager extends the Django's default :class:`django.contrib.auth.models.UserManager`.

    All methods provided by the **UserManager** are available like `create_user()`, `create_superuser()`, etc.
    """

    def active(self):
        """
        Return active users
        """
        return self.filter(
            is_active=True
        )
