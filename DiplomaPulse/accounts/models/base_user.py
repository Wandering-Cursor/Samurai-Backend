"""
Base user model.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from uuid import uuid4

from .base import BaseModel
from ..managers import UserManager


def generate_registration_code():
    return get_random_string(12)


def generate_default_email():
    return f"{uuid4()}@diplomapulse.com"


class BaseUser(AbstractUser, BaseModel):
    email = models.EmailField(
        _("email address"),
        unique=True,
        default=generate_default_email,
    )
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)

    registration_code = models.CharField(
        _("registration code"),
        max_length=150,
        default=generate_registration_code,
        null=True,
    )

    username = None

    middle_name = models.CharField(_("middle name"), max_length=150, blank=True, null=True)

    profile_picture = models.ImageField(_("profile picture"), upload_to="profile_pictures", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects: UserManager = UserManager()
