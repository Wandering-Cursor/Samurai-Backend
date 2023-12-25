from uuid import uuid4

from django.db import models

from ._base import BaseModel


class Task(BaseModel):
	id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	order = models.PositiveIntegerField()
	name = models.CharField(
		max_length=255,
		help_text="Внутрішня назва, її бачать лише адміністратори",
	)
	public_name = models.CharField(
		max_length=255,
		default="Назва завдання",
		help_text="Назва, яку бачать користувачі",
	)
	description = models.TextField(
		help_text="Опис завдання, який бачать користувачі",
	)
	reviewer = models.ForeignKey(
		"accounts.Teacher",
		on_delete=models.SET_NULL,
		related_name="tasks",
		null=True,
		blank=True,
	)
	due_date = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return f"Task: {self.name} Ord.#{self.order}"

	class Meta:
		verbose_name = "Task"
		verbose_name_plural = "Tasks"
		ordering = ["order"]
