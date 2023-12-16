from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _

from .base_user import BaseUser

if TYPE_CHECKING:
	from .faculty import Faculty


class Overseer(BaseUser):
	faculty: Faculty = models.ForeignKey(
		"Faculty",
		on_delete=models.CASCADE,
		related_name="overseers",
	)

	class Meta:
		verbose_name = _("Overseer")
		verbose_name_plural = _("Overseers")
