from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from ._base import BaseModel


class Task(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order = models.PositiveIntegerField(_("order"))
    name = models.CharField(
        _("task name"),
        max_length=255,
        help_text="Внутрішня назва, її бачать лише адміністратори",
    )
    public_name = models.CharField(
        _("public name"),
        max_length=255,
        default="Назва завдання",
        help_text="Назва, яку бачать користувачі",
    )
    description = models.TextField(
        verbose_name=_("description"),
        help_text="Опис завдання, який бачать користувачі",
    )
    reviewer = models.ForeignKey(
        "accounts.Teacher",
        on_delete=models.SET_NULL,
        related_name="tasks",
        null=True,
        blank=True,
        verbose_name=_("reviewer"),
    )
    due_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("due date"),
    )

    def __str__(self) -> str:
        return f"Task: {self.name} Ord.#{self.order}"

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
        ordering = ["order"]
