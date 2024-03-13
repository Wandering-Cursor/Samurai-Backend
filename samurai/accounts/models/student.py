from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _

from .base_account import BaseAccount

if TYPE_CHECKING:
    from samurai.organization.models.group import Group


class Student(BaseAccount):
    group: "Group" = models.ForeignKey(
        "organization.Group",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")
