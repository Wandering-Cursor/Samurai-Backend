from django.db import models
from django.utils.translation import gettext_lazy as _

from ._base import BaseModel


class Project(BaseModel):
    name = models.CharField(
        verbose_name=_("project name"),
        max_length=255,
    )
    description = models.TextField(
        verbose_name=_("description"),
    )
    for_faculty = models.ForeignKey(
        "accounts.Faculty",
        on_delete=models.CASCADE,
        related_name="projects",
        verbose_name=_("related faculty"),
    )
    tasks = models.ManyToManyField(
        "Task",
        related_name="projects",
        verbose_name=_("related tasks"),
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
