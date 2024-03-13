"""
Base user model.
"""

from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from samurai.accounts.choices import AccountTypeChoices
from samurai.accounts.managers.base_account import BaseAccountManager
from samurai.core.models.base import BaseUUIDModel


def generate_registration_code() -> str:
    return get_random_string(12)


def generate_default_email() -> str:
    return f"{uuid4()}@diploma-samurai.com"


class BaseAccount(AbstractUser, BaseUUIDModel):
    # We don't use username, so we set it to None
    username = None

    email = models.EmailField(
        _("email address"),
        unique=True,
        default=generate_default_email,
    )
    first_name = models.CharField(
        _("first name"),
        max_length=256,
    )
    last_name = models.CharField(
        _("last name"),
        max_length=256,
    )
    middle_name = models.CharField(
        _("middle name"),
        max_length=256,
        blank=True,
        null=True,
    )

    registration_code = models.CharField(
        _("registration code"),
        max_length=32,
        default=generate_registration_code,
        null=True,
    )

    profile_picture = models.ImageField(
        _("profile picture"),
        upload_to="profile_pictures",
        blank=True,
        null=True,
    )

    account_type = models.CharField(
        default=AccountTypeChoices.STUDENT,
        choices=AccountTypeChoices,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]

    objects: BaseAccountManager = BaseAccountManager()

    class Meta:
        verbose_name = _("Base User")
        verbose_name_plural = _("base users")
