from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _

from ._base import BaseModel

if TYPE_CHECKING:
    from .group import Group


class Faculty(BaseModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        _("faculty name"),
        max_length=255,
        unique=True,
    )
    groups: models.QuerySet[Group]

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Faculty")
        verbose_name_plural = _("Groups")
