from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _

from .base_user import BaseUser

if TYPE_CHECKING:
	from .faculty import Faculty


class Teacher(BaseUser):
	faculties: models.QuerySet[Faculty] = models.ManyToManyField(
		"Faculty",
		related_name="teachers",
		verbose_name=_("related faculties"),
	)
	contact_information = models.TextField(
		blank=True,
		null=True,
		verbose_name=_("contact information"),
	)

	class Meta:
		verbose_name = _("Teacher")
		verbose_name_plural = _("Teachers")
