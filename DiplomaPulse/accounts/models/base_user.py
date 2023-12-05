"""
Base user model.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .base import BaseModel
from ..managers import UserManager


class BaseUser(AbstractUser, BaseModel):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    username = None

    middle_name = models.CharField(_("middle name"), max_length=150, blank=True, null=True)

    profile_picture = models.ImageField(_("profile picture"), upload_to="profile_pictures", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()
