from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.enums import AccountTypeEnum

from .base_user import BaseUser

if TYPE_CHECKING:
	from .group import Group


class Student(BaseUser):
	group: Group = models.ForeignKey(
		"Group",
		on_delete=models.CASCADE,
		related_name="students",
		verbose_name=_("related group"),
	)

	@property
	def account_type(self) -> AccountTypeEnum:
		return AccountTypeEnum.STUDENT

	class Meta:
		verbose_name = _("Student")
		verbose_name_plural = _("Students")
