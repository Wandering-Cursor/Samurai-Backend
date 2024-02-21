from django.db import models
from django.utils.translation import gettext_lazy as _

from ._base import BaseModel


class UserProject(BaseModel):
    theme = models.CharField(
        max_length=255,
        verbose_name=_("theme"),
    )
    description = models.TextField(
        verbose_name=_("description"),
    )

    student = models.ForeignKey(
        "accounts.Student",
        related_name="user_projects",
        on_delete=models.CASCADE,
        verbose_name=_("related student"),
    )
    supervisor = models.ForeignKey(
        "accounts.Teacher",
        related_name="user_projects",
        on_delete=models.CASCADE,
        verbose_name=_("related supervisor"),
    )

    tasks = models.ManyToManyField(
        "UserTask",
        related_name="user_projects",
        verbose_name=_("related tasks"),
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("User Project")
        verbose_name_plural = _("User Projects")

    def __str__(self) -> str:
        return f"UserProject: {self.theme} by {self.student}"
