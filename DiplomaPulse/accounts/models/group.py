from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _

from ._base import BaseModel

if TYPE_CHECKING:
    from .faculty import Faculty
    from .student import Student


class Group(BaseModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        _("name of the group"),
        max_length=255,
    )
    faculty: Faculty = models.ForeignKey(
        "Faculty",
        on_delete=models.CASCADE,
        related_name="groups",
        verbose_name=_("related faculty"),
    )
    students: models.QuerySet[Student]

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")
        unique_together = ("name", "faculty")
