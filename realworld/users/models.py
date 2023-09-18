from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext as _


class User(AbstractUser):
    email = models.EmailField(unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        })
    bio = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)


    def __str__(self):
        return self.email 
    
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    # add a related_name argument to the groups field
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='custom_user_set'
    )

    # add a related_name argument to the user_permissions field
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='custom_user_set'
    )
