from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _

from students.choices import TaskState

from ._base import BaseModel

if TYPE_CHECKING:
    from .project import UserProject


class UserTask(BaseModel):
    order = models.IntegerField(
        verbose_name=_("order"),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("task name"),
    )
    description = models.TextField(
        verbose_name=_("description"),
    )
    state = models.CharField(
        max_length=255,
        choices=TaskState.choices,
        default=TaskState.NEW,
        verbose_name=_("state"),
    )

    reviewer = models.ForeignKey(
        "accounts.Teacher",
        related_name="user_tasks",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="The teacher who will review this task",
        verbose_name=_("related reviewer"),
    )
    due_date = models.DateField(
        blank=True,
        null=True,
        help_text="The date when this task should be completed",
        verbose_name=_("due date"),
    )

    comments = models.ManyToManyField(
        "Comment",
        related_name="comments",
        blank=True,
        verbose_name=_("related comments"),
    )

    user_projects: models.ManyToManyField[UserProject]

    class Meta:
        ordering = ["order"]
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    def __str__(self) -> str:
        return f"UserTask: {self.name} #{self.order} ({self.state})"
