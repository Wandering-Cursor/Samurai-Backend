from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

from ..choices import TaskState
from ._base import BaseModel

if TYPE_CHECKING:
	from .project import UserProject


class UserTask(BaseModel):
	order = models.IntegerField()
	name = models.CharField(max_length=255)
	description = models.TextField()
	state = models.CharField(
		max_length=255,
		choices=TaskState.choices,
		default=TaskState.NEW,
	)

	reviewer = models.ForeignKey(
		"accounts.Teacher",
		related_name="user_tasks",
		on_delete=models.CASCADE,
		blank=True,
		null=True,
		help_text="The teacher who will review this task",
	)
	due_date = models.DateField(
		blank=True,
		null=True,
		help_text="The date when this task should be completed",
	)

	comments = models.ManyToManyField(
		"Comment",
		related_name="comments",
		blank=True,
	)

	user_projects: models.ManyToManyField[UserProject]

	class Meta:
		ordering = ["order"]

	def __str__(self):
		return f"UserTask: {self.name} #{self.order} ({self.state})"
