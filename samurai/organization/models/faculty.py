from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _

from samurai.core.models.base import BaseUUIDModel

if TYPE_CHECKING:
    from samurai.organization.models.group import Group


class Faculty(BaseUUIDModel):
    name = models.CharField(
        _("faculty_name"),
        max_length=256,
    )
    groups: "models.ManyToManyRel[Group]"

    class Meta:
        verbose_name = _("Faculty")
        verbose_name_plural = _("Faculties")
