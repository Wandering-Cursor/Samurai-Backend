from django.db import models
from django.utils.translation import gettext_lazy as _

from samurai.core.models.base import BaseUUIDModel


class Group(BaseUUIDModel):
    name = models.CharField(
        _("group_name"),
        max_length=256,
    )
    faculty = models.ForeignKey(
        "Faculty",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")

    def __str__(self) -> str:
        return self.name
