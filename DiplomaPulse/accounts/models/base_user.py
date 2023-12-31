"""
Base user model.
"""
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from ..managers import UserManager
from ._base import BaseModel


def generate_registration_code():
	return get_random_string(12)


def generate_default_email():
	return f"{uuid4()}@diplomapulse.com"


class BaseUser(AbstractUser, BaseModel):
	username = None

	email = models.EmailField(
		_("email address"),
		unique=True,
		default=generate_default_email,
	)
	first_name = models.CharField(
		_("first name"),
		max_length=150,
	)
	last_name = models.CharField(
		_("last name"),
		max_length=150,
	)
	middle_name = models.CharField(
		_("middle name"),
		max_length=150,
		blank=True,
		null=True,
	)

	registration_code = models.CharField(
		_("registration code"),
		max_length=150,
		default=generate_registration_code,
		null=True,
	)

	profile_picture = models.ImageField(
		_("profile picture"),
		upload_to="profile_pictures",
		blank=True,
		null=True,
	)

	content_type = models.ForeignKey(
		ContentType,
		editable=False,
		null=True,
		on_delete=models.SET_NULL,
	)

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = [
		"first_name",
		"last_name",
	]

	objects: UserManager = UserManager()

	def save(self, *args, **kwargs):
		if not self.content_type:
			self.content_type = ContentType.objects.get_for_model(self.__class__)
		super().save(*args, **kwargs)

	@property
	def concrete(self):
		if self.content_type:
			return self.content_type.get_object_for_this_type(pk=self.pk)
		return self

	class Meta:
		verbose_name = _("Base User")
		verbose_name_plural = _("base users")
